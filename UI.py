import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("720x480")
        self.title("PDF Pen")
        self.resizable(False, False)

        self.files_list = []

        # A field to drag and drop files
        drop_field = ctk.CTkFrame(self, width=700, height=300, fg_color="#2E2E2E")
        drop_field.pack(padx = 10, pady =10)

        # prepare the drage_and_drop image
        pil_drop_icon = Image.open("Assets\\drag-and-drop.png")
        drop_icon = ctk.CTkImage(light_image=pil_drop_icon,
                                 dark_image=pil_drop_icon,
                                 size=(100,100))
        # display the image
        drop_icon_lable = ctk.CTkLabel(drop_field, width=100, height=100, text="", image=drop_icon)
        drop_icon_lable.place(relx=0.5, rely=0.5, y= -30, anchor="center")

        # A text under the icon to declear what's going on
        drop_text = ctk.CTkLabel(drop_field, text="Drag and Drop, or", font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
        drop_text.place(relx=0.5, rely=0.5, y=50, anchor="center")

        # A button to browse and get files
        browse_button = ctk.CTkButton(drop_field, 
                                      width=50, 
                                      height=30, 
                                      text="Browse", 
                                      fg_color="#2C2AB4", 
                                      hover_color="#1e1cb1",
                                      command=self.Browse)
        browse_button.place(relx=0.5, rely=0.5, y=80, anchor="center")

        # Buttons to Merge, Split, and Compress & Make it disabled initially 

        # Merge
        self.merge_button = ctk.CTkButton(self, width=150, 
                                     height=60, 
                                     text="Merge", 
                                     font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
                                     state="disabled",
                                     fg_color="#18185F",
                                     text_color="#A1A1A1")
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
                self.enable_buttons()
            self.files_list.extend(files)

    def enable_buttons(self):
        for btn in (self.split_button, self.merge_button, self.compress_button):
            btn.configure(state="normal", fg_color="#2C2AB4", hover_color="#1e1cb1", text_color="white")