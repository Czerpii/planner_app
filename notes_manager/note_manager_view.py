
import customtkinter as ctk
from PIL import Image
import os
from notes_manager.note_manager_reciver import *


NOTE_BG = "#212529"
NOTE_BORDER = "#343A40"
NOTE_FG = "#6C757D"
NOTE_HOVER = "#616971"

class NoteManagerMain(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color=NOTE_BG)
        self.grid(column=col, row=row, sticky='nsew')
        
        self.configure_layout()
        
        self.color_palette = self.import_ico_images("color_palette.png")
        
        self.note_bar = NoteManagerNoteBar(self, 0,0)
        self.note_tiles = NoteManagerNotesTiles(self,0,1)
        self.note_manager = NoteManager()
        
    
        self.bind("<Button-1>", self.note_bar.off_focus)
    
    def configure_layout(self):
        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=8, uniform='a')
                      
    def import_ico_images(self, image_name):
        
        current_path = os.path.dirname(os.path.realpath(__file__))
        full_path = os.path.join(current_path, "ico_images", image_name)
        
        image = ctk.CTkImage(dark_image=Image.open(full_path),
                             light_image=Image.open(full_path),
                             size=(25,25))
        return image

    def top_level_color_management(self, parent, widget, button_command):
        
        x_pos = widget.winfo_rootx()
        y_pos = widget.winfo_rooty()-10
        
        self.top_level = ctk.CTkToplevel(parent, fg_color=NOTE_BG)
        self.top_level.lift(parent)
        self.top_level.overrideredirect(True)
        self.top_level.geometry(f"340x40+{x_pos}+{y_pos}")
        
        frame = ctk.CTkFrame(self.top_level, fg_color=NOTE_BG, border_width=0)
        frame.pack(expand="true", fill='both')
        
        colors = ["#F94144","#F3722C","#F8961E","#F9844A","#F9C74F","#90BE6D","#43AA8B","#4D908E","#577590","#277DA1"]
        
        for color in colors:
            b_color = ctk.CTkButton(frame, text="", width=30, height=30, fg_color=color, command=lambda color=color: button_command(color))
            b_color.pack(side='left', pady=10, padx=2)
        
        self.top_level.bind("<Leave>", self.close_win)
         
    def close_win(self, event):
        self.check_cursor_position(self.top_level)
    
    def check_cursor_position(self, widget):
        widget = widget
        # Pobierz aktualne współrzędne i wymiary okna
        x = widget.winfo_x()
        y = widget.winfo_y()
        width = widget.winfo_width()
        height = widget.winfo_height()

        # Pobierz aktualne współrzędne kursora myszy
        mouse_x = widget.winfo_pointerx()
        mouse_y = widget.winfo_pointery()

        # Sprawdź, czy kursor myszy jest wewnątrz okna
        if not (x <= mouse_x <= x + width and y <= mouse_y <= y + height):
            # Jeżeli kursor myszy jest poza oknem, zniszcz okno
            widget.destroy()
        
        
                  
