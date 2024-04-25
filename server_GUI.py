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

        self.root.mainloop()

    def start_server(self):
        self.thread = threading.Thread(target=self.start_server_thread)
        self.thread.start()

    def start_server_thread(self):
        try:
            self.server = Server()
            self.server.start_server()

            # Display the responses in the GUI
            
            while True:
                response = self.server.get_next_response()
                if response:
                    self.response_text.insert(tk.END, response + "\n")
                else:
                    break

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.server = None

    def on_closing(self):
        if self.server:
            self.server.stop()
        self.root.destroy()


# Create the server GUI instance
if __name__ == "__main__":
    server_gui = ServerGUI()