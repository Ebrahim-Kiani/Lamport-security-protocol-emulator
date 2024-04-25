import socket
import hashlib

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.client_socket)

        # Connect to the server
        self.client_socket.connect((self.host, self.port))

    def make_hash(self, number_of_hash, text):
        hashtext = str(text)
        for n in range(number_of_hash):
            # Hash a password
            hashencode = hashtext.encode()
            hashtext = hashlib.sha256(hashencode).hexdigest()
            hashencode = hashtext
        return hashtext

    def run(self):
        # Connect to the server
        self.connect()

        # Send number of hash to the server
        number_of_hash = int(input('Please enter the number of hashes: '))
        self.client_socket.send(str(number_of_hash).encode())

        # Receive the response number of hash from the server
        response = self.client_socket.recv(1024).decode()
        print("Received response from server:\n", response)

        # Send username to the server
        username = str(input('Please enter your username: '))
        self.client_socket.send(username.encode())

        # Receive the response username from the server
        response = self.client_socket.recv(1024).decode()
        print("Received response from server:\n", response)

        # Get password from user
        password = 1234

        # Perform login from the client
        for n in range(number_of_hash, 0, -1):
            login_data = str(username) + ' ' + str(self.make_hash(n - 1, str(password)))
            self.client_socket.send(login_data.encode())

            response = self.client_socket.recv(1024).decode()
            print("Received login response from server:\n", response)

        # Close the connection
        self.client_socket.close()

# Create the client instance
client = Client('127.0.1.1', 12345)

# Run the client
client.run()