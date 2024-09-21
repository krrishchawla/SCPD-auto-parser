import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading

csv_file_path = ""
output_dir = ""

# Function to select the CSV file
def select_csv():
    global csv_file_path
    csv_file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not csv_file_path:
        messagebox.showerror("Error", "No CSV file selected.")
    else:
        csv_label.config(text=os.path.basename(csv_file_path))

# Function to select the output directory
def select_output_dir():
    global output_dir
    output_dir = filedialog.askdirectory(
        title="Select Output Directory"
    )
    if not output_dir:
        messagebox.showerror("Error", "No output directory selected.")
    else:
        output_label.config(text=os.path.basename(output_dir))

# Function to handle the deploy button click
def deploy():
    if not csv_file_path:
        messagebox.showerror("Error", "No CSV file selected.")
        return

    if not output_dir:
        messagebox.showerror("Error", "No output directory selected.")
        return

    selected_indices = listbox.curselection()
    selected_values = [options[idx] for idx in selected_indices]

    # Start the progress bar and run the process5.py script in a separate thread to keep the GUI responsive
    progress_bar.start()
    threading.Thread(target=run_process_script, args=(csv_file_path, output_dir, selected_values)).start()

# Function to run the process5.py script with two arguments
def run_process_script(csv_file_path, output_dir, selected_values):
    try:
        process5_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'process5.py')
        cmd = ['python3', process5_path, csv_file_path, output_dir] + selected_values
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

instruction_label = tk.Label(root, text="This program takes in a Roster CSV file, sorts it per class, and applies filters if any.", justify=tk.LEFT)
instruction_label.pack(pady=10)

# Heading for the checkboxes
label1 = tk.Label(root, text="1. Select filters (can do multiple), if any:")
label1.pack(pady=10)

# Create a list of options for the dropdown
options = ["Honor's Coop - Engineering", "Honor's Coop - Regular", "SCPD NDO", "BOSP"]

# Create a Listbox widget for multiple selection
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
for option in options:
    listbox.insert(tk.END, option)
listbox.pack(pady=10)

label2 = tk.Label(root, text="2. Choose the input Roster CSV file:")
label2.pack(pady=10)

# Create buttons for selecting CSV file and output directory
csv_button = tk.Button(root, text="Select Roster File (csv)", command=select_csv, borderwidth=3, highlightbackground='blue', highlightcolor="blue", padx=20)
csv_button.pack(pady=5)
csv_label = tk.Label(root, text="")
csv_label.pack(pady=5)

label3 = tk.Label(root, text="3. Choose where to save the output files:")
label3.pack(pady=10)

output_button = tk.Button(root, text="Select Output Folder", command=select_output_dir, borderwidth=3, highlightbackground='blue', highlightcolor="blue", padx=25)
output_button.pack(pady=5)
output_label = tk.Label(root, text="")
output_label.pack(pady=5)


label4 = tk.Label(root, text="4. Finally, deploy program to have it do its magic:")
label4.pack(pady=10)

# Create a button to deploy the program
deploy_button = tk.Button(root, text="Deploy", command=deploy, borderwidth=3, highlightbackground='blue', highlightcolor="blue", padx=40)
deploy_button.pack(pady=20)

# Create a progress bar
progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.pack(pady=10)

# Start the GUI main loop
root.mainloop()
