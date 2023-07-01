import customtkinter as ctk
from weather.OpenWeatherMap import *
from IpapiLocation import *




class LocationPanel(ctk.CTkFrame):
    def __init__(self, parent, col, row, weather_panel):
        super().__init__(parent, fg_color='transparent')
        self.grid(column = col, row = row, sticky = 'nsew')
         
        self.location = IpapiLocation()
        self.weather_panel = weather_panel
        
        
        #layout
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=2,uniform='a')
        self.rowconfigure(1, weight=1,uniform='a')
        
        
        #combobox
        combobox_value = self.location.get_all_location()
        self.combo = ctk.CTkComboBox(self, 
                        values=combobox_value, 
                        corner_radius=10,
                        state = 'normal',
                        justify='left',
                        command=self.choose_location)
        
        self.combo.set(self.location.get_location_with_default_state())
        self.combo.grid(column = 0, row =0, sticky = 'nsew', pady = 5) 
        self.combo.bind('<Return>', self.add_new)
      
    def choose_location(self, event): #przekazanie lokalizacji, wybranej w comboboxie, do weatherprovider
        actuall_value = self.combo.get().split(',')
        self.location.set_default_state(actuall_value[0])
        self.weather_panel.update_weather()
     
    def add_new(self, event):
        new_item = self.combo.get().split(',')
        new_item[0] = ' '.join(new_item[0].split())
        self.location.add_location(city = new_item[0])
        combobox_value = self.location.get_all_location()
        self.combo.configure(values=combobox_value)
        self.choose_location(event)
        
        
         
               
class WeatherPanel(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color='transparent')
        self.grid(column=col, row=row, sticky='nsew')
        
        weather =  OpenWeaterMap.get_weather_today(IpapiLocation().get_location_with_default_state())
        
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure((1,2,3,4,5), weight=1, uniform='a')
        
        #nazwy
        
        
        ctk.CTkLabel(self,
                     text = 'Odczuwalna:').grid(column = 0, row = 2, sticky = 'w', padx=2)
        ctk.CTkLabel(self,
                     text = 'Ciśnienie:').grid(column = 0, row = 3, sticky = 'w',  padx=2)
        ctk.CTkLabel(self,
                     text = 'Wilgotność:').grid(column = 0, row = 4, sticky = 'w', padx=2 )
        ctk.CTkLabel(self,
                     text = 'Prędkość wiatru:').grid(column = 0, row = 5, sticky = 'w', padx=2)
        
        #wartości
        self.temperature_label = ctk.CTkLabel(self,
                     text = f"{weather['temp']}\N{DEGREE SIGN}C",
                     font = ctk.CTkFont(family='Calibri', size=60, weight='bold'))
        self.temperature_label.grid(column=0, columnspan =2, row = 0, sticky = 'nsew')
        
        self.description_label = ctk.CTkLabel(self, text=f"{weather['description']}")
        self.description_label.grid(column=0, columnspan =2, row = 1, sticky = 'nsew')
        
        self.feels_like_label = ctk.CTkLabel(self,text = f"{weather['feels_like']}\N{DEGREE SIGN}C")
        self.feels_like_label.grid(column=1, row = 2, sticky='w')
        
        self.pressure_label = ctk.CTkLabel(self,text = f"{weather['pressure']} hPa")
        self.pressure_label.grid(column=1, row = 3, sticky='w')
        
        self.humidity_label = ctk.CTkLabel(self,text = f"{weather['humidity']}%")
        self.humidity_label.grid(column=1, row = 4, sticky='w')
        self.wind_label = ctk.CTkLabel(self,text = f"{weather['wind']} m/s")
        self.wind_label.grid(column=1, row = 5, sticky='w')

    def update_weather(self):
        location = IpapiLocation().get_location_with_default_state()
        weather = OpenWeaterMap.get_weather_today(location)

        # Zaktualizuj etykiety z informacjami o pogodzie
        self.temperature_label.configure(text=f"{weather['temp']}\N{DEGREE SIGN}C")
        self.feels_like_label.configure(text=f"{weather['feels_like']}\N{DEGREE SIGN}C")
        self.pressure_label.configure(text=f"{weather['pressure']} hPa")
        self.humidity_label.configure(text=f"{weather['humidity']}%")
        self.wind_label.configure(text=f"{weather['wind']} m/s")      
        self.description_label.configure(text=f"{weather['description']}")
        print("aa")
     
    