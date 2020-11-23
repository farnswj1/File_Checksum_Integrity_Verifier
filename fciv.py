'''
Justin Farnsworth
File Checksum Integrity Verifier (FCIV)
November 22, 2020

This is a simple GUI that allows the user to get the checksum 
of a file. The user can also specify which hash function to use.

NOTE: Not all hash functions are included in this program. This is 
largely because some functions are no longer supported. Also, some 
functions, notably the SHAKE series, require additional arguments. 
For simplicity and convenience, those algorithms are not included.
'''

# Imported modules
import hashlib
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename
from os.path import basename


# FCIV window class
class FCIV(object):
    # Constructor
    def __init__(self):
        # Window
        self.__window = tk.Tk()
        self.__window.title("File Checksum Integrity Verifier")
        self.__window.geometry("600x600")
        self.__window.resizable(width=False, height=False)

        # Font and size
        font = ("Courier New", 20, "bold")

        # Select File Button
        self.__filename = None
        self.__select_file_button = tk.Button(
            self.__window,
            text="Select a file:",
            font=font,
            bg="#aaaaaa",
            command=self.__select_file
        )
        self.__select_file_button.place(relx=0.5, y=75, anchor=tk.CENTER)

        # Filename Label
        self.__filename_label = tk.Label(
            self.__window,
            font=font
        )
        self.__filename_label.place(relx=0.5, y=125, anchor=tk.CENTER)

        # Select Hash Label
        self.__select_hash_label = tk.Label(
            self.__window,
            text="Select a hash function:",
            font=font
        )
        self.__select_hash_label.place(relx=0.5, y=225, anchor=tk.CENTER)

        # List of Hash Functions (exclude the SHAKE hash functions)
        self.__selected_hash = tk.StringVar()
        self.__hashes = Combobox(
            self.__window,
            textvariable=self.__selected_hash,
            font=font,
            values=[func for func in sorted(hashlib.algorithms_guaranteed) if not "shake" in func],
            height=5
        )
        self.__window.option_add('*TCombobox*Listbox.font', font) # Modifies the items' font
        self.__hashes.place(relx=0.5, y=275, anchor=tk.CENTER)

        # Encrypt Button
        self.__encrypt_button = tk.Button(
            self.__window,
            text="Get Checksum",
            font=font,
            bg="#ffff00",
            command=self.__get_checksum,
        )
        self.__encrypt_button.place(relx=0.5, y=375, anchor=tk.CENTER)

        # Checksum Textbox
        self.__checksum = tk.Text(
            self.__window,
            font=font,
            width=40,
            height=4
        )
        self.__checksum.place(relx=0.5, y=450, width=520, anchor=tk.N)

        # Run the main loop
        self.__window.mainloop()
    

    # Allow the user to select the file and save the filename
    def __select_file(self):
        self.__filename = askopenfilename(title="Select a file")
        self.__filename_label.config(text=basename(self.__filename))
    

    # Compute the checksum of the file
    def __compute_checksum(self, filename, hash_function):
        # Read the file (in bytes) and encrypt the contents
        with open(filename, "rb") as f:
            # Feed the algorithm one chunk at a time
            while chunk := f.read(4096):
                hash_function.update(chunk)
        
        # Return the checksum in hexadecimal notation
        return hash_function.hexdigest().upper()

    
    # Get the checksum using the specified hash function
    def __get_checksum(self):
        # Get the selected hash function
        selected_hash = self.__selected_hash.get()

        # Clear the checksum textbox before adding text to it
        self.__checksum.delete("1.0", tk.END)

        # If both entries are valid, print the checksum. Otherwise, print a message
        if self.__filename and selected_hash in self.__hashes["values"]:
            self.__checksum.insert(
                tk.INSERT,
                self.__compute_checksum(self.__filename, getattr(hashlib, selected_hash)())
            )
        else:
            self.__checksum.insert(tk.INSERT, "Select a file and hash function.")


# Run the FCIV program if the script is ran directly 
if __name__ == "__main__":
    FCIV()
