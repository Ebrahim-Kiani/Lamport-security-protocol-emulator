import socket
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib

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

    def start(self):
        self.create_database()
        self.create_sockets()
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

        print("Server listening on {}:{}".format(self.host, self.port))

    def accept_client_connection(self):
        # Accept a client connection
        self.client_socket, addr = self.server_socket.accept()
        print("Connected to client:", addr)

    def handle_client(self):
        # Receive data from the client
        number_of_hash = int(self.client_socket.recv(1024).decode())
        print("Received the number of hash from client:", number_of_hash)

        # Send a response back to the client
        response = "Hello from the server, your number of hash has been received!\n"
        self.client_socket.send(response.encode())

        # Receive data from the client
        username_data = self.client_socket.recv(1024).decode()
        print("Received the username from client:", username_data)

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
            print("Received the username and hashed password from client:\n", username_data, password_data)

            password_hash = self.make_hash(1, password_data)
            user = self.session.query(Usermodel).filter_by(username=username_data, password=password_hash).first()

            if user:
                print('\nUser found\n')
                response = "Message from the server: Your username and password have been received, and your account validation is correct! You are logged in :)\n"
                user.password = password_data
                self.session.commit()
                self.session.close()
            else:
                response = "Message from the server: Your username and password have been received, but your account validation is incorrect!\n"
            self.client_socket.send(response.encode())

# Create the server instance and start the server
server = Server()
server.start()