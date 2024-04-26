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

        # Start Button
        self.start_button = tk.Button(self.root, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=10)

        # Response Text
        self.response_text = tk.Text(self.root, height=30, width=70)
        self.response_text.pack(pady=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def start_server(self):
        self.thread = threading.Thread(target=self.start_server_thread)
        self.thread.start()

    def start_server_thread(self):
        self.server = Server()

            # Start the server
        self.server.start_server()

        while True:
            responses = self.server.get_responses()
            if responses:
                for response in responses:
                    # Add the response to the GUI
                    self.response_text.insert(tk.END, response + "\n")

                # Clear the responses in the Server instance
                self.server.clear_responses()

            # Sleep for a short duration to avoid constant CPU usage
            time.sleep(0.5)     
            
            
    def clear_response_text(self):
        self.response_text.delete('1.0', tk.END)
        
    def on_closing(self):
        if self.server:
            self.server.stop()
        self.root.destroy()


# Create the server GUI instance
if __name__ == "__main__":
    server_gui = ServerGUI()