class NoteManagerNoteBar(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="transparent")
        self.grid(column= col, row=row, sticky='nsew')
        
        self.note_main = parent
        
        self.create_default_frame()
        self.create_expanded_note_frame()
        self.expanded_frame.pack_forget()
        
        self.bind("<Button-1>", self.off_focus) 
    
    def create_default_frame(self):
        
        self.default_frame = ctk.CTkFrame(self, fg_color=NOTE_FG, width=500, border_width=3, border_color=NOTE_BORDER, corner_radius=10)
        self.default_frame.pack(pady=15)
        self.default_frame.pack_propagate(False)
        
 
        note_label = ctk.CTkLabel(self.default_frame, text="Utwórz notatkę...",font = ctk.CTkFont(family="Arial", size=25))
        note_label.pack(side='left', padx=10)
        
        
        button = ctk.CTkButton(self.default_frame, text="", width=30, height=30)
        button.pack(side='right', padx=10)
        
        button1 = ctk.CTkButton(self.default_frame, text="", width=30, height=30)
        button1.pack(side='right', padx=10)
        
        
         
 
        self.default_frame.bind("<Button-1>", self.on_focus)
        note_label.bind("<Button-1>", self.on_focus)

    def create_expanded_note_frame(self):
        self.expanded_frame = ctk.CTkFrame(self, fg_color=NOTE_FG, width=500, border_width=3, border_color=NOTE_BORDER, corner_radius=10)
        self.expanded_frame.pack(pady=15)
        
        self.expanded_frame.columnconfigure(0, weight=1, uniform='a')
        self.expanded_frame.rowconfigure(0, weight=2, uniform='a')
        self.expanded_frame.rowconfigure(1, weight=4, uniform='a')
        self.expanded_frame.rowconfigure(2, weight=2, uniform='a')
        self.expanded_frame.grid_propagate(False)
        
        self.entry_title = ctk.CTkEntry(self.expanded_frame,
                                        placeholder_text="Tytuł", 
                                        font = ctk.CTkFont(family="Arial", size=20),
                                        fg_color="transparent",
                                        placeholder_text_color='white',
                                        border_width=0)
        self.entry_title.grid(column=0, row=0, sticky='nsew', pady=5, padx=10)
        
        self.entry_description = ctk.CTkTextbox(self.expanded_frame, 
                                                font = ctk.CTkFont(family="Arial", size=15),
                                                fg_color="transparent",
                                                )
        self.entry_description.grid(column=0, row=1, sticky='nsew', padx=10)
        
        self.button_frame = ctk.CTkFrame(self.expanded_frame, fg_color="transparent")
        self.button_frame.grid(column=0, row=2, sticky='nsew', padx=10, pady=5)
        
        self.color_button = ctk.CTkButton(self.button_frame,
                                          text='',
                                          width=30,
                                          fg_color='transparent',
                                          hover = False,
                                          image= self.note_main.import_ico_images("color_palette.png"),
                                          command=self.change_color)
        self.color_button.pack_propagate(False)
        self.color_button.pack(side='left', padx=2, pady=2)
        
        self.cancel_button =ctk.CTkButton(self.button_frame,
                                          text='',
                                          width=30,
                                          fg_color='transparent',
                                          hover=False,
                                          image=self.note_main.import_ico_images("cancel.png"),
                                          command=self.cancel_button_click)
        self.cancel_button.pack_propagate(False)
        self.cancel_button.pack(side='right', padx=2, pady=2)
        
        self.confirm_button =ctk.CTkButton(self.button_frame,
                                          text='',
                                          width=30,
                                          fg_color='transparent',
                                          hover=False,
                                          image=self.note_main.import_ico_images("tick.png"),
                                          command=None)
        self.confirm_button.pack_propagate(False)
        self.confirm_button.pack(side='right', padx=2, pady=2)
          
    def change_color(self):
        self.note_main.top_level_color_management(self, self.color_button, self.set_color)              
    
    def set_color(self, color):
        self.expanded_frame.configure(fg_color=color)
        self.note_main.top_level.destroy()
              
    def on_focus(self, event):
        self.note_main.rowconfigure(0, weight=4, uniform='a')
        self.default_frame.pack_forget()
        self.expanded_frame.pack(pady=15)
        self.entry_description.focus()
        
    def off_focus(self, event):
        self.note_main.rowconfigure(0, weight=1, uniform='a')
        self.expanded_frame.pack_forget()
        self.default_frame.pack(pady=15)

    def cancel_button_click(self):
        self.note_main.rowconfigure(0, weight=1, uniform='a')
        self.entry_title.delete(0, "end")
        self.entry_title.configure(placeholder_text = 'Tytuł')
        self.entry_description.delete(0.0, 'end')
        self.expanded_frame.pack_forget()
        self.default_frame.pack(pady=15)

