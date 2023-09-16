import csv
import os

import random

import customtkinter as ctk

from task_manager.deadline_toplevel import *
from ICommand import Save, Edit
from invoker import Invoker
from task_manager.task_manager_reciver import *
import themes_manager


# FRAMES
FRAME_FG = "#1E1E1E"
FRAME_BORDER = "#282828"




class TaskWindow(ctk.CTkToplevel):
    """
    A window class that provides an interface for creating and editing tasks
    """
    def __init__(self, parent, task_manager_table_instance, task_manager_tiles_instance, task_data=None, selected_item_id=None):
        """Initialez the TaskWindow

        Args:
            parent: Parent window
            task_manager_table_instance: Instance of the task manager table
            task_manager_tiles_instance: Instance of the task manager tiles
            task_data: Data related to a task. Defaults to None. Provide to edit task
            selected_item_id: ID od the selected task. Defaults to None. Provide to edit task
        """
        super().__init__(parent, fg_color=themes_manager.get_color("background"))
        
        
        self.cal_widget = None
        self.parent = parent
        self.button_mode = None
        self.task_data=task_data
        self.selected_item_id=selected_item_id

        self.invoker = Invoker()
        self.task_manager_table_instance = task_manager_table_instance
        self.task_manager_tiles_instance = task_manager_tiles_instance
        self.add_task = AddTaskParameters


        self.setup_window()
        self.configure_layout()
        self.setup_labels()
        self.create_action_buttons(col=0, row=6)
       
    def setup_window(self):
        """Configures the initial window settings, size and position"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - 300 / 2)
        center_y = int(screen_height / 2 - 400 / 2)
        self.geometry(f'300x400+{center_x}+{center_y}')
        self.maxsize(300, 400)
        self.minsize(300, 400)

        self.lift(self.parent)
        self.transient(self.parent)
            
    def configure_layout(self):
        """Configures the grid layout of the window"""
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=2, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure((1, 2, 3, 4, 5, 6), weight=1, uniform='a') 

    def create_labels(self, col, row, text):
        """Create label and place on the windows"""
        ctk.CTkLabel(self,
                     text=text,
                     font = themes_manager.get_ctk_font('default_bold'),
                     anchor='center',
                     corner_radius=5,
                     fg_color=themes_manager.get_color("fg_frame"),
                     ).grid(column=col, row=row, sticky='nsew', pady=2, padx=2)

    def create_title_entry(self, col, row):
        """Creates the title entry widget."""
        self.title_entry = ctk.CTkEntry(self,
                                        placeholder_text="Nazwa",
                                        font=themes_manager.get_ctk_font("header"),
                                        corner_radius=5,
                                        fg_color=themes_manager.get_color("entry"),
                                        border_width=0
                                        )
        self.title_entry.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=2)
        
    def create_description_entry(self, col, row):
        """Creates the description textbox widget."""
        self.desc_textbox = ctk.CTkTextbox(self, 
                                           font = themes_manager.get_ctk_font('entry'),
                                           fg_color=themes_manager.get_color('entry'),
                                           border_color=themes_manager.get_color('border_entry'),
                                           corner_radius=5)
        self.desc_textbox.grid(column=col, row=row, sticky="nsew", pady=2, padx=2)
    
    def create_status_button(self, col, row, text="Nie rozpoczęto"):
        """Creates the status selection button widget."""
        self.status_list = ctk.CTkButton(self,
                                         text=text,
                                         command=self.status_list_button_click,
                                         font=themes_manager.get_ctk_font("entry"),
                                         fg_color=themes_manager.get_color('fg_frame'),
                                         hover_color=themes_manager.get_color('fg_hover_frame'),
                                         corner_radius=5)
        self.status_list.grid(column=col, row=row, sticky="nsew", pady=2, padx=2)
    
    def create_deadline_buttons(self, col, row, text_start="Brak", text_end = "Brak"):
        """Creates the date selection button widget."""
        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.grid(column=col, row=row, sticky='nsew', pady=2, padx=2)
        frame.columnconfigure(0, weight=1, uniform='a')
        frame.rowconfigure((0,1), weight=1, uniform='a')
        frame.grid_propagate(False)
        
        self.start_button = ctk.CTkButton(frame,
                                         text=text_start,
                                         command=lambda: self.open_calendar_button_click(self.start_button),
                                         font=themes_manager.get_ctk_font("entry"),
                                         fg_color=themes_manager.get_color('fg_frame'),
                                         hover_color=themes_manager.get_color('fg_hover_frame'),
                                         corner_radius=5)
        self.start_button.grid(column=0, row=0, sticky='nsew')
        
        self.end_button = ctk.CTkButton(frame,
                                         text=text_end,
                                         command= lambda: self.open_calendar_button_click(self.end_button),
                                         font=themes_manager.get_ctk_font("entry"),
                                         fg_color=themes_manager.get_color('fg_frame'),
                                         hover_color=themes_manager.get_color('fg_hover_frame'),
                                         corner_radius=5)
        self.end_button.grid(column=0, row=1, sticky='nsew')
              
    def create_priority_button(self, col, row, text="Wybierz"):
        """Creates the priority selection button widget."""
        self.priority_list = ctk.CTkButton(self,
                                           text=text,
                                           command=self.priority_list_button_click,
                                           font=themes_manager.get_ctk_font("entry"),
                                           fg_color=themes_manager.get_color('fg_frame'),
                                           hover_color=themes_manager.get_color('fg_hover_frame'),
                                           corner_radius=5)
        self.priority_list.grid(column=col, row=row, sticky="nsew", pady=2, padx=2)
     
    def create_tag_button(self, col, row, text="Wybierz"):
        """Creates the tag selection button widget."""
        self.tag_list = ctk.CTkButton(self,
                                      text=text,
                                      command=self.tag_list_button_click,
                                      font=themes_manager.get_ctk_font("entry"),
                                      fg_color=themes_manager.get_color('fg_frame'),
                                      hover_color=themes_manager.get_color('fg_hover_frame'))
        self.tag_list.grid(column=col, row=row, sticky="nsew", pady=2, padx=2)
    
    def setup_labels(self):
        """Sets up labels for different fields on the window."""
        self.create_labels(col=0, row=1, text="Opis zadania")
        self.create_labels(col=0, row=3, text='Rozpoczęcie\n\nZakończenie')
        self.create_labels(col=0, row=2, text="Status")
        self.create_labels(col=0, row=4, text="Priotytet")
        self.create_labels(col=0, row=5, text="Tag")
     
    def setup_ui_elements_for_new_task(self):
        """Configures the UI elements when creating a new task."""
        self.create_title_entry(col=0, row=0)
        self.create_description_entry(col=1, row=1)
        self.create_status_button(col=1, row=2)
        self.create_deadline_buttons(col=1, row=3)
        self.create_priority_button(col=1, row=4)
        self.create_tag_button(col=1, row=5)
        
        self.button_mode = 'new'
        self.title("Nowe zadanie")
    
    def setup_ui_elements_for_existed_task(self):
        """Configures the UI elements when editing an existing task."""
        self.create_title_entry(col=0, row=0)
        self.title_entry.insert(0, self.task_data['title'])
        
        self.create_description_entry(col=1, row=1)
        self.desc_textbox.delete("0.0", "end")
        self.desc_textbox.insert("0.0", self.task_data['description'])
        
        self.create_status_button(col=1, row=2, text=self.task_data['status'])
        self.create_deadline_buttons(col=1, row=3, text_start=self.task_data['start'], text_end=self.task_data['end'])
        self.create_priority_button(col=1, row=4, text=self.task_data['priority'])
        self.create_tag_button(col=1, row=5, text=self.task_data['tag'])
        
        self.button_mode='edit'
        self.title("Edytuj zadanie")
        
    def create_action_buttons(self, col, row):
        """Creates the save and cancel action buttons."""
        buttons_frame = ctk.CTkFrame(self, border_width=0, fg_color=FRAME_FG)
        buttons_frame.grid(column=col, row=row, columnspan=2, sticky='nsew')

        self.save_button = ctk.CTkButton(buttons_frame,
                                         text="Zapisz",
                                         command=self.save_task_button_click,
                                         font=themes_manager.get_ctk_font("button"),
                                         fg_color=themes_manager.get_color('button'),
                                         hover_color=themes_manager.get_color('button_hover'),
                                         corner_radius=5)
        self.save_button.pack(side='left', padx=4, fill='x', expand='true')
        self.cancel_button = ctk.CTkButton(buttons_frame,
                                           text="Anuluj",
                                           command=lambda: self.destroy(),
                                           font=themes_manager.get_ctk_font("button"),
                                             fg_color=themes_manager.get_color('button'),
                                            hover_color=themes_manager.get_color('button_hover'),
                                           corner_radius=5)
        self.cancel_button.pack(side='left', padx=4, fill='x', expand='true')
    
    def tag_list_button_click(self):
        """Open tag list window"""
        AddTaskParameters(parent=self, data_name="tag", new_task_window_instance=self)

    def status_list_button_click(self):
        """Open status list window"""
        AddTaskParameters(parent=self, data_name="status", new_task_window_instance=self)

    def priority_list_button_click(self):
        """Open priority list window"""
        AddTaskParameters(parent=self, data_name="priority", new_task_window_instance=self)

    def save_task_button_click(self):
        """Sets the action of the save button and triggers it"""
        if self.button_mode == 'new':
            self.new_task()
        
        elif self.button_mode == 'edit':
            self.edit_task()
    
    def new_task(self):
        """Save new task"""
        params = {
            'id': random.randint(1,10000),
            'title': self.title_entry.get(),
            'description': self.desc_textbox.get(index1="0.0", index2="end"),
            'start': self.start_button.cget("text"),
            'end' : self.end_button.cget('text'),
            'status': self.status_list.cget("text"),
            'priority': self.priority_list.cget("text"),
            'tag': self.tag_list.cget("text")
        }
        reciver = TaskManager()
        save_task_command = Save(reciver, **params)
        self.invoker.set_command(save_task_command)
        self.invoker.press_button()
        self.task_manager_table_instance.populate_treeview()
        self.task_manager_tiles_instance.new_task_tile(title=params['title'],
                                                       status=params['status'],
                                                        priority=params['priority'],
                                                        # deadline=params['start'],
                                                        id_task = params['id']
                                                        )
        self.destroy()
        
    def edit_task(self):
        """Edit the given task"""
        params = {
            'id': self.task_data['id'],
            'title': self.title_entry.get(),
            'description': self.desc_textbox.get(index1="0.0", index2="end"),
            'start': self.start_button.cget("text"),
            'end' : self.end_button.cget('text'),
            'status': self.status_list.cget("text"),
            'priority': self.priority_list.cget("text"),
            'tag': self.tag_list.cget("text")
        }

        task = TaskManager()
        edit_task_command = Edit(task, **params)
        self.invoker.set_command(edit_task_command)
        self.invoker.press_button()
        self.task_manager_table_instance.edit_chosen_task(self.selected_item_id, **params)
        self.task_manager_tiles_instance.edit_tile(self.selected_item_id, params['title'], params['priority'], params['status'])
        
        self.destroy()

    def open_calendar_button_click(self, widget):
        """Open calendar widget"""
        self.deadline_window = DeadlineWindow(self, widget, self.set_date_entry)

    def set_date_entry(self, data):
        if 'start_date' in data:
            self.start_button.configure(text=data['start_date'])
            self.end_button.configure(text="Brak")
            if 'start_time' in data:
                self.start_button.configure(text=f"{data['start_date']}, {data['start_time']}")
                self.end_button.configure(text="Brak")
        if 'end_date' in data:
            self.start_button.configure(text=data['start_date'])
            self.end_button.configure(text=f"{data['end_date']}")
            if 'end_time' in data:
                self.start_button.configure(text=f"{data['start_date']}, {data['start_time']}")
                self.end_button.configure(text=f"{data['end_date']}, {data['end_time']} ")


class AddTaskParameters(ctk.CTkToplevel):
    def __init__(self, parent, data_name, new_task_window_instance):
        super().__init__(parent, fg_color=themes_manager.get_color("background"))
        self.entry_box = None
        self.button_parameters = None
        self.parent = new_task_window_instance
        self.data_name = data_name
        
        singleton = UserSingleton()
        self.pathname = singleton.folder_path
        self.data_file = os.path.join(self.pathname, f"{data_name}.csv")
        self.data_list = []
        
        if data_name == 'status':
            self.widget = self.parent.status_list
        elif data_name == 'priority':
            self.widget = self.parent.priority_list
        elif data_name == 'tag':
            self.widget = self.parent.tag_list
        else:
            raise ValueError(f"Unknown data_name: {data_name}")

        x_pos = self.widget.winfo_rootx()
        y_pos = self.widget.winfo_rooty()

        self.geometry(f"+{x_pos}+{y_pos}")
        self.lift(self.parent)
        self.overrideredirect(True)
        self.import_data_from_csv_file()
        self.create_buttons_list()

        self.bind("<Leave>", self.close_win)

    def close_win(self, event):
        self.after(1, self.check_cursor_position(self))

    def check_cursor_position(self, widget):
        widget = widget
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

    def import_data_from_csv_file(self):

        with open(self.data_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # pomiń pierwszy wiersz
            for row in reader:
                self.data_list.append(row)
            file.close()

    def create_buttons_list(self):
        if self.data_name == 'status' or self.data_name == 'priority' :
            for i in range(len(self.data_list)):
                record_frame = ctk.CTkFrame(self)

                self.button_parameters = ctk.CTkButton(record_frame,
                                                       text=''.join(self.data_list[i]),
                                                       font=themes_manager.get_ctk_font("button"),
                                                       fg_color=themes_manager.get_color("button"),
                                                        hover_color=themes_manager.get_color("button_hover"),
                                                       command=lambda button_text=self.data_list[i][
                                                           0]: self.button_parameters_clicked(button_text)
                                                       ).pack(side='left')
                record_frame.pack(pady=2.5)
                
        elif self.data_name == 'tag':
            self.entry_box = ctk.CTkEntry(self, state='normal',
                                          placeholder_text="Wpisz nowy",
                                          font=themes_manager.get_ctk_font("entry"),
                                          fg_color=themes_manager.get_color("entry"),
                                          border_color=themes_manager.get_color("border_entry"))
            self.entry_box.pack(fill='x', pady=2.5)
            self.entry_box.bind('<Return>', lambda event: self.add_new())

            for i in range(len(self.data_list)):
                record_frame = ctk.CTkFrame(self)

                self.button_parameters = ctk.CTkButton(record_frame,
                                                       text=''.join(self.data_list[i]),
                                                       fg_color=themes_manager.get_color("button"),
                                                       font=themes_manager.get_ctk_font("button"),
                                                         hover_color=themes_manager.get_color("button_hover"),
                                                       command=lambda button_text=self.data_list[i][
                                                           0]: self.button_parameters_clicked(button_text)
                                                       ).pack(side='left')
                ctk.CTkButton(record_frame,
                              text="x",
                              fg_color=themes_manager.get_color("button"),
                            hover_color=themes_manager.get_color("button_hover"),
                              command=lambda parameters=record_frame,
                                             index=self.data_list[i][0]: self.button_delete_clicked(parameters, index),
                              width=10).pack(side='left')
                record_frame.pack(pady=2.5)

    def button_parameters_clicked(self, button_text):
        self.widget.configure(text=button_text)
        self.destroy()
       
    def button_delete_clicked(self, parameters, index):
        parameters.destroy()

        with open(self.data_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            temp_data = list(reader)
            file.close()
        temp_data.remove([index])

        with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(temp_data)
            file.close()

        self.import_data_from_csv_file()

    def add_new(self):

        temp = self.entry_box.get()
        self.entry_box.delete(0, 'end')
        with open(self.data_file, 'a', newline='', encoding='utf=8') as file:
            writer = csv.writer(file)
            writer.writerow([temp])
            file.close()

        self.data_list.append(temp)
        record_frame = ctk.CTkFrame(self)
        ctk.CTkButton(record_frame,
                      text=temp,
                      fg_color=themes_manager.get_color("button"),
                      hover_color=themes_manager.get_color("button_hover"),
                      command=lambda button_text=temp: self.button_parameters_clicked(button_text)).pack(side='left')
        ctk.CTkButton(record_frame,
                      text='x',
                      fg_color=themes_manager.get_color("button"),
                      hover_color=themes_manager.get_color("button_hover"),
                      command=lambda parameters=record_frame, index=temp: self.button_delete_clicked(parameters, index),
                      width=10).pack(side='left')
        record_frame.pack(pady=2.5)
