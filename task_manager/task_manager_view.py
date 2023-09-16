
from typing import Optional, Tuple, Union
import os
import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from .task_window import TaskWindow
from .task_manager_reciver import TaskManager
from ICommand import Delete
from invoker import Invoker
from UserSingleton import *
import themes_manager
    

#priority color
HIGH_PRIORITY = '#a90205'
MEDIUM_PRIORITY = '#e6b41d' 
LOW_PRIORITY = '#8d9214'
     
class TaskManagerMain(ctk.CTkFrame):
    def __init__(self, parent, col, row,):
        super().__init__(parent, fg_color='transparent', corner_radius=0, border_width=0)
        self.grid(column = col, row=row, sticky = "nsew")

        self.initialize_variables()
        self.configure_layout()
        self.initialize_widgets()

    def initialize_variables(self):
        self.view_state = "table"
        self.status_var_not_started = ctk.BooleanVar(value='True')
        self.status_var_in_progress = ctk.BooleanVar(value='True')
        self.status_var_end = ctk.BooleanVar(value='True')
        self.status_var_archived = ctk.BooleanVar(value='True')

    def configure_layout(self):
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=20, uniform="a")

    def initialize_widgets(self):
        self.task_reciver = TaskManager()
        self.task_manager_table = TaskManagerTable(self, 0, 1, self)
        self.task_manager_tiles = TaskManagerTiles(self, 0, 1, self)
        self.task_manager_tiles.grid_remove()
        TaskManagerButtonBar(self, 0, 0, self.task_manager_table, self, self.task_manager_tiles)

    def change_view(self):
        if self.view_state == "table":
            self.task_manager_table.grid_remove()
            self.task_manager_tiles.grid() 
            self.view_state = "tiles"
        elif self.view_state == "tiles":
            self.task_manager_tiles.grid_remove()  
            self.task_manager_table.grid()  
            self.view_state = "table"
    
