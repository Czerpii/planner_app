import customtkinter as ctk
from typing import Optional, Tuple, Union
from .WeatherComponents import *

class WeatherWidget(ctk.CTkFrame):
    """
    A custom weather widget frame that contains weather panels and location panel.
    """

    def __init__(self, parent, col, row):
        """
        Initializes a WeatherWidget instance.

        Args:
            parent: The parent widget.
            col (int): The column in the grid.
            row (int): The row in the grid.
        """
        super().__init__(parent, corner_radius=10, fg_color='transparent')
        self.grid(column=col, row=row, sticky='nsew', padx=2)
        
        # Create layout
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=6, uniform='a')
        self.rowconfigure(2, weight=9, uniform='a')
        self.grid_propagate(False)
        
        # Create weather panels
        self.weather_daily_panel = WeatherDailyPanel(self, col=0, row=1)
        self.weather_forecast_panel = Weather5DaysPanel(self, col=0, row=2)
        self.location_panel = LocationPanel(self, col=0, row=0, weather_daily_panel=self.weather_daily_panel, weather_forecast_panel=self.weather_forecast_panel)
