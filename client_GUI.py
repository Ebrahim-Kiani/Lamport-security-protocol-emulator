import tkinter as tk
from client import Client

class ClientGUI:
    def __init__(self, client):
        self.client = client

        self.root = tk.Tk()
        self.root.title("Client")
        
        # Port number
        self.port_label = tk.Label(self.root, text="Port:")
        self.port_label.grid(row=0, column=0)
        self.port_entry = tk.Entry(self.root)
        self.port_entry.grid(row=0, column=1)
        
        # Number of Hashes
        self.number_of_hashes_label = tk.Label(self.root, text="Number of logins:")
        self.number_of_hashes_label.grid(row=1, column=0)
        self.number_of_hashes_entry = tk.Entry(self.root)
        self.number_of_hashes_entry.grid(row=1, column=1)

        # Username
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.grid(row=2, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=2, column=1)

        # Password
        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.grid(row=3, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=3, column=1)

        # Run Button
        self.run_button = tk.Button(self.root, text="Run", command=self.run_client, width=20, bg='green')
        self.run_button.grid(row=4, column=0, columnspan=3)
        
        #login Button
        self.run_button = tk.Button(self.root, text="Login", command=self.run_login, width=20, bg='blue')
        self.run_button.grid(row=6, column=0, columnspan=3)

        # Response Text
        self.response_text = tk.Text(self.root, height=30, width=70)
        self.response_text.grid(row=5, column=0, columnspan=2)
        
        self.root.mainloop()

    def run_client(self):
        # Get the input values
        number_of_hash = int(self.number_of_hashes_entry.get())
        username = self.username_entry.get()
        password = self.password_entry.get()
        port = self.port_entry.get()

        # Set the input values in the client
        self.client.set_input(number_of_hash, username, password, port)

        # Run the client
        self.client.run()
        
        # Cleaning text box before input new
        self.clear_response_text()
        
        # Display the responses in the GUI
        responses = self.client.get_responses()
        for response in responses:
            self.response_text.insert(tk.END, response + "\n")
            
    def run_login(self):
        # Run the client
        self.client.login()
        
        # Cleaning text box before input new
        self.clear_response_text()
        
        # Display the responses in the GUI
        responses = self.client.get_responses()
        
        for response in responses:
            self.response_text.insert(tk.END, response + "\n")            
            
    def clear_response_text(self):
        self.response_text.delete('1.0', tk.END)

# Create the client instance
client = Client('127.0.1.1')

# Create the GUI instance and pass the client object
gui = ClientGUI(client)
