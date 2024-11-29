import subprocess as sb
import tkinter as tk
from tkinter import simpledialog, ttk

# Create the main application window
w = tk.Tk()
w.title("Winget Command Center")
w.geometry("900x600")

# Create a frame for better layout
frame = ttk.Frame(w)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Add a vertical scrollbar
scrollbar = ttk.Scrollbar(frame, orient="vertical")

# Create the Text widget for displaying output
text_area = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set, font=("Arial", 12))
text_area.pack(side="left", fill="both", expand=True)

# Configure the scrollbar to work with the Text widget
scrollbar.config(command=text_area.yview)
scrollbar.pack(side="right", fill="y")

# Create a label to show the current action
app_label = tk.Label(w, text="No action selected", font=("Arial", 14), fg="blue")
app_label.pack(pady=5)

def execute_command(command, prompt_text=None):
    """Executes a winget command with optional app name input."""
    if prompt_text:
        appname = simpledialog.askstring("Winget Command", prompt_text)
        if not appname:
            text_area.insert(tk.END, "Operation canceled by user.\n")
            text_area.see(tk.END)
            return
        command = f"{command} {appname}"
        app_label.config(text=f"Executing: {command}")
    else:
        app_label.config(text=f"Executing: {command}")
    
    try:
        # Log the execution process
        text_area.insert(tk.END, f"Running: {command}...\n")
        text_area.see(tk.END)
        
        # Run the winget command
        output = sb.check_output(f"winget {command}", shell=True, text=True, stderr=sb.STDOUT)
        text_area.insert(tk.END, output + "\n")
        text_area.insert(tk.END, f"Command '{command}' completed successfully.\n")
    
    except sb.CalledProcessError as e:
        # Handle errors and display in the text area
        text_area.insert(tk.END, f"Error running '{command}': {e.output}\n")
    except Exception as ex:
        text_area.insert(tk.END, f"An unexpected error occurred: {ex}\n")
    
    text_area.see(tk.END)  # Auto-scroll to the end

# Add buttons for various winget commands
button_frame = ttk.Frame(w)
button_frame.pack(pady=10)

install_button = ttk.Button(button_frame, text="Install App", command=lambda: execute_command("install", "Enter the app name to install"))
install_button.grid(row=0, column=0, padx=5, pady=5)

upgrade_button = ttk.Button(button_frame, text="Upgrade App", command=lambda: execute_command("upgrade", "Enter the app name to upgrade"))
upgrade_button.grid(row=0, column=1, padx=5, pady=5)

uninstall_button = ttk.Button(button_frame, text="Uninstall App", command=lambda: execute_command("uninstall", "Enter the app name to uninstall"))
uninstall_button.grid(row=0, column=2, padx=5, pady=5)

list_button = ttk.Button(button_frame, text="List Installed Apps", command=lambda: execute_command("list"))
list_button.grid(row=1, column=0, padx=5, pady=5)

search_button = ttk.Button(button_frame, text="Search for App", command=lambda: execute_command("search", "Enter the app name to search"))
search_button.grid(row=1, column=1, padx=5, pady=5)

# Run the application
w.mainloop()
