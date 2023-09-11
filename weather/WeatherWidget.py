import customtkinter as ctk
from typing import Optional, Tuple, Union
from weather.WeatherComponents import *
 
class WeatherWidget(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, corner_radius=10, fg_color='transparent')
        self.grid(column = col, row = row, sticky = 'nsew', padx=2)
        
        #create layout
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1,uniform='a')
        self.rowconfigure(1, weight=6,uniform='a')
        self.rowconfigure(2, weight=9, uniform='a')
        self.grid_propagate(False)
      
      
      
        #create panels  
        self.weather_daily_panel = WeatherDailyPanel(self, col=0, row=1)
        self.weather_forecast_panel = Weather5DaysPanel(self, col=0, row=2 )
        self.location_panel = LocationPanel(self, col=0, row=0, weather_daily_panel=self.weather_daily_panel, weather_forecast_panel=self.weather_forecast_panel)
        

        
    
       
        
        
