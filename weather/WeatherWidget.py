import customtkinter as ctk
from typing import Optional, Tuple, Union
from weather.WeatherComponents import *
 
class WeatherWidget(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color = 'red', corner_radius=0)
        self.grid(column = col, row = row, sticky = 'nsew')
        
        #create layout
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1,uniform='a')
        self.rowconfigure(1, weight=4,uniform='a')
      
      
      
        #create panels  
        self.weather_panel = WeatherPanel(self, col=0, row=1)
        self.location_panel = LocationPanel(self, col=0, row=0, weather_panel=self.weather_panel)
    
    
       
        
        
