
import customtkinter as ctk
from PIL import Image
import os
import random
from notes_manager.note_manager_reciver import *
from ICommand import *
from invoker import *

NOTE_BG = "#212529"
NOTE_BORDER = "#343A40"
NOTE_FG = "#6C757D"
NOTE_HOVER = "#616971"

class NoteManagerMain(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color=NOTE_BG, corner_radius=5)
        self.grid(column=col, row=row, sticky='nsew')
        
        self.configure_layout()
        
        self.color_palette = self.import_ico_images("color_palette.png")
        
       
        self.note_tiles = NoteManagerNotesTiles(self,0,1)
        self.note_bar = NoteManagerNoteBar(self, 0,0, self.note_tiles)
        self.note_manager = NoteManager()
        self.invoker = Invoker()
    
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
    
    def save_note(self, **params):
        reciver = self.note_manager
        save_note_command = Save(reciver, **params)
        self.invoker.set_command(save_note_command)
        self.invoker.press_button()
    
    def delete_note(self, id_note):
        reciver = self.note_manager
        delete_note_command = Delete(reciver, id_note)
        self.invoker.set_command(delete_note_command)
        self.invoker.press_button()
                        
class NoteManagerNoteBar(ctk.CTkFrame):
    def __init__(self, parent, col, row, tiles_note_manager_instance):
        super().__init__(parent, fg_color="transparent", corner_radius=5)
        self.grid(column= col, row=row, sticky='nsew')
        
        self.note_main = parent
        self.note_tiles_manager = tiles_note_manager_instance
        
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
                                          command=self.save_button_click)
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
        self.expanded_frame.configure(fg_color = NOTE_FG)
        self.default_frame.pack(pady=15)

    def save_button_click(self):
        params = {
            'id': random.randint(1,10000),
            'title': self.entry_title.get(),
            'description': self.entry_description.get(index1='0.0', index2='end'),
            'background_color': self.expanded_frame.cget('fg_color')
        }
        self.note_main.save_note(**params)
        self.note_tiles_manager.add_new_note(title = params['title'],
                                             description = params['description'],
                                             background_color = params['background_color'],
                                             id_note = params['id'])
            

class NoteManagerNotesTiles(ctk.CTkScrollableFrame):
    """
    A class to manage and display notes in a grid layout.

    Attributes:
    ----------
    note_main : parent instance
        The main instance of the note manager.
    tiles : dict
        Dictionary to store note tiles by their IDs.
    row : int
        Current row position for the next tile.
    column : int
        Current column position for the next tile.
    """

    def __init__(self, parent, col, row):
        """Initialize the NoteManagerNotesTiles."""
        super().__init__(parent, fg_color="transparent")
        self.grid(column=col, row=row, sticky='nsew')
        
        self.note_main = parent
        self.tiles = {}
        self.row = 0
        self.column = 0
        
        self.configure_grid()
        self.show_saved_notes()
                      
    def configure_grid(self):
        """Configure grid layout for the frame."""
        self.columnconfigure((0,1,2,3), weight=1, uniform='a')
    
    def show_saved_notes(self):
        """Display saved notes from the file."""
        data = NoteManager().import_notes()
        
        for dictionary in data:
            tile = NoteTile(self, main_instance=self.note_main, col=self.column, row=self.row, title_text=dictionary['title'], desc_text=dictionary['description'], tile_color=dictionary['background_color'], id_note=dictionary['id'])
            self.tiles[str(dictionary['id'])] = tile
            self.column += 1
            if self.column > 3:
                self.column = 0
                self.row += 1
        
    def add_new_note(self, title, description, background_color, id_note):
        """Add a new note to the beginning of the grid and shift other notes."""
        tile = NoteTile(self, main_instance=self.note_main, col=self.column, row=self.row, title_text=title, desc_text=description, tile_color=background_color, id_note=id_note)
        self.tiles[str(id_note)] = tile
        self.column += 1
        if self.column > 3:
            self.column = 0
            self.row += 1
        self.reposition_notes()

    def delete_note(self, id_note):
        """Delete the note with the given ID and reposition the remaining notes."""
        tile = self.tiles.get(str(id_note))
        if tile:
            tile.destroy()
            del self.tiles[str(id_note)]
            self.reposition_notes()

    def reposition_notes(self):
        """Reposition notes to fill empty spaces in the grid."""
        notes = list(self.tiles.values())
        col, row = 0, 0
        for note in notes:
            note.grid(column=col, row=row)  # Assuming NoteTile uses .grid() method for positioning
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.column, self.row = col, row
        

