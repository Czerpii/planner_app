from typing import Optional, Tuple, Union
import customtkinter as ctk
from tkinter import ttk
from tkinter import PhotoImage
from ICommand import Save
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
        
        columns = ('task','description','deadline', 'status', 'priority', 'tag')
        treeview = ttk.Treeview(self, columns = columns, show = 'headings')
        
        #tworzenie nagłówków
        
        treeview.heading('task', text='Zadanie')
        treeview.heading('description', text='Opis')
        treeview.heading('deadline', text='Termin wykonania')
        treeview.heading('status', text ='Status')
        treeview.heading('priority', text='Piorytet')
        treeview.heading('tag', text='Tag')
        
        
        treeview.pack(side='left',expand='true', fill='both')   
        
    

#klasa tworząca pasek z przyciskami
class TaskManagerButtonBar(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew")
        self.invoker = Invoker()
        self.parent = parent
        
        self.toplevel_window = None
        
        #layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=2, uniform='a')
        self.columnconfigure(10, weight=1, uniform='a')
        
        #add images
        refresh_image = PhotoImage(file= "./button_image/refresh.png")
        
        ####buttons#####
        
        #new task button - open new window
        self.create_button(text = "Nowy", row=0,column=0, command=self.open_new_task_window, image=None)
    
        #refresh button - refresh all task 
        self.create_button(text ='', row=0, column=10, command=None, image=refresh_image)
        
        
    #create button
    def create_button(self, text, row, column, command, image):
        
        ctk.CTkButton(self, 
                      text = text,
                      command=command,
                      image=image
                      ).grid(row = row, 
                             column=column, 
                             sticky ='nsew',
                             padx =2
                             )
    
    #open widnow to add new task            
    def open_new_task_window(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = NewTaskWindow(self.parent)
        else:
            self.toplevel_window.focus()
       
                       

 
class NewTaskWindow(ctk.CTkToplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("300x400+700+350")
        self.maxsize(300, 400)
        self.minsize(300, 400)
        self.transient(parent)
        self.title("Nowe zadanie")
        
        
        self.invoker =Invoker()
        
        #layout
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=2, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure((1,2,3,4,5,6), weight=1, uniform='a')
        
        #fonts
        self.name_font = ctk.CTkFont(family="Abril Fatface", size=30, weight="bold")
        
        #title frame and title entry
        self.title_frame = ctk.CTkFrame(self, border_width=0, fg_color='transparent')
        self.title_frame.grid(row=0, column=0, columnspan = 2, sticky='nsew')
        
        self.title_entry = ctk.CTkEntry(self.title_frame,
                                        placeholder_text="Nazwa",
                                        font=self.name_font,
                                        corner_radius=10,
                                        fg_color='transparent',
                                        border_width=0
                                        )
        self.title_entry.pack(fill = "both", expand = True, side = "top")    
        
        
        #description textbox
        self.desc_label = ctk.CTkLabel(self, text="Opis zadania")
        self.desc_label.grid(column = 0, row = 1, sticky = "w", padx=2)
        
        self.desc_textbox = ctk.CTkTextbox(self)
        self.desc_textbox.grid(column=1, row=1, sticky="nsew")
        
        
        #status dropbox
        self.status_label = ctk.CTkLabel(self, text="Status")
        self.status_label.grid(column=0, row=2, sticky='w')
        
        self.status_list = ctk.CTkComboBox(self, values=['option1'])
        self.status_list.grid(column=1, row=2, sticky="ew")
        
        #deadline entry
        self.date_label = ctk.CTkLabel(self, text="Data wykonania")
        self.date_label.grid(column=0, row=3, sticky='w')
        
        self.date_frame_entry = ctk.CTkFrame(self, border_width=0, fg_color='transparent')
        self.date_frame_entry.grid(column=1, row=3, sticky='nsew')
        
        self.date_entry = ctk.CTkEntry(self.date_frame_entry)
        self.date_entry.pack(side = 'left', expand = "true", fill ="x")
        
        self.date_button = ctk.CTkButton(self.date_frame_entry, text=" ", width=25)
        self.date_button.pack(side ='left')
        
        
        #priority list
        self.priority_label = ctk.CTkLabel(self, text="Priorytet")
        self.priority_label.grid(column=0, row=4, sticky='w')
        
        self.priority_list = ctk.CTkComboBox(self, values=['option1'])
        self.priority_list.grid(column=1, row=4, sticky="ew")
        
        #tag list
        self.tag_label = ctk.CTkLabel(self, text="Tag")
        self.tag_label.grid(column=0, row=5, sticky='w')
        
        self.tag_list = ctk.CTkComboBox(self, values=['option1'])
        self.tag_list.grid(column=1, row=5, sticky="ew")
        
        
        #buttons - add save and cancel button
        self.buttons_frame = ctk.CTkFrame(self, border_width=0, fg_color='transparent')
        self.buttons_frame.grid(column=0, row=6, columnspan =2, sticky='nsew')
        
        self.save_button = ctk.CTkButton(self.buttons_frame, text="Zapisz", command=self.save_task_button_click)
        self.save_button.pack(side='left', padx=4, fill='x', expand='true')
        self.cancel_button = ctk.CTkButton(self.buttons_frame, text="Anuluj")
        self.cancel_button.pack(side='left', padx=4, fill='x', expand='true')

        

    def save_task_button_click(self):
        
      
        task = TaskManager()
        save_task_command = Save(task,
                                 title=self.title_entry.get(),
                                 description=self.desc_textbox.get(index1="0.0",index2="end"),
                                 deadline=self.date_entry.get(),
                                 status=self.status_list.get(),
                                 priority=self.priority_list.get(), 
                                 tag=self.tag_list.get())
        self.invoker.set_command(save_task_command)
        self.invoker.press_button()