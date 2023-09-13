
import customtkinter as ctk
from PIL import Image
from task_manager.task_manager_view import TaskManagerMain
from notes_manager.note_manager_view import NoteManagerMain
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

        # View initializations
        self.task_manager_view = TaskManagerMain(self.parent, 0, 1)
        self.note_manager_view = NoteManagerMain(self.parent, 0, 1)
        self.note_manager_view.grid_forget()
        self.task_manager_view.grid_forget()

        # UI setup
        self.setup_ui_elements()

    def setup_ui_elements(self):
        """Setup UI elements for the ButtonsBar."""
        # Configuring grid for layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, uniform='a')

        # Image setup for buttons
        task_image = self.load_image("./button_image/tasks.png", (40, 40))
        note_image = self.load_image("./button_image/note.png", (40, 40))

        # TaskManager Button
        self.task_manager_button = self.create_button(task_image, self.task_manager_button_click)
        self.task_manager_button.grid(column=0, row=0, sticky='ns', padx=5, pady=2)

        # NoteManager Button
        self.note_button = self.create_button(note_image,self.note_manager_button_click)
        self.note_button.grid(column=1, row=0, sticky='ns', pady=2)

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
        return ctk.CTkButton(self, text="", fg_color=themes_manager.get_color("button"), hover_color=themes_manager.get_color('button_hover'), image=image, command=command)

    def switch_view(self, new_view):
        """Switch to the given view, hiding the current one."""
        if self.current_view:
            self.current_view.grid_forget()
        self.current_view = new_view
        self.current_view.grid(column=0, row=1, sticky='nsew')

    def task_manager_button_click(self):
        """Switch to the TaskManager view."""
        self.switch_view(self.task_manager_view)

    def note_manager_button_click(self):
        """Switch to the NoteManager view."""
        self.switch_view(self.note_manager_view)