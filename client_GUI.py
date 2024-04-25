from tkinter import *
from tkinter import messagebox

# Create the main window
window = Tk()
window.title("Server")
# Configure pad X and pad Y for the main window
window.config(padx=300, pady=300)

# Create the entry widget for User input
entry = Entry(window, width=20, font=("Arial", 16))
entry.grid(row=200, column=100, columnspan=1, padx=10, pady=10, sticky="ew")

# list box for logs 
list_box_logs = Listbox(window)
list_box_logs.grid(row=2, column=0, sticky=N+S+E+W)
# Run the main event loop
window.mainloop()