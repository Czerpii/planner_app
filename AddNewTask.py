import csv
import os

import random

import customtkinter as ctk

from CalendarWidget import CalendarDateEntry
from ICommand import Save
from invoker import Invoker
from task_manager_reciver import *

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


class NewTaskWindow(ctk.CTkToplevel):
    def __init__(self, parent, task_manager_table_instance, task_manager_tiles_instance):
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
        self.task_manager_table_instance = task_manager_table_instance
        self.task_manager_tiles_instance = task_manager_tiles_instance
        self.add_task = AddTaskParameters

        # create storage file to tag priority status
        self.create_data_storage_file("priority")
        self.create_data_storage_file("status")
        self.create_data_storage_file("tag")

        # layout
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=2, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure((1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # fonts
        self.name_font = ctk.CTkFont(family="Abril Fatface", size=30, weight="bold")

        # task title
        self.title_entry = ctk.CTkEntry(self,
                                        placeholder_text="Nazwa",
                                        font=self.name_font,
                                        corner_radius=5,
                                        fg_color=ENTRY_FG,
                                        border_width=0
                                        )
        self.title_entry.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=2)

        # description textbox
        self.create_labels(col=0, row=1, text="Opis zadania")

        self.desc_textbox = ctk.CTkTextbox(self, fg_color=DESC_FG, corner_radius=5)
        self.desc_textbox.grid(column=1, row=1, sticky="nsew", pady=2, padx=2)

        # deadline entry
        self.create_labels(col=0, row=3, text='Termin')

        self.date_button = ctk.CTkButton(self,
                                         text="Bezterminowo",
                                         command=self.open_calendar_button_click,
                                         fg_color=BUTTON_FG,
                                         hover_color=BUTTON_HOVER,
                                         corner_radius=5)
        self.date_button.grid(column=1, row=3, sticky='nsew', pady=2, padx=2)

        # status
        self.create_labels(col=0, row=2, text="Status")
        self.status_list = ctk.CTkButton(self,
                                         text='Nie rozpoczęto',
                                         command=self.status_list_button_click,
                                         fg_color=BUTTON_FG,
                                         hover_color=BUTTON_HOVER,
                                         corner_radius=5)
        self.status_list.grid(column=1, row=2, sticky="nsew", pady=2, padx=2)

        # priority list
        self.create_labels(col=0, row=4, text="Priotytet")
        self.priority_list = ctk.CTkButton(self,
                                           text='Wybierz',
                                           command=self.priority_list_button_click,
                                           fg_color=BUTTON_FG,
                                           hover_color=BUTTON_HOVER,
                                           corner_radius=5)
        self.priority_list.grid(column=1, row=4, sticky="nsew", pady=2, padx=2)

        # tag list
        self.create_labels(col=0, row=5, text="Tag")
        self.tag_list = ctk.CTkButton(self,
                                      text='Wybierz',
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
            'id': random.randint(1,10000),
            'title': self.title_entry.get(),
            'description': self.desc_textbox.get(index1="0.0", index2="end"),
            'deadline': self.date_button.cget("text"),
            'status': self.status_list.cget("text"),
            'priority': self.priority_list.cget("text"),
            'tag': self.tag_list.cget("text")
        }
        task = TaskManager()
        save_task_command = Save(task, **params)
        self.invoker.set_command(save_task_command)
        self.invoker.press_button()
        self.task_manager_table_instance.add_to_treeview()
        self.task_manager_tiles_instance.new_task_tile(title=params['title'],
                                                       status=params['status'],
                                                        priority=params['priority'],
                                                        deadline=params['deadline'],
                                                        id_task = params['id']
                                                        )
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

    def create_data_storage_file(self, data_name: str):
        """Tworzy pliki przechowujące parametry: status, prioryter, tag

        Args:
            data_name (str): należy podać jeden z parametrów dla które chcemy utworzyć plik
        """
        file_name = f"./task_file/{data_name}.csv"
        self.headers = [data_name]

        if data_name == "tag":
            elements = [["Praca"], ["Nauka"], ["Rozwój"]]
        elif data_name == "priority":
            elements = [["Niski"], ["Średni"], ["Wysoki"]]
        elif data_name == "status":
            elements = [["Nie rozpoczęto"], ["W trakcie"], ["Zakończony"]]

        if not os.path.exists(file_name):
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
                file.close()

            with open(file_name, 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(elements)


class AddTaskParameters(ctk.CTkToplevel):
    def __init__(self, parent, data_name, new_task_window_instance):
        super().__init__(parent)
        self.parent = new_task_window_instance
        self.data_name = data_name
        self.data_file = f"./task_file/{data_name}.csv"
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

        if self.data_name == 'status' or "priority":
            for i in range(len(self.data_list)):
                record_frame = ctk.CTkFrame(self)

                self.button_parameters = ctk.CTkButton(record_frame,
                                                       text=''.join(self.data_list[i]),
                                                       fg_color='transparent',
                                                       command=lambda button_text=self.data_list[i][
                                                           0]: self.button_parameters_clicked(button_text)
                                                       ).pack(side='left')
                record_frame.pack(pady=2.5)
        else:
            self.entry_box = ctk.CTkEntry(self, state='normal', placeholder_text="Wpisz nowy")
            self.entry_box.pack(fill='x', pady=2.5)
            self.entry_box.bind('<Return>', lambda event: self.add_new())

            for i in range(len(self.data_list)):
                record_frame = ctk.CTkFrame(self)

                self.button_parameters = ctk.CTkButton(record_frame,
                                                       text=''.join(self.data_list[i]),
                                                       fg_color='transparent',
                                                       command=lambda button_text=self.data_list[i][
                                                           0]: self.button_parameters_clicked(button_text)
                                                       ).pack(side='left')
                ctk.CTkButton(record_frame,
                              text="x",
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
                      fg_color="transparent",
                      command=lambda button_text=temp: self.button_parameters_clicked(button_text)).pack(side='left')
        ctk.CTkButton(record_frame,
                      text='x',
                      command=lambda parameters=record_frame, index=temp: self.button_delete_clicked(parameters, index),
                      width=10).pack(side='left')
        record_frame.pack(pady=2.5)
