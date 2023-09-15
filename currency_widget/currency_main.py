
import customtkinter as ctk

from ui_components import *



class CurrencyMain(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew")
        
        
        self.configure_layout()
        
        ctk.CTkFrame(self, fg_color='red').grid(column=0,row=0, sticky='nsew')
        ctk.CTkFrame(self, fg_color='blue').grid(column=0,row=1, sticky='nsew')
        
        self.currency_calculator = CurrencyCalculatorUI(self, 1, 0)
        ctk.CTkFrame(self, fg_color='orange').grid(column=1,row=1, sticky='nsew')
        
        ctk.CTkFrame(self, fg_color='pink').grid(column=2,row=0, sticky='nsew')
        ctk.CTkFrame(self, fg_color='gray').grid(column=2,row=1, sticky='nsew')

    def configure_layout(self):
        self.columnconfigure((0,2), weight=1, uniform='a')
        self.columnconfigure(1, weight=5, uniform='a')
        self.rowconfigure((0,1), weight=1, uniform='a')
        




class Main(ctk.CTk):
    """Main application window class."""
    
    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        self.setup_window()
        self.configure_grid_main_view()
        CurrencyMain(self, 0,1)

        self.mainloop()

    def setup_window(self):
        """Configure the main window's appearance and behavior."""
        self.set_geometry_and_center(1080, 720)
     



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



    def configure_grid_main_view(self):
        """Configure grid settings for the main view layout."""
        self.columnconfigure(0, weight=5, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=15, uniform='a')
    

    

if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    Main()
