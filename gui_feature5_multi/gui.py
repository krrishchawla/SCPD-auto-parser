import os
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import sys

# Set the working directory to the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Function to handle button click
def on_button_click():
    user_input = entry.get()
    selected_indices = listbox.curselection()
    selected_values = [options[idx] for idx in selected_indices]
    
    if not user_input:
        messagebox.showerror("Input Error", "Please enter the name of the CSV file.")
        return

    if '.csv' in user_input:
        user_input = user_input.replace('.csv', '')

    if not os.path.isfile(user_input + '.csv'):
        messagebox.showerror("CSV File Not Found", f"Error: {user_input}.csv not found! Make sure it is the right name (case sensitive)")
        return 

    # Run the hello script in a separate thread to keep the GUI responsive
    threading.Thread(target=run_hello_script, args=(user_input, selected_values)).start()

# Function to run the hello.py script with two arguments
def run_hello_script(user_input, selected_values):
    
    try:
        process5_path = os.path.join(script_dir, 'process5.py')
        cmd = ['python3', process5_path, user_input] + selected_values
        print("Command for program:", cmd)
        subprocess.run(cmd)
    except FileNotFoundError:
        messagebox.showerror("Python File Not Found", "Error: process5.py not found!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        root.quit()  # Close the GUI window after processing

# Create the main window
root = tk.Tk()
root.title("SCPD Auto Parser")

# Create a style for the button
style = ttk.Style()
style.configure("Blue.TButton", background="blue")

# Heading for the text input field
label1 = tk.Label(root, text="Type name of CSV file:")
label1.pack()

# Create an entry widget to input text
entry = tk.Entry(root)
entry.pack()

# Heading for the checkboxes
label2 = tk.Label(root, text="Select to include the tuition groups:")
label2.pack()

# Create a list of options for the dropdown
options = ["Honor's Coop - Engineering", "Honor's Coop - Regular", "SCPD NDO", "BOSP"]

# Create a Listbox widget for multiple selection
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
for option in options:
    listbox.insert(tk.END, option)
listbox.pack()

# Create a button with a blue background
button = tk.Button(root, text="Deploy Program", command=on_button_click, borderwidth=3, highlightbackground="blue", highlightcolor="blue")
button.pack()

# Start the GUI main loop
root.mainloop()
