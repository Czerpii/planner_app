import customtkinter as ctk 





class ButtonsBar(ctk.CTkFrame): 
    def __init__ (self, parent, col, row):
        super().__init__(parent, fg_color='gray', )
        self.grid(column = col, row = row, sticky = 'nsew')