class TaskManagerTable(ctk.CTkFrame):
    """
    A class representing the table view of the Task Manager.
    """
    def __init__(self, parent, col, row, main_task_manager_instance):
        """
        Initializes a TaskManagerTable instance.

        Args:
            parent: The parent widget.
            col: The column to place the widget in.
            row: The row to place the widget in.
            main_task_manager_instance: The main TaskManager instance.
        """
        super().__init__(parent, fg_color="transparent", corner_radius=10)
        self.grid(column=col, row=row, sticky="nsew", padx=5, pady=5)
        
        self.initialize_variables(main_task_manager_instance)
        self.create_treeview()
        self.populate_treeview()
        self.bind_events()

    def initialize_variables(self, main_task_manager_instance):
        """
        Initializes the class variables.

        Args:
            main_task_manager_instance: The main TaskManager instance.
        """
        self.invoker = Invoker()
        self.task_manager_main = main_task_manager_instance

    def create_treeview(self):
        """
        Creates the Treeview widget for displaying tasks.
        """
        self.configure_treeview_style()
        self.task_list = ttk.Treeview(self, columns=('id', 'title', 'description', 'start', 'end', 'status', 'priority', 'tag'))
        self.configure_treeview_columns()
        self.configure_treeview_headings()
        self.task_list.pack(side='left', expand='true', fill='both')

    def configure_treeview_style(self):
        """
        Configures the style of the Treeview widget.
        """
        style = ttk.Style()
        
       
        style.layout('Treeview.Heading', [
            ('Treeview.Heading.cell', {'sticky': 'nswe'}),
            ('Treeview.Heading.border', {'sticky': 'nswe', 'children': [
                ('Treeview.Heading.padding', {'sticky': 'nswe', 'children': [
                    ('Treeview.Heading.image', {'side': 'right', 'sticky': ''}),
                    ('Treeview.Heading.text', {'sticky': 'w'})
                ]})
            ]})
        ])
        
      
        style.configure("Treeview", font=('San Francisco', 10), foreground="white", 
                        background=themes_manager.get_color("background"), 
                        fieldbackground=themes_manager.get_color("background"),
                        lineseparatorcolor = themes_manager.get_color('border_entry'),
                        
                        rowheight=50)
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) 
        
        style.configure('Treeview.Heading', 
                        font=('San Francisco', 12, 'bold'),
                        background = themes_manager.get_color("fg_frame"),
                        foreground='white', 
                        relief='flat')
        
        style.map('Treeview',
          background=[('selected', themes_manager.get_color('fg_frame'))],  # 'red' to kolor podświetlenia
          foreground=[('selected', 'white')]  # 'white' to kolor tekstu dla zaznaczonego wiersza
          )

    def configure_treeview_columns(self):
        """
        Configures the columns of the Treeview widget.
        """
        self.task_list.column('#0', width=0, stretch=False)
        self.task_list.column('id', width=0, stretch=False)
        self.task_list.column('title', width=100)
        self.task_list.column('description', width=150)
        self.task_list.column('start', width=100)
        self.task_list.column('end', width=100)
        self.task_list.column('status', width=100)
        self.task_list.column('priority', width=80)
        self.task_list.column('tag', width=50)

    def configure_treeview_headings(self):
        """
        Configures the headings of the Treeview widget.
        """
        self.task_list.heading('title', text='Zadanie')
        self.task_list.heading('description', text='Opis')
        self.task_list.heading('start', text='Rozpoczęcie')
        self.task_list.heading('end', text = 'Zakończenie')
        self.task_list.heading('status', text='Status')
        self.task_list.heading('priority', text='Priorytet')
        self.task_list.heading('tag', text='Tag')

    def populate_treeview(self):
        """
        Populates the Treeview widget with task data.
        """
        for i in self.task_list.get_children():
            self.task_list.delete(i)
        data = self.task_manager_main.task_reciver.import_tasks()
        for row in data:
            self.task_list.insert('', 'end', values=list(row.values()), iid=row['id'])

    def bind_events(self):
        """
        Binds events to the Treeview widget.
        """
        self.task_list.bind("<Double-1>", self.open_editor_event)

    def delete_selected_task(self, id_task):
        """
        Deletes the selected task from the Treeview.

        Args:
            id_task: The ID of the task to delete.
        """
        self.task_list.delete(id_task)

    def open_editor_event(self, event):
        """
        Opens the task editor when a task is double-clicked.

        Args:
            event: The event object.
        """
        self.open_editor()
    
    def open_editor(self):
        """
        Opens the task editor for the selected task.
        """
        selected_item_id = self.task_list.selection()[0]
        if selected_item_id:
            values = self.task_list.item(selected_item_id, "values")
            keys = self.task_list["columns"]
            selected_dictionary = dict(zip(keys, values))
            TaskWindow(self, self, self.task_manager_main.task_manager_tiles, selected_dictionary, selected_item_id).setup_ui_elements_for_existed_task()
            
    def edit_chosen_task(self, item_id, **values):
        """
        Edits the chosen task with new values.

        Args:
            item_id: The ID of the task to edit.
            values: New values for the task.
        """
        values_list = list(values.values())
        self.task_list.item(item_id, values=values_list)

    def on_select(self):
        """
        Returns the ID of the selected task.

        Returns:
            str: The ID of the selected task.
        """
        return self.task_list.selection()[0]
      
