import customtkinter as ctk
import sys
from settings import *
try: 
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

from info_bar import *
from buttons_bar import *
from TaskManagerView import TaskManagerMain

class Main(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BLACK)
        self.change_title_bar_color()
        self.geometry_with_center(WIDTH, HEIGHT)
        self.title('')
        
        try:
            self.iconbitmap('./empty.ico')
        except: 
            print("Błędna ścieżka")
            pass
      

        #tworzenie siatki głównego okna
        self.columnconfigure(0, weight=5, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.rowconfigure(0, weight=1,uniform='a')
        self.rowconfigure(1, weight=15,uniform='a')
        
        
        #aktywowanie startowych modułów
        #ctk.CTkLabel(self, text='', fg_color='red').grid(column = 1, row=0, rowspan = 2, sticky = 'nsew')
        #ctk.CTkLabel(self, text='', fg_color='blue').grid(column = 0, row=1,  sticky = 'nsew')
        #ctk.CTkLabel(self, text='', fg_color='yellow').grid(column = 0, row=0,  sticky = 'nsew')
        
        InfoBar(self, col= 1, row=0, rowspan =2)
        ButtonsBar(self, 0,0)
        TaskManagerMain(self,0,1)
        
        self.mainloop()
        
       
        
        
    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_COLOR_BLACK
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
           pass 
       
    def geometry_with_center(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - width/2)
        center_y = int(screen_height/2 - height/2)
        self.geometry(f'{width}x{height}+{center_x}+{center_y}')
        self.minsize(width, height)
        
    def create_buttons(self):
        pass

if __name__ == '__main__':
    Main()