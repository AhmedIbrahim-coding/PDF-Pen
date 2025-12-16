import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("720x480")
        self.title("PDF Pen")
        self.resizable(False, False)

        self.files_list = []

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
                                     command=self.merging)
        self.merge_button.place(y=400, x=180, anchor="center")

        # Split
        self.split_button = ctk.CTkButton(self, width=150, 
                                     height=60, 
                                     text="Split", 
                                     font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
                                     state="disabled",
                                     fg_color="#18185F",
                                     text_color="#A1A1A1")
        self.split_button.place(y=400, x=360, anchor="center")

        # Compress
        self.compress_button = ctk.CTkButton(self, width=150, 
                                     height=60, 
                                     text="Compress", 
                                     font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
                                     state="disabled",
                                     fg_color="#18185F",
                                     text_color="#A1A1A1")
        self.compress_button.place(y=400, x=540, anchor="center")

    def Browse(self):
        files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])

        if files:
            if len(self.files_list) == 0:
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
                

            # add the selected files to the files list
            self.files_list.extend(files)
            self.show_added_files(files)

    def enable_buttons(self):
        for btn in (self.split_button, self.merge_button, self.compress_button):
            btn.configure(state="normal", fg_color="#2C2AB4", hover_color="#1e1cb1", text_color="white")

    def show_added_files(self, files_list):
        # add all the selected files to the files field
        for file in files_list:
            file_label = ctk.CTkFrame(self.files_field, width=400, height=50, fg_color="#254661")
            file_label.pack(pady=3, padx=5, anchor="w", fill="x", before=self.adding_button) # add the labels before the add button

            # display file's name
            file_fullname = os.path.basename(file)
            max_name_len = 15
            file_name = f"{file_fullname[:max_name_len+1]}..." if len(file_fullname) > max_name_len else file_fullname
            file_name_label = ctk.CTkLabel(file_label, text=file_name, font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
            file_name_label.place(rely=0.5, relx=0, x=10, anchor="w")

            # display file's path
            max_path_len = 30
            path = file if len(file) <= max_path_len else file[:max_path_len+1]
            path_label = ctk.CTkLabel(file_label, text=path, font=("Arial", 13))

    def merging(self):
        self.merge_window = ctk.CTkToplevel(self)
        self.merge_window.geometry("960x540")
        self.title("Merge")
        self.merge_window.resizable(False, False)
        self.merge_window.grab_set()
        self.merge_window.focus()
        
