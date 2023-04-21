import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox as messagebox
import tkinter.scrolledtext as scrolledtext
import pyperclip
import os
# Define function for transforming a single file

def transform_file(input_file_path, output_file_path):
    # Get current date and time
    current_time = datetime.datetime.now().strftime('%a %b %d %I:%M:%S %p %Y')

    # Open input and output files
    with open(input_file_path, 'r') as input_file:
        with open(output_file_path, 'w') as output_file:
            # Write header lines to output file
            output_file.write(f'date {current_time}\n')
            output_file.write('base hex  timestamps absolute\n')
            output_file.write('no internal events logged\n')
            output_file.write('// version 7.5.0\n')
            output_file.write(f'Begin Triggerblock {current_time}\n')
            output_file.write('    0.000000 Start of measurement\n')

            # Transform input file contents
            for line in input_file:
                values = line.split()
                time = float(values[0][1:-1])
                # remove the 0 in front of the can id and add x to the end and make it lower case
                can_id = values[2][1:] + 'x'
                can_id = can_id.lower()
                data = ''.join(values[4:])
                data_bytes = [data[i:i+2] for i in range(0, len(data), 2)]
                formatted_data = ' '.join(data_bytes).upper()
                output_file.write(
                    f'    {time:.6f} 1 {can_id} Rx d 8 {formatted_data.lower()}\n')

            # Write footer line to output file
            output_file.write('End TriggerBlock\n')


# Create GUI and hide it
root = tk.Tk()
# change title to "CAN Transform by Bryan Volckaert 2023"
root.title('Transformer')
# add text to the gui that says:
# use command candump -tz can0 can1 > totransform.log
tk.Label(root, text="Transform candump output to file that is usable in Vector").pack()
tk.Label(root, text="Use command: candump -tz can0 can1 > totransform.log").pack()
# function to copy text to clipboard


def copy_to_clipboard():
    text = "candump -tz can0 can1 > totransform.log"
    pyperclip.copy(text)

# create a box for all the buttons in a row
button_frame = tk.Frame(root)
button_frame.pack()

copy_button = tk.Button(
    button_frame, text="Copy command to clipboard", command=copy_to_clipboard)
copy_button.pack()

def transform_pressed():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select input log", filetypes = (("Log Files", "*.log*"), ("all files", "*.*")))
    print(filename)
    # if filename not defined
    if filename == "":
        messagebox.showerror("Error", "No file selected")
        return
    # print file name to console
    
    # open dialog to select output file
    output_file_path = filedialog.asksaveasfilename(initialdir = "/", title = "Select output log", filetypes = (("Log Files", "*.asc*"), ("all files", "*.*")))
    # if there is no extension add .asc
    if not os.path.splitext(output_file_path)[1]:
        output_file_path += ".asc"
    # call transform function
    transform_file(filename, output_file_path)
    # show message box that says "Transforming complete"
    messagebox.showinfo("Transforming complete", "Transforming complete")
    # close the gui
# transform button
transform_button = tk.Button(button_frame, text="Transform", command=lambda: transform_pressed() )
transform_button.pack()


# close button
close_button = tk.Button(button_frame, text="Close", command=root.destroy)
close_button.pack()

# main loop
root.mainloop()



