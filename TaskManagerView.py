from typing import Optional, Tuple, Union
import customtkinter as ctk
from tkinter import ttk
from PIL import Image
import csv
from AddNewTask import *
from ICommand import Delete
from invoker import Invoker
        
class TaskManagerMain(ctk.CTkFrame):
    def __init__(self, parent, col, row,):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew")
        
        #variables
        self.view_state = "table"
        
        
        #layout
        self.columnconfigure(0, weight=1, uniform='a' )
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=20, uniform="a")
        
        
        #wywołanie widgetów widoku
        self.task_manager_table = TaskManagerTable(self, 0, 1, self)
        self.task_manager_tiles = TaskManagerTiles(self, 0, 1, self)
        self.task_manager_tiles.grid_remove()
        
        TaskManagerButtonBar(self,0,0, self.task_manager_table, self, self.task_manager_tiles)


    def change_view(self):
        if self.view_state == "table":
            self.task_manager_table.grid_remove()
            self.task_manager_tiles.grid() 
            self.view_state = "tiles"
        elif self.view_state == "tiles":
            self.task_manager_tiles.grid_remove()  
            self.task_manager_table.grid()  
            self.view_state = "table"
    
    
    def import_tasks(self):
        task_file = './task_file/tasks.csv'
        data = []
        if os.path.exists(task_file):
            with open(task_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = list(reader)
                file.close()
        return data   
    
    def import_all_status(self):
        status = []
        with open("./task_file/status.csv", 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                status.append(row)
            file.close() 
        return status
            
#klasa tworząca tabele z listą zadań
class TaskManagerTable(ctk.CTkFrame):
    def __init__(self, parent, col, row, main_task_manager_instance):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew")
        self.task_file = './task_file/tasks.csv'
        
        self.invoker = Invoker()
        self.main_task_manager = main_task_manager_instance
        self.create_treeview()
        self.add_to_treeview()

    
    #tworzenie listy dla menadzera zadań
    def create_treeview(self):
        style = ttk.Style()
        style.configure("Treeview",
                        font=('Helvetica', 10),  # ustawienie czcionki
                        foreground="black",  # ustawienie koloru czcionki
                        background="lightblue",  # ustawienie koloru tła
                        fieldbackground="lightblue")  # ustawienie koloru tła dla pól
        style.configure("Treeview.Heading",
                        background="blue",  # ustawienie koloru tła nagłówka
                        foreground="black")  # ustawienie koloru czcionki nagłówka
          
        self.task_list = ttk.Treeview(self)
        self.task_list['columns'] = ('task', 'description', 'deadline', 'status', 'priority','tag')
        self.task_list.column('#0', width=0, stretch='false')
        self.task_list.column('task', width=100)
        self.task_list.column('description', width=200)
        self.task_list.column('deadline',width=80)
        self.task_list.column('status', width=100)
        self.task_list.column('priority',width=100)
        self.task_list.column('tag',width=80)
    
        self.task_list.heading('task', text='Zadanie')
        self.task_list.heading('description', text='Opis')
        self.task_list.heading('deadline', text='Termin')
        self.task_list.heading('status', text='Status')
        self.task_list.heading('priority', text='Priorytet')
        self.task_list.heading('tag', text='Tag')
    
        self.task_list.pack(side='left',expand='true',fill='both')
             
    def add_to_treeview(self):
        #czyszczenie treeview
        for i in self.task_list.get_children():
            self.task_list.delete(i)
        data = self.main_task_manager.import_tasks()
        
        for row in data:
            self.task_list.insert('','end', values=list(row.values()))
 
    
    def remove_selected_task(self):
        selected_task_id = self.task_list.selection()[0]
        self.task_list.delete(selected_task_id)
        data = []
        for item in self.task_list.get_children():
            data.append(self.task_list.item(item)['values'])
        
        task=TaskManager()
        delete_task_command = Delete(task, data)
        self.invoker.set_command(delete_task_command)
        self.invoker.press_button()
        
    

class TaskManagerTiles(ctk.CTkFrame):
    def __init__(self, parent, col, row, task_manager_main):
        super().__init__(parent, fg_color='transparent')
        self.grid(column = col, row=row, sticky='nsew')
    
        #instances
        self.task_manager_main = task_manager_main
    
        # self.create_tile()
        self.create_status_frame()
        

    def create_tile(self):
        tile_frame = ctk.CTkFrame(self)
        
        tile_frame.columnconfigure(0, weight=1, uniform="a")
        tile_frame.columnconfigure(1, weight=2, uniform='a')
        tile_frame.rowconfigure(0, weight=1, uniform='a')
        tile_frame.rowconfigure((1,2,3,4,5,6), weight=1, uniform='a')
        
        self.name_font = ctk.CTkFont(family="Abril Fatface", size=20, weight="bold")
        
        title_label = ctk.CTkLabel(tile_frame,
                                    text="Nazwa",
                                    font=self.name_font,
                                    corner_radius=5,
                                    fg_color=ENTRY_FG,
                                    )  
        title_label.grid(row=0, column=0, columnspan = 2, sticky='nsew', pady=2)
        
        self.create_labels(parent=tile_frame, col=0, row=1, text="Opis zadania")

        self.create_labels(parent=tile_frame, col=0, row=3, text='Termin')

        self.create_labels(parent=tile_frame, col=0, row=2, text="Status")

        self.create_labels(parent=tile_frame, col=0, row=4, text="Priotytet")

        self.create_labels(parent=tile_frame, col=0, row=5, text="Tag")
        
        self.create_labels(parent=tile_frame, col=1, row=1, text="Opis zadania")

        self.create_labels(parent=tile_frame, col=1, row=3, text='Termin')

        self.create_labels(parent=tile_frame, col=1, row=2, text="Status")

        self.create_labels(parent=tile_frame, col=1, row=4, text="Priotytet")

        self.create_labels(parent=tile_frame, col=1, row=5, text="Tag")

        
        
        tile_frame.pack()

    def create_labels(self, parent, col, row, text):
        ctk.CTkLabel(parent,
                     text=text,
                     anchor='center',
                     corner_radius=5, 
                     fg_color=LABEL_FG,
                     text_color=LABEL_TEXT,
                     ).grid(column=col, row=row, sticky='nsew', pady=2, padx=2)
    
    def create_status_frame(self):
        status = self.task_manager_main.import_all_status()
        for i in status:
            status_frame = ctk.CTkFrame(self)
            ctk.CTkLabel(status_frame, text=i[0]).pack()
            status_frame.pack(side='left', expand ='true', fill="both", padx=3)
        
#klasa tworząca pasek z przyciskami
class TaskManagerButtonBar(ctk.CTkFrame):
    def __init__(self, parent, col, row, task_manager_table, task_manager_main, task_manager_tiles):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew")
        
        #instances
        self.parent = parent
        self.toplevel_window = None
        self.task_manager_table = task_manager_table
        self.task_manager_main = task_manager_main
        self.task_manager_tiles = task_manager_tiles
        
        #layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=2, uniform='a')
        self.columnconfigure(10, weight=1, uniform='a')
        
        #add images - zmienic na ctkimage
        refresh_image = ctk.CTkImage(dark_image= Image.open("./button_image/refresh.png"),
                                     light_image= Image.open("./button_image/refresh.png"))
        
        ####buttons#####
        #new task button - open new window
        self.new_task_button =self.create_button(text = "Nowy", row=0,column=0, command=self.open_new_task_window, image=None)

        #delete task button 
        self.delete_button =self.create_button(text="Usuń", row=0,column=1, command=self.delete_task_button_click, image=None)
        
        #status selection
        self.selection_button = self.create_button(text='Status', row=0, column=9, command=self.status_selection_button_click, image=None)
        # change view 
        self.change_view_button =self.create_button(text ='', row=0, column=10, command=self.change_view_button_click, image=refresh_image)
           
    #create button
    def create_button(self, text, row, column, command, image):
        button = ctk.CTkButton(self, 
                      text = text,
                      command=command,
                      image=image
                      )
        button.grid(row = row, 
                    column=column, 
                    sticky ='nsew',
                    padx =2
                    )
        return button
    
    #obsługa przycisków           
    def open_new_task_window(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = NewTaskWindow(self.parent, self.task_manager_table)
        else:
            self.toplevel_window.focus()

    def delete_task_button_click(self):
        self.task_manager_table.remove_selected_task()
    
    def change_view_button_click(self):
        self.task_manager_main.change_view()
    
    def status_selection_button_click(self):
        self.status_top = ctk.CTkToplevel(self.task_manager_main)
        x_pos = self.selection_button.winfo_rootx()
        y_pos = self.selection_button.winfo_rooty()
        self.status_top.geometry(f"+{x_pos}+{y_pos}")
        self.status_top.lift(self.parent)
        self.status_top.overrideredirect(True)
        self.status_top.transient(self)
        
        status = self.task_manager_main.import_all_status()
        
        print(status)
        #bind
        self.status_top.bind("<Leave>", self.close_top)
        
        for i in status:
            self.checkbox = ctk.CTkCheckBox(self.status_top, text=i[0]).pack(expand='true', fill='x')
        
        
        

    def close_top(self, event):
        self.status_top.after(10, self.check_cursor_position(self.status_top))

    def check_cursor_position(self, widget):
        widget=widget
    # Pobierz aktualne współrzędne i wymiary okna
        x = widget.winfo_x()
        y = widget.winfo_y()
        width = widget.winfo_width()
        height = widget.winfo_height()

        # Pobierz aktualne współrzędne kursora myszy
        mouse_x = widget.winfo_pointerx()
        mouse_y = widget.winfo_pointery()

        # Sprawdź, czy kursor myszy jest wewnątrz okna
        if not (x <= mouse_x <= x + width and y <= mouse_y <= y + height):
            # Jeżeli kursor myszy jest poza oknem, zniszcz okno
            widget.destroy()