from typing import Optional, Tuple, Union
import customtkinter as ctk
from tkinter import ttk
from PIL import Image
import csv
from AddNewTask import *
from ICommand import Delete
from invoker import Invoker
from EditCurrentTask import *      
###colors### 
#tiles
FRAME_TILES = "#1b2127"
TILES = "#303742"
TILES_HOVER = "#6e737b"

#priority color
HIGH_PRIORITY = '#a90205'
MEDIUM_PRIORITY = '#e6b41d' 
LOW_PRIORITY = '#8d9214'
     
class TaskManagerMain(ctk.CTkFrame):
    def __init__(self, parent, col, row,):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew")
        
        #variables
        self.view_state = "table"
        self.status_var_not_started = ctk.BooleanVar(value='True')
        self.status_var_in_progress = ctk.BooleanVar(value='True')
        self.status_var_end = ctk.BooleanVar(value='True')
        self.status_var_archived = ctk.BooleanVar(value='True')
        
        
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
        self.task_manager_main = main_task_manager_instance
        self.create_treeview()
        self.add_to_treeview()
        
        self.task_list.bind("<Double-1>", self.open_editor)
        
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
        self.task_list['columns'] = ('id','title', 'description', 'deadline', 'status', 'priority','tag')
        
        self.task_list.column('#0', width=0, stretch=False)
        self.task_list.column('id', width=0, stretch=False)
        self.task_list.column('title', width=100,)
        self.task_list.column('description', width=200,)
        self.task_list.column('deadline',width=80,)
        self.task_list.column('status', width=100,)
        self.task_list.column('priority',width=100,)
        self.task_list.column('tag',width=80,)
     
    
        self.task_list.heading('title', text='Zadanie')
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
        data = self.task_manager_main.import_tasks()
        
        for row in data:
            self.task_list.insert('','end', values=list(row.values()), iid=row['id'])
    
    def delete_selected_task(self):
        selected_task_id = self.task_list.selection()[0]
        self.task_list.delete(selected_task_id)
              
    def open_editor(self, event):
        self.selected_item_id = self.task_list.selection()[0]
        if self.selected_item_id:
            item = self.selected_item_id
            values = self.task_list.item(item, "values")
            keys = self.task_list["columns"]
            selected_dictionary = dict(zip(keys, values))
            EditTaskWindow(self,
                           self,
                           self.task_manager_main.task_manager_tiles,
                           selected_dictionary,
                           self.selected_item_id)
            
    def edit_choosen_task(self, item_id, **values):
        values_list = list(values.values())
        self.task_list.item(item_id, values=values_list)
    
    def on_select(self):
        task_id = self.task_list.selection()[0]
        return task_id 
    