class TaskManagerTiles(ctk.CTkFrame):
    """
    A class representing the tiles view of the Task Manager.
    """
    
    def __init__(self, parent, col, row, task_manager_main):
        """
        Initializes a TaskManagerTiles instance.

        Args:
            parent: The parent widget.
            col: The column to place the widget in.
            row: The row to place the widget in.
            task_manager_main: The main TaskManager instance.
        """
        super().__init__(parent, fg_color='transparent')
        self.grid(column = col, row=row, sticky='nsew')
    
        #instances
        self.task_manager_main = task_manager_main
        self.selected_tile_id = None
        #tiles storage
        self.tiles = {}

        # self.create_tile()
        self.create_status_frame()
        self.create_tiles()
           
    def create_tiles(self):
        """
        Creates and populates tiles for tasks.
        """
       
        data_dict = self.task_manager_main.task_reciver.import_tasks()
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
                tile = TilesCreator(parent, self, item['title'], item['priority'], color, item['id'])
                self.tiles[item['id']] = tile
                
    def new_task_tile(self, title, status, priority, id_task):
        """
        Creates a new tile for a task.

        Args:
            title: The title of the task.
            status: The status of the task.
            priority: The priority of the task.
            id_task: The ID of the task.
        """
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
            color = None
        
        tile = TilesCreator(parent,self,title, priority, color, id_task)
        self.tiles[str(id_task)] = tile
             
    def create_scrollable_frame(self, text):
        """
        Creates a scrollable frame with a label.

        Args:
            text: The text for the label.

        Returns:
            ctk.CTkScrollableFrame: The created scrollable frame.
        """
        frame = ctk.CTkScrollableFrame(self,
                                       fg_color=themes_manager.get_color('fg_frame'),
                                       scrollbar_button_color=themes_manager.get_color('scrollbar'),
                                       scrollbar_button_hover_color=themes_manager.get_color('scrollbar_hover'))
        ctk.CTkLabel(frame,
                     text=text,
                     font = themes_manager.get_ctk_font('default_bold')).pack()
        frame.pack(side='left', expand='true', fill="both", padx=3)
        return frame

    def create_status_frame(self):
        """
        Creates status frames for different task statuses.
        """
        self.status_frame_not_started = self.create_scrollable_frame("Nie rozpoczęte")
        self.status_frame_in_progress = self.create_scrollable_frame("W trakcie")
        self.status_frame_end = self.create_scrollable_frame("Zakończone")
        self.status_frame_archived = self.create_scrollable_frame("Zarchiwizowane")
      
    def create_frame(self, frame, status): 
        """
        Creates a frame based on the given status.

        Args:
            frame: The frame to create.
            status: The status of the frame.
        """
        status = status.get()
        frame = frame
        if status == True:
            frame.pack(side='left', expand ='true', fill="both", padx=3)   
        else: 
            frame.pack_forget()
            
    def edit_tile(self, id_task, title, priority, status):
        """
        Edits a tile for a task.

        Args:
            id_task: The ID of the task.
            title: The new title of the task.
            priority: The new priority of the task.
            status: The new status of the task.
        """
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
            color = None

        tile = self.tiles.get(str(id_task))
        tile.destroy()
        
        
        tile = TilesCreator(parent,self,title, priority, color, id_task)
        self.tiles[str(id_task)] = tile
    
    def delete_tile(self, id_task):
        """
        Deletes a tile for a task.

        Args:
            id_task: The ID of the task.
        """
        tile = self.tiles.get(str(id_task))
        if tile:
            tile.destroy()
            del self.tiles[str(id_task)]
       
    def open_editor(self, id_task):
        """
        Opens the task editor for a selected task.

        Args:
            id_task: The ID of the selected task.
        """
        selected_task = []
        for row in self.task_manager_main.task_reciver.import_tasks():
            if row['id'] == str(id_task):
                selected_task = row     
        
        TaskWindow(self,
                       self.task_manager_main.task_manager_table,
                       self,
                       selected_task,
                       id_task).setup_ui_elements_for_existed_task()
    
    def on_select(self):
        """
        Returns the ID of the selected tile.

        Returns:
            str: The ID of the selected tile.
        """
        return self.selected_tile_id          
        

