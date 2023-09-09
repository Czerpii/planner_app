
import customtkinter as ctk
from settings import *
from info_bar import *
from buttons_bar import *
from task_manager.task_manager_view import TaskManagerMain
from users_management.user_management_view import *

try:
    from ctypes import windll, byref, sizeof, c_int
except ImportError:
    pass

class Main(ctk.CTk):
    """Main application window class."""
    
    def __init__(self):
        """Initialize the main application window."""
        super().__init__(fg_color="#004B23")
        self.setup_window()
        self.user_management_view()
        self.mainloop()

    def setup_window(self):
        """Configure the main window's appearance and behavior."""
        self.change_title_bar_color()
        self.set_geometry_and_center(WIDTH, HEIGHT)
        self.title('')
        self.set_icon('./empty.ico')

    def set_icon(self, icon_path):
        """Set the window's icon.

        :param icon_path: Path to the icon file.
        """
        try:
            self.iconbitmap(icon_path)
        except:
            print("Błędna ścieżka")
            pass

    def change_title_bar_color(self):
        """Change the color of the title bar if running on Windows."""
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_COLOR_GREEN
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def set_geometry_and_center(self, width, height):
        """Set window geometry and center it on screen.

        :param width: Width of the window.
        :param height: Height of the window.
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        self.geometry(f'{width}x{height}+{center_x}+{center_y}')
        self.minsize(width, height)
        self.maxsize(width, height)

    def user_management_view(self):
        """Initialize and display the user management view."""
        self.configure(fg_color="#0b2e6b")
        LoginView(self)

    def create_ui_elements(self):
        """Create and configure UI elements for the main view."""
        self.configure_grid_main_view()
        InfoBar(self, col=1, row=0, rowspan=2)
        buttons_bar = ButtonsBar(self, 0, 0)
        default_view = TaskManagerMain(self, 0, 1)
        buttons_bar.switch_view(default_view)

    def configure_grid_main_view(self):
        """Configure grid settings for the main view layout."""
        self.columnconfigure(0, weight=5, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=15, uniform='a')
        self.configure(fg_color="#004B23")

    def main_view(self, instance):
        """Display the main application view.

        :param instance: Instance of the current view to be destroyed.
        """
        instance.destroy()
        self.create_ui_elements()
    

if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    Main()
