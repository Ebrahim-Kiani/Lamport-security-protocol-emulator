import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port for the server
host = '127.0.1.1'  # localhost
port = 12345

# Connect to the server
client_socket.connect((host, port))




import hashlib



# Hash the password using SHA-256



def make_hash(number_of_hash , text):
    hashtext = str(text)
    for n in range(0 , number_of_hash):
        # Hash a password
        hashencode = hashtext.encode()
        
        hashtext = hashlib.sha256(hashencode).hexdigest()
        
        hashencode = hashtext
    return hashtext

# get pssword and number of hash from user
username = str(input('please enter your username:'))
password = 1234
number_of_hash = int(input('please enter number of login:'))



# Send number of hash to the server

client_socket.send(str(number_of_hash).encode())

# Receive the response number of hash from the server
response = client_socket.recv(1024).decode()
print("Received response from server:\n", response)

# Send username to the server

client_socket.send(username.encode())

# Receive the response username from the server
response = client_socket.recv(1024).decode()
print("Received response from server:\n", response)


# doing login from client

for n in range(number_of_hash,0 , -1 ):
    
    login_data = str(username) +' '+ str(make_hash(n-1 , str(password)))
    
    client_socket.send(login_data.encode())

    response = client_socket.recv(1024).decode()
    print("Received loging response from server:\n", response)
    





# Close the connection
client_socket.close()