class NoteManagerNotesTiles(ctk.CTkScrollableFrame):
    def __init__(self, parent, col, row ):
        super().__init__(parent, fg_color="transparent")
        self.grid(column=col, row=row, sticky='nsew')
        
        self.main_instance = parent
        
        self.configure_grid()
        self.create_columns()
        self.test()
        # self.create_tiles()
                      
    def configure_grid(self):
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0,1,2,3), weight=1, uniform='a')
        
    def create_columns(self):
        
        self.col_1 = ctk.CTkFrame(self, fg_color='transparent')
        self.col_1.grid(column=0, row=0, sticky='nsew')
        
        self.col_2 = ctk.CTkFrame(self, fg_color='transparent')
        self.col_2.grid(column=1, row=0, sticky='nsew')
        
        self.col_3 = ctk.CTkFrame(self, fg_color='transparent')
        self.col_3.grid(column=2, row=0, sticky='nsew')
        
        self.col_4 = ctk.CTkFrame(self, fg_color='transparent')
        self.col_4.grid(column=3, row=0, sticky='nsew')
        
        self.columns = {1: self.col_1, 2: self.col_2, 3: self.col_3, 4: self.col_4}
    
    def test(self):
        NoteTile(self.col_1, self.main_instance)
    
    def create_tiles(self):
        
        
        for key, master in self.columns.items():
            ctk.CTkLabel(master=master, text="text", fg_color='red', height=100).pack(side='top', expand='true', fill='both', padx=2, pady=2)

        ctk.CTkLabel(master=self.columns[1], text="text", fg_color='blue', height=100).pack(side='top', expand='true', fill='both', padx=2, pady=2)
        
        ctk.CTkLabel(master=self.columns[1], text="text", fg_color='blue', height=150).pack(side='top', expand='true', fill='both', padx=2, pady=2)
        
        ctk.CTkLabel(master=self.columns[4], text="text", fg_color='blue', height=50).pack(side='top', expand='true', fill='both', padx=2, pady=2)
        
        ctk.CTkLabel(master=self.columns[2], text="text", fg_color='yellow', height=400).pack(side='top', expand='true', fill='both', padx=2, pady=2)
        
        ctk.CTkLabel(master=self.columns[3], text="text", fg_color='blue', height=200).pack(side='top', expand='true', fill='both', padx=2, pady=2)
     

class NoteTile(ctk.CTkFrame):
    """NoteTile is a custom frame for displaying a note with title and description."""
    
    def __init__(self, parent, main_instance):
        super().__init__(parent, fg_color=NOTE_FG, width=500, border_width=3, border_color=NOTE_BORDER, corner_radius=10)
        
        self.note_bar = parent
        self.note_main = main_instance
        self.configure_grid()
        self.initialize_widgets()
        self.pack(pady=15)
        
    def configure_grid(self):
        """Configure grid layout."""
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure(1, weight=4, uniform='a')
        self.rowconfigure(2, weight=2, uniform='a')
        self.grid_propagate(False)
        
    def initialize_widgets(self):
        """Initialize widgets."""
        self.initialize_entry_title()
        self.initialize_entry_description()
        self.initialize_button_frame()
        
    def initialize_entry_title(self):
        """Initialize title entry."""
        self.entry_title = ctk.CTkEntry(self,
                                        placeholder_text="Tytuł", 
                                        font=ctk.CTkFont(family="Arial", size=20),
                                        fg_color="transparent",
                                        placeholder_text_color='white',
                                        border_width=0)
        self.entry_title.grid(column=0, row=0, sticky='nsew', pady=5, padx=10)
        
    def initialize_entry_description(self):
        """Initialize description entry."""
        self.entry_description = ctk.CTkTextbox(self, 
                                                font=ctk.CTkFont(family="Arial", size=15),
                                                fg_color="transparent")
        self.entry_description.grid(column=0, row=1, sticky='nsew', padx=10)
        
    def initialize_button_frame(self):
        """Initialize button frame."""
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(column=0, row=2, sticky='nsew', padx=10, pady=5)
        
        self.color_button = ctk.CTkButton(self.button_frame,
                                          text='',
                                          width=30,
                                          fg_color='transparent',
                                          hover=False,
                                          image=self.note_main.import_ico_images("color_palette.png"),
                                          command=self.change_color)
        self.color_button.pack_propagate(False)
        self.color_button.pack(side='left', padx=2, pady=2)
    
               
    def change_color(self):
        """Open top level window with color palette."""
        self.note_main.top_level_color_management(self, self.color_button, self.set_color)
        
    def set_color(self, color):
        """Set the selected color as the background ."""
        self.configure(fg_color=color)
        self.note_main.top_level.destroy()
        
    def cancel_button_click(self):
        self.note_main.rowconfigure(0, weight=1, uniform='a')
        self.note_bar.new_note_frame.pack_forget()
        self.note_bar.default_frame.pack(pady=15)



