import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading
import sys

# Determine the directory where the executable or script is located
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)

# Function to handle button click
def on_button_click():
    # Prompt user to select a CSV file
    csv_file_path = filedialog.askopenfilename(
        initialdir=script_dir,
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    if not csv_file_path:
        messagebox.showerror("Error", "No CSV file selected.")
        return

    selected_indices = listbox.curselection()
    selected_values = [options[idx] for idx in selected_indices]

    # Start the progress bar and run the hello script in a separate thread to keep the GUI responsive
    progress_bar.start()
    threading.Thread(target=run_hello_script, args=(csv_file_path, selected_values)).start()

# Function to run the process5.py script with two arguments
def run_hello_script(csv_file_path, selected_values):
    try:
        process5_path = os.path.join(script_dir, 'process5.py')
        cmd = ['python3', process5_path, csv_file_path] + selected_values
        print("Command for program:", cmd)
        subprocess.run(cmd)
    except FileNotFoundError:
        messagebox.showerror("Python File Not Found", "Error: process5.py not found!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        progress_bar.stop()
        root.quit()  # Close the GUI window after processing

# Create the main window
root = tk.Tk()
root.title("SCPD Auto Parser")

# Create a style for the button
style = ttk.Style()
style.configure("Blue.TButton", background="blue")

# Heading for the checkboxes
label1 = tk.Label(root, text="Select to filter the tuition groups:")
label1.pack()

# Create a list of options for the dropdown
options = ["Honor's Coop - Engineering", "Honor's Coop - Regular", "SCPD NDO", "BOSP"]

# Create a Listbox widget for multiple selection
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
for option in options:
    listbox.insert(tk.END, option)
listbox.pack()

# Create a button to select CSV file
select_button = tk.Button(root, text="Select CSV File and Deploy", command=on_button_click, borderwidth=3, highlightbackground="blue", highlightcolor="blue")
select_button.pack()

# Create a progress bar
progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.pack()

# Start the GUI main loop
root.mainloop()
