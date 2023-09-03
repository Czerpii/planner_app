import customtkinter as ctk
from settings import *
from info_bar import *
from buttons_bar import *
from TaskManagerView import TaskManagerMain
from user_management_view import *

try:
    from ctypes import windll, byref, sizeof, c_int
except ImportError:
    pass


class Main(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BLACK)
        self.setup_window()
        self.user_management_view()
        self.mainloop()


    def setup_window(self):
        self.change_title_bar_color()
        self.set_geometry_and_center(WIDTH, HEIGHT)
        self.title('')
        self.set_icon('./empty.ico')

    def set_icon(self, icon_path):
        try:
            self.iconbitmap(icon_path)
        except:
            print("Błędna ścieżka")
            pass

    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_COLOR_BLACK
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def set_geometry_and_center(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        self.geometry(f'{width}x{height}+{center_x}+{center_y}')
        self.minsize(width, height)
        self.maxsize(width, height)

    def user_management_view(self):
        self.configure(fg_color="#0b2e6b")
        LoginView(self)
    
    def create_ui_elements(self):
        self.configure_grid_main_view()
        InfoBar(self, col=1, row=0, rowspan=2)
        ButtonsBar(self, 0, 0)
        TaskManagerMain(self, 0, 1)
    
    def configure_grid_main_view(self):
        self.columnconfigure(0, weight=5, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=15, uniform='a')
        self.configure(fg_color=BLACK)
        
    def main_view(self, instance):
        instance.pack_forget()
        self.create_ui_elements()

    
if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    Main()
