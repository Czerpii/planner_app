from typing import Optional, Tuple, Union
import customtkinter as ctk
from tkinter import ttk
from ICommand import CreateNewTask
from task_manager_reciver import *
from invoker import Invoker



#główne okno listy zadań 
class TaskManagerMain(ctk.CTkFrame):
    def __init__(self, parent, col, row,):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew")
        
        
        #layout
        self.columnconfigure(0, weight=1, uniform='a' )
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=20, uniform="a")
        
        
        #wywołanie widgetów widoku
        TaskManagerTable(self, 0, 1)
        TaskManagerButtonBar(self,0,0)




#klasa tworząca tabele z listą zadań
class TaskManagerTable(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew")
        
        self.create_treeview()
        
    
    #tworzenie listy dla menadzera zadań
    def create_treeview(self):
        
        #tworzenie kolumn
        columns = ('task', 'deadline', 'priority')
        
        
        treeview = ttk.Treeview(self, columns = columns, show = 'headings')
        
        #tworzenie nagłówków
        treeview.heading('task', text='Zadanie')
        treeview.heading('deadline', text='Termin wykonania')
        treeview.heading('priority', text='Piorytet')
        
        
        
        treeview.pack(fill='both', expand='true')   
    

#klasa tworząca pasek z przyciskami
class TaskManagerButtonBar(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew")
        self.invoker = Invoker()
        self.parent = parent
        
        #layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1, uniform='a')
        
        
        #create buttons
        self.create_button(text = "Nowy", row=0,column=0, command=self.new_task_button_click)
        self.create_button(text = "Usuń", row=0,column=1, command=self.test)



    def create_button(self, text, row, column, command):
        
        ctk.CTkButton(self, 
                      text = text,
                      command=command
                      ).grid(row = row, 
                             column=column, 
                             sticky ='nsew',
                             padx =2
                             )
                      
    def new_task_button_click(self):
        task = TaskManager()
        new_task_command = CreateNewTask(task, self.parent)
        self.invoker.set_command(new_task_command)
        self.invoker.press_button()
        
    def test(self):
        window = ctk.CTkToplevel(self)
        window.geometry("300x400+500+200")
        window.transient(self)
        
        
