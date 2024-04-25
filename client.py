import socket
import hashlib

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.number_of_hash = None
        self.username = None
        self.password = None
        self.responses = []

    def connect(self):
        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    def set_input(self, number_of_hash, username, password):
        self.number_of_hash = int(number_of_hash)
        self.username = username
        self.password = int(password)

    def run(self):
        # Connect to the server
        self.connect()

        # Send number of hash to the server
        self.client_socket.send(str(self.number_of_hash).encode())

        # Receive the response number of hash from the server
        response = self.client_socket.recv(1024).decode()
        self.responses.append("Received response from server:\n" + response)

        # Send username to the server
        self.client_socket.send(self.username.encode())

        # Receive the response username from the server
        response = self.client_socket.recv(1024).decode()
        self.responses.append("Received response from server:\n" + response)

        # Perform login from the client
        for n in range(self.number_of_hash, 0, -1):
            login_data = str(self.username) + ' ' + str(self.make_hash(n - 1, self.password))
            self.client_socket.send(login_data.encode())

            response = self.client_socket.recv(1024).decode()
            self.responses.append("Received login response from server:\n" + response)

        # Close the connection
        self.client_socket.close()

    def get_responses(self):
        return self.responses