from customtkinter import CTkFrame
from weather.WeatherWidget import *
from world_clock.clock_view import WorldClock

class InfoBar(CTkFrame):
    def __init__(self, parent, col, row, rowspan):
        super().__init__(master=parent, fg_color='#004B23', corner_radius=0)
        self.grid(column=col, row=row, rowspan=rowspan, sticky='nsew')

        # layout
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
        self.rowconfigure(2, weight=2, uniform='a')

        # widget
        WeatherWidget(self, col=0, row=2)
        WorldClock(self, col=0, row=0)