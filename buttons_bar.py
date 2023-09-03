import customtkinter as ctk
from PIL import Image
from task_manager.TaskManagerView import TaskManagerMain


class ButtonsBar(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color='#474747', )
        self.grid(column=col, row=row, sticky='nsew')
        self.parent = parent

        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, uniform='a')

        # dodawanie obrazków
        task_image = ctk.CTkImage(dark_image=Image.open("./button_image/task.png"),
                                  light_image=Image.open("./button_image/task.png"),
                                  size=(40, 40))

        reminders_image = ctk.CTkImage(dark_image=Image.open("./button_image/reminders.png"),
                                       light_image=Image.open("./button_image/reminders.png"),
                                       size=(50, 50))

        # przycisk uruchamijacy widok menadżera zadań
        self.task_manager_button = ctk.CTkButton(self,
                                                 text="",
                                                 fg_color='transparent',
                                                 hover_color="#5F5F5F",
                                                 image=task_image,
                                                 command=self.task_manager_button_click)
        self.task_manager_button.grid(column=0, row=0, sticky='ns', padx=5, pady=1)

        self.reminder_button = ctk.CTkButton(self,
                                             text="",
                                             fg_color='transparent',
                                             hover_color="#5F5F5F",
                                             image=reminders_image, )
        self.reminder_button.grid(column=1, row=0, sticky='ns', pady=1)

    def task_manager_button_click(self):
        TaskManagerMain(self.parent, 0, 1)
