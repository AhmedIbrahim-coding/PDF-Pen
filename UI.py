import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os
from core import merge_files, split_files, compress_files, EntryError

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("720x480")
        self.title("PDF Pen")
        self.resizable(False, False)

        # A dictionary to hold the files paths with keys
        self.files_dictionary = {}
        self.displayed_files = {}

        # A field to display files
        self.files_field = ctk.CTkFrame(self, width=700, height=300, fg_color="#2E2E2E")
        self.files_field.pack(padx = 10, pady =10)


        # prepare the browse image
        pil_drop_icon = Image.open("Assets\\import.png")
        drop_icon = ctk.CTkImage(light_image=pil_drop_icon,
                                 dark_image=pil_drop_icon,
                                 size=(150,150))
        # display the image
        drop_icon_lable = ctk.CTkLabel(self.files_field, width=150, height=150, text="", image=drop_icon)
        drop_icon_lable.place(relx=0.5, rely=0.5, y=-30, anchor="center")

        # A button to browse and get files
        browse_button = ctk.CTkButton(self.files_field, 
                                      width=50, 
                                      height=30, 
                                      text="Browse", 
                                      fg_color="#2C2AB4", 
                                      hover_color="#1e1cb1",
                                      command=self.Browse)
        browse_button.place(relx=0.5, rely=0.5, y=70, anchor="center")

        # Buttons to Merge, Split, and Compress & Make it disabled initially 

        # Merge
        self.merge_button = ctk.CTkButton(self, width=150, 
                                     height=60, 
                                     text="Merge", 
                                     font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
                                     state="disabled",
                                     fg_color="#18185F",
                                     text_color="#A1A1A1",
                                     command=self.on_merge_click)
        self.merge_button.place(y=400, x=180, anchor="center")

        # Split
        self.split_button = ctk.CTkButton(self, width=150, 
                                     height=60, 
                                     text="Split", 
                                     font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
                                     state="disabled",
                                     fg_color="#18185F",
                                     text_color="#A1A1A1",
                                     command=self.on_split_click)
        self.split_button.place(y=400, x=360, anchor="center")

        # Compress
        self.compress_button = ctk.CTkButton(self, width=150, 
                                     height=60, 
                                     text="Compress", 
                                     font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
                                     state="disabled",
                                     fg_color="#18185F",
                                     text_color="#A1A1A1",
                                     command=self.on_compress_click)
        self.compress_button.place(y=400, x=540, anchor="center")

    def Browse(self):
        files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])

        if files:
            if len(self.files_dictionary) == 0:
                # destroy the current frame and make it scrollable frame
                self.enable_buttons()
                self.files_field.destroy()
                self.files_field = ctk.CTkScrollableFrame(self, width=700, height=290, fg_color="#2E2E2E")
                self.files_field.pack(padx = 10, pady =10)

                # add an icon for the adding button
                pil_add_icon = Image.open("Assets\\plus.png")
                add_icon = ctk.CTkImage(light_image=pil_add_icon,
                                        dark_image=pil_add_icon,
                                        size=(30,30))
                
                # add a button once to add more files, but only once if the files list is impty
                self.adding_button = ctk.CTkButton(self.files_field,
                                                   height=50,
                                                   width=50,
                                                   text="",
                                                   fg_color="#3050b9",
                                                   hover_color="#24508A",
                                                   image=add_icon, command=self.Browse)
                self.adding_button.pack(pady=3, padx=5, anchor="w")
                

            # add the selected files to the files dictionary
            start_key = len(self.files_dictionary) + 1 # to store the lenght before adding items
            key = start_key 
            for file in files:
                self.files_dictionary[key] = file
                key += 1
            self.show_added_files(files, start_key)

    def enable_buttons(self):
        for btn in (self.split_button, self.merge_button, self.compress_button):
            btn.configure(state="normal", fg_color="#2C2AB4", hover_color="#1e1cb1", text_color="white")

    def show_added_files(self, files_list, start_key):
        # add all the selected files to the files field
        for file in files_list:
            file_label = FileFrame(self.files_field, file_path=file, file_key=start_key)
            file_label.pack(pady=3, padx=5, anchor="w", fill="x", before=self.adding_button) # add the labels before the add button



    def on_merge_click(self):
        file_direcotry = self.select_directory("Save Merged Files")
        if file_direcotry:
            merge_files(self.files_dictionary, file_direcotry)

    def on_split_click(self):
        # A child window to get the pages for every split
        window = ctk.CTkToplevel(self)
        window.focus()
        window.grab_set()
        window.geometry("320x120")
        window.title("Split Options")
        window.resizable(False, False)
        
        pages_entry = ctk.CTkEntry(window, width=50, height=30, placeholder_text="", font=("Arial", 12), border_color="gray")
        pages_entry.place(relx=0.5, rely=0, y=50, anchor="center")

        text_label1 = ctk.CTkLabel(window, text="Split at ", font=("Arial", 12))
        text_label1.place(x=110, y=50, rely=0, relx=0, anchor="center")
        text_label2 = ctk.CTkLabel(window, text="pages.", font=("Arial", 12))
        text_label2.place(x=210, y=50, rely=0, relx=0, anchor ="center")

        # a func to start splitting when hit the split button
        def start_split():
            try:
                range = int(pages_entry.get())

                if range == 0 or type(range) != int:
                    raise EntryError()
                
                output_dir = filedialog.askdirectory(title="Save files in...")
                if output_dir:
                    window.destroy()
                    split_files(self.files_dictionary, output_dir, range)
            except:
                pages_entry.configure(border_color="red")

        split_button = ctk.CTkButton(window, width=80, height=30, text="Split", font=("Arial", 12), command=start_split)
        split_button.place(relx=1, rely=1, y=-30, x=-50, anchor="center")

    def on_compress_click(self):
        output_dir = filedialog.askdirectory(title="Output where")
        if output_dir:
            print(output_dir)
            compress_files(self.files_dictionary, output_dir)


    def select_directory(self, window_title):
        file_direcotry = filedialog.asksaveasfilename(title=window_title,
                                                      initialfile= "Untitled",
                                                      defaultextension=".pdf", 
                                                      filetypes=[("PDF files", "*.pdf")])
        if file_direcotry:
            return file_direcotry


class FileFrame(ctk.CTkFrame):
    def __init__(self, master, file_path, file_key):
        super().__init__(master=master, width=690, height=50, fg_color="#254661")
        # master is the scrollable frame; its master is the App instance
        self.app = getattr(master, "master", None)
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_key = file_key

        self.display_file_name()
        self.display_file_path()

    def display_file_name(self):
        name = self.file_name if len(self.file_name) <= 15 else f"{self.file_name[:16]}..."
        file_name_label = ctk.CTkLabel(self, text=name, font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
        file_name_label.place(rely=0.5, relx=0, x=10, anchor="w")

    def display_file_path(self):
        path = self.file_path if len(self.file_path) <= 30 else f"{self.file_path[:31]}..."
        path_label = ctk.CTkLabel(self, text=path, font=("Arial", 10))
        path_label.place(rely=0.5, relx=0.5, x=-30, anchor="w")