class NoteTile(ctk.CTkFrame):
    """NoteTile is a custom frame for displaying a note with title and description."""
    
    def __init__(self, parent, main_instance, col, row, title_text, desc_text, tile_color, id_note):
        super().__init__(parent, fg_color=tile_color, width=500, border_width=3, border_color=NOTE_BORDER, corner_radius=10)
        
        self.parent = parent
        self.note_main = main_instance
        # self.note_main = main_instance
        self.title_text = title_text
        self.desc_text = desc_text
        self.id_note = id_note
        
        self.configure_grid()
        self.initialize_widgets()
        self.grid(column=col, row=row, sticky='nsew', padx=2, pady=2)
        
    def configure_grid(self):
        """Configure grid layout."""
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure(1, weight=4, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        self.grid_propagate(False)
        
    def initialize_widgets(self):
        """Initialize widgets."""
        self.initialize_label_title()
        self.initialize_label_description()
        self.initialize_button_frame()
        
    def initialize_label_title(self):
        """Initialize title entry."""
        self.entry_title = ctk.CTkLabel(self,
                                        text = self.title_text,
                                        font=ctk.CTkFont(family="Arial", size=20),
                                        justify = 'left',
                                        anchor = 'w',
                                        fg_color="transparent",
                                        )
        self.entry_title.grid(column=0, row=0, sticky='nsew', pady=5, padx=10)
        
    def initialize_label_description(self):
        """Initialize description entry."""
        self.entry_description = ctk.CTkTextbox(self, 
                                                font=ctk.CTkFont(family="Arial", size=15),
                                                
                                                fg_color="transparent",
                                                padx=2)
        self.entry_description.insert("0.0", self.desc_text )
        self.entry_description.configure(state='disable')
        self.entry_description.grid(column=0, row=1, sticky='nsew', padx=10)
        self.entry_description.bind('<MouseWheel>', self._on_entry_description_scroll)

    def _on_entry_description_scroll(self, event):
        """Handle the mouse wheel scroll event for the entry_description."""
        self.entry_description.yview_scroll(-1*(event.delta//120), "units")
        return "break"
        
        
    def initialize_button_frame(self):
        """Initialize button frame."""
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(column=0, row=2, sticky='nsew', padx=10, pady=5)
        
        self.color_button = ctk.CTkButton(self.button_frame,
                                          text='X',
                                          width=30,
                                          fg_color='transparent',
                                          hover=False,
                                          command=self.delete_tile)
        self.color_button.pack_propagate(False)
        self.color_button.pack(side='right', padx=2, pady=2)
    
    def delete_tile(self):
        self.parent.delete_note(self.id_note)
        self.note_main.delete_note(self.id_note)
         
    # def change_color(self):
    #     """Open top level window with color palette."""
    #     self.note_main.top_level_color_management(self, self.color_button, self.set_color)
        
    # def set_color(self, color):
    #     """Set the selected color as the background ."""
    #     self.configure(fg_color=color)
    #     self.note_main.top_level.destroy()
        
    # def cancel_button_click(self):
    #     self.note_main.rowconfigure(0, weight=1, uniform='a')
    #     self.note_bar.new_note_frame.pack_forget()
    #     self.note_bar.default_frame.pack(pady=15)