class TilesCreator(ctk.CTkFrame):
    """
    A class for creating task tiles in the TaskManagerTiles view.
    """

    def __init__(self, parent, task_manager_tiles, title_name, priority_name, color, id_task):
        """
        Initializes a TilesCreator instance.

        Args:
            parent: The parent widget.
            task_manager_tiles: The parent TaskManagerTiles instance.
            title_name: The title of the task.
            priority_name: The priority of the task.
            color: The color associated with the priority.
            id_task: The ID of the task.
        """
        super().__init__(parent, fg_color=themes_manager.get_color('tile'))
        self.pack(side='bottom', fill='x', pady=5)

        self.update_idletasks()

        self.parent = parent
        self.columnconfigure((0, 1), weight=1, uniform='a')
        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.task_manager_tiles = task_manager_tiles
        self.id_task_tile = id_task

        # Title label
        self.title_label = ctk.CTkLabel(self, text=title_name,
                                        wraplength=self.winfo_width(),
                                        justify='left',
                                        font=themes_manager.get_ctk_font('small_header'))
        self.title_label.grid(column=0, row=0, columnspan=2, sticky='nw', pady=5, padx=5)

        # Priority label
        self.priority_label = ctk.CTkLabel(self, text=priority_name, fg_color=color, corner_radius=5)
        self.priority_label.grid(column=0, row=1, sticky='nsew', padx=5, pady=2)
        self.priority_label.grid_propagate("false")

        # Binds
        self.bind("<Double-1>", self.on_double_click)
        self.bind("<Button-1>", self.on_click)
        self.title_label.bind("<Double-1>", self.on_double_click)
        self.title_label.bind("<Button-1>", self.on_click)
        self.priority_label.bind("<Double-1>", self.on_double_click)
        self.priority_label.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        """
        Event handler for mouse entering the tile. Changes the foreground color.
        """
        self.configure(fg_color=themes_manager.get_color('tile_hover'))

    def on_leave(self, event):
        """
        Event handler for mouse leaving the tile. Resets the foreground color.
        """
        self.configure(fg_color=themes_manager.get_color('tile'))

    def on_double_click(self, event):
        """
        Event handler for double-clicking the tile. Opens the task editor.
        """
        self.task_manager_tiles.open_editor(self.id_task_tile)
        self.configure(fg_color=themes_manager.get_color('tile'))
        self.task_manager_tiles.selected_tile_id = None

    def on_click(self, event):
        """
        Event handler for clicking the tile. Handles tile selection.
        """
        if self.task_manager_tiles.selected_tile_id is not None:
            previous_tile = self.task_manager_tiles.tiles.get(str(self.task_manager_tiles.selected_tile_id))
            if previous_tile:
                previous_tile.configure(fg_color=themes_manager.get_color('tile'))

        self.configure(fg_color=themes_manager.get_color('tile_hover'))
        self.task_manager_tiles.selected_tile_id = self.id_task_tile


