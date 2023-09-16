from customtkinter import CTkFrame
from weather_widget.WeatherWidget import *
from world_clock.clock_view import WorldClock
import themes_manager

class InfoBar(CTkFrame):
    """
    The InfoBar class represents a frame that contains widgets to display information 
    such as weather and world clock.
    """
    
    def __init__(self, parent, col, row, rowspan):
        """
        Initializes a new instance of the InfoBar class.
        
        Args:
            parent (tk.Widget): The parent widget.
            col (int): The column where the InfoBar should be placed in the grid.
            row (int): The row where the InfoBar should be placed in the grid.
            rowspan (int): How many rows the InfoBar should span in the grid.
        """
        super().__init__(master=parent, fg_color='transparent', corner_radius=0)
        self.grid(column=col, row=row, rowspan=rowspan, sticky='nsew')

        # Configure layout
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=4, uniform='a')

        # Initialize and place widgets
        WeatherWidget(self, col=0, row=1)  # Weather widget
        WorldClock(self, col=0, row=0)     # World clock widget
