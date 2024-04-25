import socket
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib

def modify_database():
    # Create the database engine
    engine = create_engine('sqlite:///ServerDataBase.db', echo=True)

    # Create a session factory
    Session = sessionmaker(bind=engine)
    session = Session()

    # Define the base model
    Base = declarative_base()

    # Define your model class
    class Usermodel(Base):
        __tablename__ = 'Usermodel'

        id = Column(Integer, primary_key=True)
        username = Column(String(100))
        password = Column(String)

    # Create the database tables
    Base.metadata.create_all(engine)
    return Usermodel, session








# Hash the password using SHA-256



def make_hash(number_of_hash , text):
    hashtext = str(text)
    for n in range(0 , number_of_hash):
        # Hash a password
        hashencode = hashtext.encode()
        
        hashtext = hashlib.sha256(hashencode).hexdigest()
        
        hashencode = hashtext
    return hashtext





def get_user_info_from_client():

    # Receive data from the client
    number_of_hash = int(client_socket.recv(1024).decode())
    print("Received the number of hash from client:", number_of_hash)

    # Send a response back to the client
    response = "Hello from the server, your number of hash has been recived!\n"
    client_socket.send(response.encode())

    # Receive data from the client
    username_data = client_socket.recv(1024).decode()
    print("Received the username form client:", username_data)

    # Send a response back to the client
    response = "Hello from the server, your usernme has been recived!\n"
    client_socket.send(response.encode())
    return username_data, number_of_hash



def make_and_save_user(number_of_hash, username_data, password , Usermodel):
    
    password_hash = make_hash(number_of_hash , password)
    # Create a new object by usernme
    user = Usermodel(username=username_data , password= password_hash)

    # Add the object to the session
    session.add(user)

    # Commit the session to persist the object in the database
    session.commit()
    
    
def login_user(username_data, number_of_hash, Usermodel, password , session):
    for n in range(number_of_hash, 0, -1 ):
        data = client_socket.recv(1024).decode()
        username_data, password_data = data.split() 
        print("****************************************************************Received the username and hashed password form client:\n", username_data, password_data)
        
        
        password_hash = make_hash(1, password_data)
        user= session.query(Usermodel).filter_by(username=username_data, password=password_hash).first()
        
        if user:
            print('\n*****************************************************************************user found*************************************************************\n')
            response = "message from the server, your usernme and password have been recived and And your account validation is correct! you are loged in :) \n"
            user.password = password_data
            session.commit()
            session.close()
        else:
            response = "message from the server, your usernme and password have been recived and But your account validation is incorrect!**\n"
        client_socket.send(response.encode())
        

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port for the server
host = '127.0.1.1'  # localhost
port = 12345

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for client connections
server_socket.listen(1)

print("Server listening on {}:{}\n".format(host, port))
# Accept a client connection
client_socket, addr = server_socket.accept()
print("Connected to client:\n", addr)    





# main job for loging user
Usermodel ,session = modify_database()

password = 1234

username_data, number_of_hash = get_user_info_from_client()

make_and_save_user(number_of_hash, username_data, password , Usermodel)

login_user(username_data, number_of_hash, Usermodel, password , session )


# Close the connection
client_socket.close()
server_socket.close()





