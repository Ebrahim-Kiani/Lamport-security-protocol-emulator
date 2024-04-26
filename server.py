import socket
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib
import queue

Base = declarative_base()
class Usermodel(Base):
    __tablename__ = 'Usermodel'

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Server:
    def __init__(self):
        self.host = '127.0.1.1'
        self.port = 12345
        self.server_socket = None
        self.client_socket = None
        self.engine = None
        self.Session = None
        self.session = None
        self.responses = queue.Queue()
        

    def add_response(self, response):
            self.responses.put(response)

    def get_next_response(self):
        if not self.responses.empty():
            return self.responses.get()
        else:
            return None
        
    def start_server(self):
        self.create_database()
        self.create_sockets()

        # Notify that the server has started

        self.accept_client_connection()
        self.handle_client()

    def create_database(self):
        # Create the database engine
        self.engine = create_engine('sqlite:///ServerDataBase.db', echo=True)

        # Create a session factory
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Define the base model
        Base = declarative_base()

        # Create the database tables
        Base.metadata.create_all(self.engine)

    def create_sockets(self):
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the host and port
        self.server_socket.bind((self.host, self.port))

        # Listen for client connections
        self.server_socket.listen(1)
        string= str("Server listening on {}:{}".format(self.host, self.port))+ str("\n")
        self.add_response(string)

    def accept_client_connection(self):
        # Accept a client connection
        self.client_socket, addr = self.server_socket.accept()
        string = str("Connected to client:") + str(addr)+"\n"
        self.add_response(string)

    def handle_client(self):
        # Receive data from the client
        number_of_hash = int(self.client_socket.recv(1024).decode())
        string = str("Received the number of hash from client:") + str(number_of_hash)+"\n"
        self.add_response(string)

        # Send a response back to the client
        response = "Hello from the server, your number of hash has been received!\n"
        self.client_socket.send(response.encode())

        # Receive data from the client
        username_data = self.client_socket.recv(1024).decode()
        string = str("Received the username from client:") + str(username_data)
        self.add_response(string)

        # Send a response back to the client
        response = "Hello from the server, your username has been received!\n"
        self.client_socket.send(response.encode())

        password = "1234"
        self.make_and_save_user(number_of_hash, username_data, password)

        self.login_user(username_data, number_of_hash, password)

        # Close the connection
        self.client_socket.close()
        self.server_socket.close()

    def make_hash(self, number_of_hash, text):
        hashtext = str(text)
        for n in range(0, number_of_hash):
            # Hash a password
            hashencode = hashtext.encode()
            hashtext = hashlib.sha256(hashencode).hexdigest()
            hashencode = hashtext
        return hashtext

    def make_and_save_user(self, number_of_hash, username_data, password):
        password_hash = self.make_hash(number_of_hash, password)
        # Create a new object by username
        user = Usermodel(username=username_data, password=password_hash)

        # Add the object to the session
        self.session.add(user)

        # Commit the session to persist the object in the database
        self.session.commit()

    def login_user(self, username_data, number_of_hash, password):
        for n in range(number_of_hash, 0, -1):
            data = self.client_socket.recv(1024).decode()
            username_data, password_data = data.split()
            string = str("**Received the username and hashed password from client:") + str(password_data) +  str(username_data) +"\n"
            self.add_response(string)

            password_hash = self.make_hash(1, password_data)
            user = self.session.query(Usermodel).filter_by(username=username_data, password=password_hash).first()

            if user:
                self.add_response('\nUser found\n')
                response = "**message from the server, your usernme and password have been checked and And your account validation is correct! you are loged in :) \n"
                self.add_response(string)
                user.password = password_data
                self.session.commit()
                self.session.close()
            else:
                response = "message from the server, your usernme and password have been checked and But your account validation is incorrect!**\n"
            self.client_socket.send(response.encode())