class TaskManagerButtonBar(ctk.CTkFrame):
    """
    A class representing the button bar in the TaskManager application.
    """

    def __init__(self, parent, col, row, task_manager_table, task_manager_main, task_manager_tiles):
        """
        Initializes a TaskManagerButtonBar instance.

        Args:
            parent: The parent widget.
            col: The column in which to place the button bar.
            row: The row in which to place the button bar.
            task_manager_table: The TaskManagerTable instance.
            task_manager_main: The main TaskManager instance.
            task_manager_tiles: The TaskManagerTiles instance.
        """
        super().__init__(parent, fg_color="transparent", corner_radius=0, border_width=0)
        self.grid(column=col, row=row, sticky="nsew")

        # Instances
        self.parent = parent
        self.toplevel_window = None
        self.task_manager_table = task_manager_table
        self.task_manager_main = task_manager_main
        self.task_manager_tiles = task_manager_tiles
        self.invoker = Invoker()

        # Layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=2, uniform='a')
        self.columnconfigure(10, weight=1, uniform='a')

        # Add images - change to ctkimage
        current_directory = os.path.dirname(os.path.abspath(__file__))
        change_image_path = os.path.join(current_directory, "../button_image/change.png")
        change_image = ctk.CTkImage(dark_image=Image.open(change_image_path),
                                    light_image=Image.open(change_image_path))

        # Buttons
        # New task button - open new window
        self.new_task_button = self.create_button(text="Nowy", row=0, column=0, command=self.open_new_task_window,
                                                  image=None)

        # Edit task button
        self.edit_task_button = self.create_button(text="Edytuj", row=0, column=1, command=self.edit_task_button_click,
                                                  image=None)

        # Delete task button
        self.delete_button = self.create_button(text="Usuń", row=0, column=2, command=self.delete_task_button_click,
                                                image=None)

        # Status selection
        self.selection_button = self.create_button(text='Status', row=0, column=9,
                                                    command=self.status_selection_button_click, image=None)
        self.selection_button.grid_remove()

        # Change view
        self.change_view_button = self.create_button(text='', row=0, column=10, command=self.change_view_button_click,
                                                    image=change_image)

    def create_button(self, text, row, column, command, image):
        """
        Create a button with specified parameters.

        Args:
            text: The text on the button.
            row: The row in which to place the button.
            column: The column in which to place the button.
            command: The command to be executed when the button is clicked.
            image: The image to be displayed on the button.

        Returns:
            The created button.
        """
        button = ctk.CTkButton(self,
                               text=text,
                               font=themes_manager.get_ctk_font("button"),
                               command=command,
                               image=image,
                               fg_color=themes_manager.get_color('button'),
                               hover_color=themes_manager.get_color('button_hover'),
                               )
        button.grid(row=row,
                    column=column,
                    sticky='nsew',
                    padx=2,
                    pady=2
                    )
        return button

    def open_new_task_window(self):
        """
        Open a new task window.
        """
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = TaskWindow(self.parent, self.task_manager_table, self.task_manager_tiles). \
                setup_ui_elements_for_new_task()
        else:
            self.toplevel_window.focus()

        singleton = UserSingleton()

    def edit_task_button_click(self):
        """
        Handle the click of the edit task button.
        """
        if self.task_manager_tiles.on_select() is not None:
            id_task = self.task_manager_tiles.on_select()
        else:
            try:
                id_task = self.task_manager_table.on_select()
            except:
                return

        self.task_manager_tiles.open_editor(id_task)
        self.task_manager_tiles.selected_tile_id = None

    def delete_task_button_click(self):
        """
        Handle the click of the delete task button.
        """
        if self.task_manager_tiles.on_select() is not None:
            id_task = self.task_manager_tiles.on_select()
        else:
            try:
                id_task = self.task_manager_table.on_select()
            except:
                return

        self.task_manager_table.delete_selected_task(id_task)
        self.task_manager_tiles.delete_tile(id_task)
        self.task_manager_tiles.selected_tile_id = None
        data = []
        for item in self.task_manager_table.task_list.get_children():
            data.append(self.task_manager_table.task_list.item(item)['values'])

        task = TaskManager()
        delete_task_command = Delete(task, id_task)
        self.invoker.set_command(delete_task_command)
        self.invoker.press_button()

    def change_view_button_click(self):
        """
        Handle the click of the change view button.
        """
        self.task_manager_main.change_view()
        if self.task_manager_main.view_state == 'table':
            self.selection_button.grid_remove()
        elif self.task_manager_main.view_state == 'tiles':
            self.selection_button.grid(row=0, column=9, sticky='nsew', padx=2)

    def status_selection_button_click(self):
        """
        Handle the click of the status selection button.
        """
        status = self.task_manager_main.task_reciver.import_all_status()

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
                                          variable=self.task_manager_main.status_var_not_started,
                                          command=lambda: self.task_manager_tiles.create_frame(
                                              self.task_manager_tiles.status_frame_not_started,
                                              self.task_manager_main.status_var_not_started),
                                          onvalue=True,
                                          offvalue=False,
                                          ).pack(expand='true', fill='x')
        self.checkbox_2 = ctk.CTkCheckBox(self.status_top,
                                          text=status[1][0],
                                          variable=self.task_manager_main.status_var_in_progress,
                                          command=lambda: self.task_manager_tiles.create_frame(
                                              self.task_manager_tiles.status_frame_in_progress,
                                              self.task_manager_main.status_var_in_progress),
                                          ).pack(expand='true', fill='x')
        self.checkbox_3 = ctk.CTkCheckBox(self.status_top,
                                          text=status[2][0],
                                          variable=self.task_manager_main.status_var_end,
                                          command=lambda: self.task_manager_tiles.create_frame(
                                              self.task_manager_tiles.status_frame_end,
                                              self.task_manager_main.status_var_end),
                                          ).pack(expand='true', fill='x')
        self.checkbox_4 = ctk.CTkCheckBox(self.status_top,
                                          text=status[3][0],
                                          variable=self.task_manager_main.status_var_archived,
                                          command=lambda: self.task_manager_tiles.create_frame(
                                              self.task_manager_tiles.status_frame_archived,
                                              self.task_manager_main.status_var_archived),
                                          ).pack(expand='true', fill='x')

    def close_top(self, event):
        """
        Close the status selection top-level window.
        """
        self.status_top.after(10, self.check_cursor_position(self.status_top))

    def check_cursor_position(self, widget):
        """
        Check the cursor position for closing the top-level window.

        Args:
            widget: The widget to check.
        """
        widget=widget
        x = widget.winfo_x()
        y = widget.winfo_y()
        width = widget.winfo_width()
        height = widget.winfo_height()

        mouse_x = widget.winfo_pointerx()
        mouse_y = widget.winfo_pointery()

        if not (x <= mouse_x <= x + width and y <= mouse_y <= y + height):
            widget.destroy()