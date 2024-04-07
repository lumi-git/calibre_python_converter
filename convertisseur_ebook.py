import os, subprocess, threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Import ttk module for progress bar

class EbookConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.directory = ''
        self.output_directory = ''
        self.CALIBRE_PATH = 'C:\\Program Files\\Calibre2\\ebook-convert.exe'

        self.title("Ebook Converter")
        self.geometry("400x300")  # Set a reasonable default size


        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        container = ttk.Frame(self)

        container.pack(expand=True, fill="both", padx=10, pady=10)

        self.label_source_dir = ttk.Label(container, text="No Source Directory Selected")
        self.label_source_dir.pack(fill='x', padx=10)

        self.btn_choose_source = ttk.Button(container, text="Choose Source Directory", command=self.choose_source_directory)

        self.btn_choose_source.pack(fill='x', pady=5, padx=10)

        self.label_dest_dir = ttk.Label(container, text="No Destination Directory Selected")
        self.label_dest_dir.pack(fill='x', padx=10)

        self.btn_choose_dest = ttk.Button(container, text="Choose Destination Directory", command=self.choose_destination_directory)
        self.btn_choose_dest.pack(fill='x', pady=5, padx=10)

        self.thread = threading.Thread(target=self.start_conversion)

        self.btn_convert = ttk.Button(container, text="Convert", command=self.thread.start)

        self.btn_convert.pack(fill='x', pady=10, padx=10)

        self.progress_bar = ttk.Progressbar(container, orient='horizontal', mode='determinate')
        self.progress_bar.pack(fill='x', pady=5, padx=10)

        self.current_file_label = ttk.Label(container, text="processing: ")
        self.current_file_label.pack(fill='x', padx=10)

        exit_button = ttk.Button(container, text="Exit", command=self.exitapp)
        #red color for the button background

        exit_button.pack(fill='x', pady=5, padx=10)


    def exitapp(self):
        self.destroy()
        exit()

    def addSpace(self) :
        label_source_dir = tk.Label(self, text="")
        label_source_dir['pady'] = 10
        label_source_dir.pack()


    def choose_source_directory(self):
        self.directory = filedialog.askdirectory()
        self.label_source_dir.config(text=f"Source: {self.directory}")

    def choose_destination_directory(self):
        self.output_directory = filedialog.askdirectory()
        self.label_dest_dir.config(text=f"Destination: {self.output_directory}")

    def start_conversion(self):

        if not self.directory or not self.output_directory:
            messagebox.showerror("Error", "Please select both source and destination directories.")
            return

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        absolute_in_path = os.path.abspath(self.directory)
        absolute_out_path = os.path.abspath(self.output_directory)

        epub_files = [filename for filename in os.listdir(absolute_in_path) if filename.endswith(".epub")]
        num_files = len(epub_files)

        if num_files == 0:
            messagebox.showinfo("No files", "There are no .epub files to convert in the selected directory.")
            return

        self.progress_bar['maximum'] = num_files
        self.progress_bar['value'] = 0

        for filename in epub_files:
            if not self.thread.is_alive():
                return
            new_name = filename.replace(" ", "_")
            input_file = os.path.join(absolute_in_path, new_name)
            out_file = os.path.join(absolute_out_path, new_name).replace(".epub", ".azw3")

            os.rename(os.path.join(absolute_in_path, filename), input_file)
            self.current_file_label.config(text=f"processing: {filename}")
            # Start the conversion process
            subprocess.call([self.CALIBRE_PATH, input_file, out_file], shell=True)

            # Update progress bar after each file is converted
            self.progress_bar['value'] += 1
            self.update_idletasks()

        messagebox.showinfo("Complete", "All files have been converted.")

if __name__ == "__main__":
    app = EbookConverterApp()
    app.mainloop()
