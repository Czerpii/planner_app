
import os
import customtkinter as ctk
from PIL import Image
from task_manager.task_manager_view import TaskManagerMain
from notes_manager.note_manager_view import NoteManagerMain
from currency_widget.currency_main import CurrencyMain
import themes_manager

class ButtonsBar(ctk.CTkFrame):
    """
    Class representing the ButtonsBar frame. This frame provides buttons for switching
    between different views
    """
    
    def __init__(self, parent, col, row):
        """Initialize the ButtonsBar frame.

        :param parent: Parent widget.
        :param col: Column position for grid placement.
        :param row: Row position for grid placement.
        """
        super().__init__(parent, fg_color=themes_manager.get_color("background"), corner_radius=0)
        self.task_manager_button = None
        self.note_button = None
        self.grid(column=col, row=row, sticky='nsew',)
        self.parent = parent
        self.current_view = None
        self.active_button = None

        # View initializations
        self.task_manager_view = None
        self.note_manager_view = None
        self.currency_widget_view = None

        # UI setup
        self.setup_ui_elements()

    def setup_ui_elements(self):
        """Setup UI elements for the ButtonsBar."""
        # Configuring grid for layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, uniform='a')
        # Image setup for buttons
        current_directory = os.path.dirname(os.path.abspath(__file__))
        task_image_path = os.path.join(current_directory, "button_image/tasks.png")
        note_image_path = os.path.join(current_directory, "button_image/note.png")
        currency_image_path = os.path.join(current_directory, "button_image/currency.png")
        task_image = self.load_image(task_image_path, (35, 35))
        note_image = self.load_image(note_image_path, (35, 35))
        currency_image = self.load_image(currency_image_path, (35, 35))
        # TaskManager Button
        self.task_manager_button = self.create_button(task_image, self.task_manager_button_click)
        self.task_manager_button.grid(column=0, row=0, sticky='ns', padx=5, pady=2)

        # NoteManager Button
        self.note_button = self.create_button(note_image,self.note_manager_button_click)
        self.note_button.grid(column=1, row=0, sticky='ns', pady=2)
        
        #Exchange rate button
        self.exchange_button = self.create_button(currency_image,self.exchange_rate_button_click)
        self.exchange_button.grid(column=2, row=0, sticky='ns', pady=2, padx=5)

    def load_image(self, path, size):
        """Load an image from a given path and resize it to the specified size.

        :param path: Path to the image file.
        :param size: Tuple containing width and height for resizing.
        :return: Resized image.
        """
        return ctk.CTkImage(dark_image=Image.open(path), light_image=Image.open(path), size=size)

    def create_button(self, image, command):
        """Create a button with the specified image and command.

        :param image: Image to display on the button.
        :param command: Command to execute when the button is clicked.
        :return: Created button.
        """
        return ctk.CTkButton(self, text="", fg_color="transparent", hover_color=themes_manager.get_color('fg_frame'), image=image, command=command)

    def init_task_manager_view(self):
        """Initialize the TaskManager view if it's not already initialized."""
        if not self.task_manager_view:
            self.task_manager_view = TaskManagerMain(self.parent, 0, 1)

    def init_note_manager_view(self):
        """Initialize the NoteManager view if it's not already initialized."""
        if not self.note_manager_view:
            self.note_manager_view = NoteManagerMain(self.parent, 0, 1)

    def init_currency_widget_view(self):
        """Initialize the CurrencyMain view if it's not already initialized."""
        if not self.currency_widget_view:
            self.currency_widget_view = CurrencyMain(self.parent, 0, 1)
          
    def switch_view(self, new_view, new_active_button):
        """Switch to the given view, hiding the current one."""
        if self.current_view:
            self.current_view.grid_forget()
        self.current_view = new_view
        self.current_view.grid(column=0, row=1, sticky='nsew')

        # Reset the color of the previously active button
        if self.active_button:
            self.active_button.configure(fg_color="transparent")

        # Set the new active button and change its color
        self.active_button = new_active_button
        self.active_button.configure(fg_color=themes_manager.get_color("fg_frame")) 

    def task_manager_button_click(self):
        """Switch to the TaskManager view."""
        self.init_task_manager_view()
        self.switch_view(self.task_manager_view, self.task_manager_button)

    def note_manager_button_click(self):
        """Switch to the NoteManager view."""
        self.init_note_manager_view()
        self.switch_view(self.note_manager_view, self.note_button)
        
    def exchange_rate_button_click(self):
        """Switch to the ExchangeRate view"""
        self.init_currency_widget_view()
        self.switch_view(self.currency_widget_view, self.exchange_button)