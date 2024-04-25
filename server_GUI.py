import tkinter as tk
from tkinter import messagebox

# Create the main window
window = tk.Tk()
window.title("Server")

# Create the entry widget for the math expression
entry = tk.Entry(window, width=20, font=("Arial", 16))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")