class TaskManagerTiles(ctk.CTkFrame):
    def __init__(self, parent, col, row, task_manager_main):
        super().__init__(parent, fg_color='transparent')
        self.grid(column = col, row=row, sticky='nsew')
    
        #instances
        self.task_manager_main = task_manager_main
        
        #tiles storage
        self.tiles = {}

        # self.create_tile()
        self.create_status_frame()
        self.create_tiles()
           
    def create_tiles(self):
       
        data_dict = self.task_manager_main.import_tasks()
        item_amount = len(data_dict)
        status_to_frame = {
            'Nie rozpoczęto': self.status_frame_not_started,
            'W trakcie': self.status_frame_in_progress,
            'Zakończony': self.status_frame_end,
            'Zarchiwizowane': self.status_frame_archived
        }

        priority_to_color = {
            'Wysoki': HIGH_PRIORITY,
            'Średni': MEDIUM_PRIORITY,
            'Niski': LOW_PRIORITY
        }

        for item in data_dict:
            parent = status_to_frame.get(item['status'], None)
            color = priority_to_color.get(item['priority'], None)
            if parent:  # Sprawdź, czy znaleziono odpowiednią ramkę
                tile = TilesCreator(parent, self, item['title'], item['priority'], item['deadline'], color, item['id'])
                self.tiles[item['id']] = tile
                
    def new_task_tile(self, title, status, priority, deadline, id_task):
        status_to_frame = {
            'Nie rozpoczęto': self.status_frame_not_started,
            'W trakcie': self.status_frame_in_progress,
            'Zakończony': self.status_frame_end,
            'Zarchiwizowane': self.status_frame_archived
        }

        priority_to_color = {
            'Wysoki': HIGH_PRIORITY,
            'Średni': MEDIUM_PRIORITY,
            'Niski': LOW_PRIORITY
        }
        
        parent = status_to_frame[status]
        try:
            color = priority_to_color[priority]
        except:
            color = TILES
        
        tile = TilesCreator(parent,self,title, priority, deadline, color, id_task)
        self.tiles[str(id_task)] = tile
             
    def create_status_frame(self):
        self.status_frame_not_started = ctk.CTkScrollableFrame(self, fg_color=FRAME_TILES)
        ctk.CTkLabel(self.status_frame_not_started, text="Nie rozpoczęte").pack()
        self.status_frame_not_started.pack(side='left', expand ='true', fill="both", padx=3)
        
        
        self.status_frame_in_progress = ctk.CTkScrollableFrame(self, fg_color=FRAME_TILES)
        ctk.CTkLabel(self.status_frame_in_progress, text="W trakcie").pack()
        self.status_frame_in_progress.pack(side='left', expand ='true', fill="both", padx=3)
        
        
        self.status_frame_end = ctk.CTkScrollableFrame(self, fg_color=FRAME_TILES)
        ctk.CTkLabel(self.status_frame_end, text="Zakończone").pack()
        self.status_frame_end.pack(side='left', expand ='true', fill="both", padx=3)
        
        
        self.status_frame_archived = ctk.CTkScrollableFrame(self, fg_color=FRAME_TILES)
        ctk.CTkLabel(self.status_frame_archived, text="Zarchiwizowane").pack()
        self.status_frame_archived.pack(side='left', expand ='true', fill="both", padx=3)
       
    def create_frame(self, frame, status): #ukrywania i pokazywanie ramki z statusami za pomocą checkboxa
        status = status.get()
        frame = frame
        if status == True:
            frame.pack(side='left', expand ='true', fill="both", padx=3)   
        else: 
            frame.pack_forget()
            
    def edit_tile(self, id_task, title, priority, due_to, status):
        priority_to_color = {
            'Wysoki': HIGH_PRIORITY,
            'Średni': MEDIUM_PRIORITY,
            'Niski': LOW_PRIORITY
        }
        
        status_to_frame = {
            'Nie rozpoczęto': self.status_frame_not_started,
            'W trakcie': self.status_frame_in_progress,
            'Zakończony': self.status_frame_end,
            'Zarchiwizowane': self.status_frame_archived
        }
        
        parent = status_to_frame[status]
        
        try:
            color = priority_to_color[priority]
        except:
            color = TILES

        tile = self.tiles.get(str(id_task))
        tile.destroy()
        
        tile = TilesCreator(parent,self,title, priority, due_to, color, id_task)
        self.tiles[str(id_task)] = tile
    
    def delete_tile(self, id_task):
        tile = self.tiles.get(id_task)
        if tile:
            tile.destroy()
            del self.tiles[id_task]
       
    def open_editor(self, id_task):
        selected_task = []
        for row in self.task_manager_main.import_tasks():
            if row['id'] == str(id_task):
                selected_task = row     
        
        EditTaskWindow(self,
                       self.task_manager_main.task_manager_table,
                       self,
                       selected_task,
                       id_task)
        
