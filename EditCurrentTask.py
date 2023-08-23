import csv
import os

import random

import customtkinter as ctk

from CalendarWidget import CalendarDateEntry
from ICommand import Edit
from invoker import Invoker
from task_manager_reciver import *
from AddNewTask import AddTaskParameters
# TOPLEVEL
TOP_LEVEL_FG = "#1E1E1E"

# FRAMES
FRAME_FG = "#1E1E1E"
FRAME_BORDER = "#282828"

# ENTRIES
ENTRY_FG = "#3A3A3A"
ENTRY_TEXT = "#FFFFFF"

# LABELS
LABEL_FG = "#3A3A3A"
LABEL_TEXT = "#FFFFFF"

# BUTTONS
BUTTON_FG = "#282828"
BUTTON_HOVER = "#3A3A3A"

# DESC
DESC_FG = "#282828"


class EditTaskWindow(ctk.CTkToplevel):
    def __init__(self, parent, task_data, selected_item_id):
        super().__init__(parent, fg_color=TOP_LEVEL_FG)
        # centrowanie okna
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - 300 / 2)
        center_y = int(screen_height / 2 - 400 / 2)
        self.geometry(f'300x400+{center_x}+{center_y}')
        self.maxsize(300, 400)
        self.minsize(300, 400)

        self.lift(parent)
        self.transient(parent)
        self.title("Nowe zadanie")
        

        self.invoker = Invoker()
        self.task_manager_table_instance = parent
        # self.task_manager_tiles_instance = task_manager_tiles_instance
        self.add_task = AddTaskParameters
        self.task_data = task_data
        self.selected_item_id = selected_item_id
        
        # layout
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=2, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure((1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # fonts
        self.name_font = ctk.CTkFont(family="Abril Fatface", size=30, weight="bold")

        # task title
        self.title_entry = ctk.CTkEntry(self,
                                        font=self.name_font,
                                        corner_radius=5,
                                        fg_color=ENTRY_FG,
                                        border_width=0
                                        )
        self.title_entry.insert(0, self.task_data['title'])
        self.title_entry.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=2)
        

        # description textbox
        self.create_labels(col=0, row=1, text="Opis zadania")

        self.desc_textbox = ctk.CTkTextbox(self, fg_color=DESC_FG, corner_radius=5)
        self.desc_textbox.insert(ctk.END, self.task_data['description'])
        self.desc_textbox.grid(column=1, row=1, sticky="nsew", pady=2, padx=2)

        # deadline entry
        self.create_labels(col=0, row=3, text='Termin')

        self.date_button = ctk.CTkButton(self,
                                         text=self.task_data['deadline'],
                                         command=self.open_calendar_button_click,
                                         fg_color=BUTTON_FG,
                                         hover_color=BUTTON_HOVER,
                                         corner_radius=5)
        self.date_button.grid(column=1, row=3, sticky='nsew', pady=2, padx=2)

        # status
        self.create_labels(col=0, row=2, text="Status")
        self.status_list = ctk.CTkButton(self,
                                         text=self.task_data['status'],
                                         command=self.status_list_button_click,
                                         fg_color=BUTTON_FG,
                                         hover_color=BUTTON_HOVER,
                                         corner_radius=5)
        self.status_list.grid(column=1, row=2, sticky="nsew", pady=2, padx=2)

        # priority list
        self.create_labels(col=0, row=4, text="Priotytet")
        self.priority_list = ctk.CTkButton(self,
                                           text=self.task_data['priority'],
                                           command=self.priority_list_button_click,
                                           fg_color=BUTTON_FG,
                                           hover_color=BUTTON_HOVER,
                                           corner_radius=5)
        self.priority_list.grid(column=1, row=4, sticky="nsew", pady=2, padx=2)

        # tag list
        self.create_labels(col=0, row=5, text="Tag")
        self.tag_list = ctk.CTkButton(self,
                                      text=self.task_data['tag'],
                                      command=self.tag_list_button_click,
                                      fg_color=BUTTON_FG,
                                      hover_color=BUTTON_HOVER)
        self.tag_list.grid(column=1, row=5, sticky="nsew", pady=2, padx=2)

        # buttons - save and cancel
        self.buttons_frame = ctk.CTkFrame(self, border_width=0, fg_color=FRAME_FG)
        self.buttons_frame.grid(column=0, row=6, columnspan=2, sticky='nsew')

        self.save_button = ctk.CTkButton(self.buttons_frame,
                                         text="Zapisz",
                                         command=self.save_task_button_click,
                                         fg_color=BUTTON_FG,
                                         hover_color=BUTTON_HOVER,
                                         corner_radius=5)
        self.save_button.pack(side='left', padx=4, fill='x', expand='true')
        self.cancel_button = ctk.CTkButton(self.buttons_frame,
                                           text="Anuluj",
                                           command=lambda: self.destroy(),
                                           fg_color=BUTTON_FG,
                                           hover_color=BUTTON_HOVER,
                                           corner_radius=5)
        self.cancel_button.pack(side='left', padx=4, fill='x', expand='true')

    def create_labels(self, col, row, text):
        ctk.CTkLabel(self,
                     text=text,
                     anchor='center',
                     corner_radius=5,
                     fg_color=LABEL_FG,
                     text_color=LABEL_TEXT,
                     ).grid(column=col, row=row, sticky='nsew', pady=2, padx=2)

    def tag_list_button_click(self):
        AddTaskParameters(parent=self, data_name="tag", new_task_window_instance=self)

    def status_list_button_click(self):
        AddTaskParameters(parent=self, data_name="status", new_task_window_instance=self)

    def priority_list_button_click(self):
        AddTaskParameters(parent=self, data_name="priority", new_task_window_instance=self)

    def save_task_button_click(self):
        params = {
            'id': self.task_data['id'],
            'title': self.title_entry.get(),
            'description': self.desc_textbox.get(index1="0.0", index2="end"),
            'deadline': self.date_button.cget("text"),
            'status': self.status_list.cget("text"),
            'priority': self.priority_list.cget("text"),
            'tag': self.tag_list.cget("text")
        }
     
        task = TaskManager()
        edit_task_command = Edit(task, **params)
        self.invoker.set_command(edit_task_command)
        self.invoker.press_button()
        self.task_manager_table_instance.edit_choosen_task(self.selected_item_id, **params)
        
        self.destroy()

    
    def open_calendar_button_click(self):
        x_pos = self.date_button.winfo_rootx()
        y_pos = self.date_button.winfo_rooty()

        self.cal_widget = ctk.CTkToplevel(self)
        self.cal_widget.geometry(f"210x210+{x_pos}+{y_pos}")
        self.cal_widget.title("Wybierz date")
        self.cal_widget.overrideredirect(True)
        self.cal_widget.transient(self)

        cal = CalendarDateEntry(self.cal_widget, on_date_select=self.set_date_entry)

    def set_date_entry(self, date):
        self.date_button.configure(text=date)

        self.cal_widget.destroy()
