from typing import Optional, Tuple, Union
import customtkinter as ctk



#główne okno listy zadań 
class TaskManagerMain(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew")
        
        
        #layout
        self.columnconfigure(0, weight=1, uniform='a' )
        self.rowconfigure(0, weight=2, uniform="a")
        self.rowconfigure(1, weight=20, uniform="a")
        
        
        #wywołanie widgetów widoku
        TaskManagerTable(self, 0, 1)
        TaskManagerButtonBar(self,0,0)




#klasa tworząca tabele z listą zadań
class TaskManagerTable(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="blue")
        self.grid(column = col, row=row, sticky = "nsew")
        
        
        
    

#klasa tworząca pasek z przyciskami
class TaskManagerButtonBar(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="yellow")
        self.grid(column = col, row=row, sticky = "nsew")
    