class TilesCreator(ctk.CTkFrame):
    def __init__(self, parent, task_manager_tiles, title_name, priority_name, due_to, color, id_task):
        super().__init__(parent, fg_color=TILES)
        self.pack(side='top', fill='x', pady=5)
        
        self.update_idletasks()
        
        self.parent = parent
        self.columnconfigure((0,1), weight=1, uniform='a')
        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        # self.grid_propagate(False)
        self.task_manager_tiles = task_manager_tiles
        self.id_task_tile = id_task
        
        
        self.name_font = ctk.CTkFont(family="Abril Fatface", size=20, weight="bold")
        
        
        
        self.title_label = ctk.CTkLabel(self, text=title_name,
                                wraplength=self.winfo_width(), 
                                justify='left',
                                font=self.name_font)
        self.title_label.grid(column=0, row=0, columnspan=2, sticky='nw', pady=5, padx=5)
        
        
        self.priority_label = ctk.CTkLabel(self, text=priority_name, fg_color=color, corner_radius=5)
        self.priority_label.grid(column=0, row=1, sticky='nsew', padx=5, pady=2)
        
        self.due_label = ctk.CTkLabel(self, text=due_to)
        self.due_label.grid(column=1, row=1, sticky='nsew', padx=5,pady=2)

        self.priority_list = self.priority_label

        #binds
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Double-1>", self.on_double_click)
        
        self.title_label.bind("<Enter>", self.on_enter)
        self.title_label.bind("<Leave>", self.on_leave)
        self.title_label.bind("<Double-1>", self.on_double_click)
        
        self.priority_label.bind("<Enter>", self.on_enter)
        self.priority_label.bind("<Leave>", self.on_leave)
        self.priority_label.bind("<Button-1>", self.on_click_priority)
        
        self.due_label.bind("<Enter>", self.on_enter)
        self.due_label.bind("<Leave>", self.on_leave)
        self.due_label.bind("<Double-1>", self.on_double_click)
        
    def on_enter(self, event):
        self.configure(fg_color=TILES_HOVER)
    
    def on_leave(self, event):
        self.configure(fg_color=TILES)
        
    def on_click_priority(self, event):
       AddTaskParameters(parent = self, data_name='priority', new_task_window_instance=self)
       
    def on_double_click(self, event):
        self.task_manager_tiles.open_editor(self.id_task_tile)
    
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
        self.invoker = Invoker()
        
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
            self.toplevel_window = NewTaskWindow(self.parent, self.task_manager_table, self.task_manager_tiles)
        else:
            self.toplevel_window.focus()

    def delete_task_button_click(self):
        
        id_task = self.task_manager_table.on_select()
        
        self.task_manager_table.delete_selected_task()
        self.task_manager_tiles.delete_tile(id_task)
        
        data = []
        for item in self.task_manager_table.task_list.get_children():
            data.append(self.task_manager_table.task_list.item(item)['values'])
        
        task=TaskManager()
        delete_task_command = Delete(task, data)
        self.invoker.set_command(delete_task_command)
        self.invoker.press_button()
        
        
    
    def change_view_button_click(self):
        self.task_manager_main.change_view()
    
    def status_selection_button_click(self):
        
        status = self.task_manager_main.import_all_status()
        
        self.status_top = ctk.CTkToplevel(self.task_manager_main)
        x_pos = self.selection_button.winfo_rootx()
        y_pos = self.selection_button.winfo_rooty()
        self.status_top.geometry(f"+{x_pos}+{y_pos}")
        self.status_top.lift(self.parent)
        self.status_top.overrideredirect(True)
        self.status_top.transient(self)
        
        self.status_top.bind("<Leave>", self.close_top)
        
        self.checkbox_1 = ctk.CTkCheckBox(self.status_top,
                                          text=status[0][0],
                                          variable = self.task_manager_main.status_var_not_started,
                                          command = lambda: self.task_manager_tiles.create_frame(self.task_manager_tiles.status_frame_not_started,
                                                                                                 self.task_manager_main.status_var_not_started),
                                          onvalue = True,
                                          offvalue = False,
                                          ).pack(expand='true', fill='x')
        self.checkbox_2 = ctk.CTkCheckBox(self.status_top,
                                          text=status[1][0],
                                          variable = self.task_manager_main.status_var_in_progress,
                                          command = lambda: self.task_manager_tiles.create_frame(self.task_manager_tiles.status_frame_in_progress,
                                                                                                 self.task_manager_main.status_var_in_progress),
                                          ).pack(expand='true', fill='x')
        self.checkbox_3 = ctk.CTkCheckBox(self.status_top,
                                          text=status[2][0],
                                          variable = self.task_manager_main.status_var_end,
                                          command = lambda: self.task_manager_tiles.create_frame(self.task_manager_tiles.status_frame_end,
                                                                                                 self.task_manager_main.status_var_end),
                                          ).pack(expand='true', fill='x')
        self.checkbox_4 = ctk.CTkCheckBox(self.status_top,
                                          text=status[3][0],
                                          variable = self.task_manager_main.status_var_archived,
                                          command = lambda: self.task_manager_tiles.create_frame(self.task_manager_tiles.status_frame_archived,
                                                                                                 self.task_manager_main.status_var_archived),
                                          ).pack(expand='true', fill='x')
        
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