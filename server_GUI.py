import tkinter as tk
from tkinter import messagebox
import threading
from server import Server


class ServerGUI:
    def __init__(self):
        self.server = None
        self.thread = None

        self.root = tk.Tk()
        self.root.title("Server")
        # Port number
        self.port_label = tk.Label(self.root, text="Port:")
        self.port_label.grid(row=0, column=0)
        self.port_entry = tk.Entry(self.root)
        self.port_entry.grid(row=0, column=1)
        
        # Password
        self.Password_label = tk.Label(self.root, text="Password:")
        self.Password_label.grid(row=1, column=0)
        self.Password_entry = tk.Entry(self.root)
        self.Password_entry.grid(row=1, column=1)
        
        # Set data Button
        self.start_button = tk.Button(self.root, text="Set password and port", command=self.set_data , bg='green')
        self.start_button.grid(row=2, column=1)
        
        # Start Button
        self.start_button = tk.Button(self.root, text="Start Server", command=self.start_server, bg='blue')
        self.start_button.grid(row=3, column=0)

        # Response Text
        self.response_text = tk.Text(self.root, height=30, width=70)
        self.response_text.grid(row=4, column=0 ,columnspan=2)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def set_data(self):
        self.server = Server()
        password = self.Password_entry.get()
        port = self.port_entry.get()        
        self.server.set_port_password(port, password)
        
    def start_server(self):
        self.clear_response_text()  # Clear the response text
        self.thread = threading.Thread(target=self.start_server_thread)
        self.thread.start()
        
    def update_responses(self, responses):
        self.response_text.delete('1.0', tk.END)
        for response in responses:
            self.response_text.insert(tk.END, response + "\n")
            
    def start_server_thread(self):
        
        self.server.set_gui(self)  # Pass the GUI instance reference to the Server

        # Start the server
        self.server.start_server()

        # Rest of the start_server_thread method code    
        #self.update_responses()
            
    def clear_response_text(self):
        self.response_text.delete('1.0', tk.END)
        
    def on_closing(self):
        if self.server:
            self.server.stop()
        self.root.destroy()


# Create the server GUI instance
if __name__ == "__main__":
    server_gui = ServerGUI()