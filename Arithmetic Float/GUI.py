import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import zipfile
import os
from Comp import *

class FileCompressorDecompressor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("File Compressor/Decompressor")
        self.geometry("400x350")
        self.config(bg="lightblue") 

        self.operation = tk.StringVar(value="compress")

        self.header_label = tk.Label(self, text=" Floating point Arithmetic Coding", font=("Arial", 16, "bold"), bg="lightblue", fg="black")
        self.header_label.pack(pady=20)

        tk.Radiobutton(self, text="Compress", variable=self.operation, value="compress", font=("Arial", 12, "bold"), bg="lightblue", fg="black").pack(pady=10)
        tk.Radiobutton(self, text="Decompress", variable=self.operation, value="decompress", font=("Arial", 12, "bold"), bg="lightblue", fg="black").pack(pady=10)

        self.input_file_button = tk.Button(self, text="Select File", command=self.select_input_file, font=("Arial", 12), bg="lightgreen", fg="black")
        self.input_file_button.pack(pady=10)


        self.execute_button = tk.Button(self, text="Execute", command=self.execute, font=("Arial", 14, "bold"), bg="lightcoral", fg="white")
        self.execute_button.pack(pady=20)

        self.input_file = None
        self.output_file = None

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename(title="Select Input File")
        if self.input_file:
            print(f"Input file selected: {self.input_file}")

    def execute(self):
        if self.operation.get() == "compress":
            Comp(self.input_file)
        elif self.operation.get() == "decompress":
            Decomp(self.input_file)


if __name__ == "__main__":
    app = FileCompressorDecompressor()
    app.mainloop()
