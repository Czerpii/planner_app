import customtkinter as ctk
from .OpenWeatherMap import *
from location.ApiLocation import *
from PIL import Image, ImageTk
import themes_manager


class LocationPanel(ctk.CTkFrame):
    """
    A class representing a panel for selecting and managing locations.
    """

    def __init__(self, parent, col, row, weather_daily_panel, weather_forecast_panel):
        """
        Initializes a LocationPanel instance.

        Args:
            parent: The parent widget.
            col (int): The column in the grid.
            row (int): The row in the grid.
            weather_daily_panel: The weather panel for daily forecasts.
            weather_forecast_panel: The weather panel for 5-day forecasts.
        """
        super().__init__(parent, fg_color="transparent", corner_radius=5)
        self.grid(column=col, row=row, sticky='nsew', pady=3, padx=3)
         
        self.location = ApiLocation()
        self.weather_daily_panel = weather_daily_panel
        self.weather_forecast_panel = weather_forecast_panel
        
        # Layout
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        
        # Combobox
        combobox_value = self.location.get_all_location()
        self.combo = ctk.CTkComboBox(
            self, 
            values=combobox_value,
            font=themes_manager.get_ctk_font('entry'),
            fg_color=themes_manager.get_color('entry'),
            button_color=themes_manager.get_color("button"),
            button_hover_color=themes_manager.get_color("button_hover"),
            border_width=0,
            dropdown_fg_color=themes_manager.get_color('background'),
            dropdown_hover_color=themes_manager.get_color("button_hover"),
            corner_radius=10,
            state='normal',
            justify='left',
            command=self.choose_location
        )
        self.combo.set(self.location.get_location_with_default_state())
        self.combo.grid(column=0, row=0, sticky='nsew') 
        self.combo.bind('<Return>', self.add_new)
      
    def choose_location(self, event):
        """
        Handle the selection of a location from the combo box.

        Args:
            event: The event object (not used in this method).
        """
        actual_value = self.combo.get().split(',')
        self.location.set_default_state(actual_value[0])
        self.weather_daily_panel.update_daily_weather()
        self.weather_forecast_panel.update_forecast_weather()
     
    def add_new(self, event):
        """
        Add a new location to the combo box and set it as the default location.

        Args:
            event: The event object (not used in this method).
        """
        new_item = self.combo.get().split(',')
        new_item[0] = ' '.join(new_item[0].split())
        self.location.add_location(city=new_item[0])
        combobox_value = self.location.get_all_location()
        self.combo.configure(values=combobox_value)
        self.choose_location(event)

        
        
         
               
class WeatherDailyPanel(ctk.CTkFrame):
    """
    A class representing a panel for displaying daily weather information.
    """

    def __init__(self, parent, col, row):
        """
        Initializes a WeatherDailyPanel instance.

        Args:
            parent: The parent widget.
            col (int): The column in the grid.
            row (int): The row in the grid.
        """
        super().__init__(parent, fg_color=themes_manager.get_color("fg_frame"), corner_radius=5)
        self.grid(column=col, row=row, sticky='nsew', padx=3, pady=3)
        
        weather = OpenWeaterMap.get_weather_today(ApiLocation().get_location_with_default_state())
        self.parent = parent
        
        # Layout configuration
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure((1,2,3,4,5), weight=1, uniform='a')
        self.grid_propagate(False)
        
        # Labels for weather information
        ctk.CTkLabel(self, text='Odczuwalna:', font=themes_manager.get_ctk_font("default")).grid(column=0, row=2, sticky='w', padx=2)
        ctk.CTkLabel(self, text='Ciśnienie:', font=themes_manager.get_ctk_font("default")).grid(column=0, row=3, sticky='w', padx=2)
        ctk.CTkLabel(self, text='Wilgotność:', font=themes_manager.get_ctk_font("default")).grid(column=0, row=4, sticky='w', padx=2)
        ctk.CTkLabel(self, text='Prędkość wiatru:', font=themes_manager.get_ctk_font("default")).grid(column=0, row=5, sticky='w', padx=2)
        
        # Temperature and weather description
        self.temperature_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.temperature_frame.grid(column=0, row=0, columnspan=2, sticky='nsew', padx=2, pady=2)      
        self.temperature_frame.columnconfigure(0, weight=1, uniform='a')  
        self.temperature_frame.columnconfigure(1, weight=3, uniform='a')  
        self.temperature_frame.rowconfigure(0, weight=0, uniform='a')
        self.temperature_frame.grid_propagate(False)

        self.ico_label = ctk.CTkLabel(self.temperature_frame, text="")
        self.ico_label.grid(column=0, row=0, sticky='nsew', pady=5, padx=3)
          
        self.temperature_label = ctk.CTkLabel(self.temperature_frame,
                     text=f"{weather['temp']}\N{DEGREE SIGN}C",
                     font=ctk.CTkFont(family='San Francisco', size=50, weight='bold'))
        self.temperature_label.grid(column=1, row=0, sticky='nsew', pady=5, padx=3)
        
        self.description_label = ctk.CTkLabel(self,
                                              text=f"{weather['description']}",
                                              font=themes_manager.get_ctk_font("default"))
        self.description_label.grid(column=0, columnspan=2, row=1, sticky='nsew')
        
        self.feels_like_label = ctk.CTkLabel(self,
                                             text=f"{weather['feels_like']}\N{DEGREE SIGN}C",
                                             font=themes_manager.get_ctk_font("default"))
        self.feels_like_label.grid(column=1, row=2, sticky='w')
        
        self.pressure_label = ctk.CTkLabel(self,
                                           text=f"{weather['pressure']} hPa",
                                           font=themes_manager.get_ctk_font("default"))
        self.pressure_label.grid(column=1, row=3, sticky='w')
        
        self.humidity_label = ctk.CTkLabel(self,
                                           text=f"{weather['humidity']}%",
                                           font=themes_manager.get_ctk_font("default"))
        self.humidity_label.grid(column=1, row=4, sticky='w')
        
        self.wind_label = ctk.CTkLabel(self,
                                       text=f"{weather['wind']} m/s",
                                       font=themes_manager.get_ctk_font("default"))
        self.wind_label.grid(column=1, row=5, sticky='w')

        self.set_icon_based_on_weather_status(weather['weather_ico'])
        self.start_updating_weather()

    def update_daily_weather(self):
        """
        Update the daily weather information displayed on the panel.
        """
        location = ApiLocation().get_location_with_default_state()
        weather = OpenWeaterMap.get_weather_today(location)

        # Update weather information labels
        self.weather_status = weather['weather_main']
        self.temperature_label.configure(text=f"{weather['temp']}\N{DEGREE SIGN}C")
        self.feels_like_label.configure(text=f"{weather['feels_like']}\N{DEGREE SIGN}C")
        self.pressure_label.configure(text=f"{weather['pressure']} hPa")
        self.humidity_label.configure(text=f"{weather['humidity']}%")
        self.wind_label.configure(text=f"{weather['wind']} m/s")      
        self.description_label.configure(text=f"{weather['description']}")

        self.set_icon_based_on_weather_status(weather['weather_ico'])
    
    def start_updating_weather(self, interval=600000):
        """
        Start updating the weather information at a specified interval.

        Args:
            interval (int): The interval (in milliseconds) at which to update the weather information.
        """
        self.update_daily_weather()
        self.after(interval, self.start_updating_weather, interval)
    
    def set_icon_based_on_weather_status(self, weather_ico):
        """
        Set the weather icon based on the weather status.

        Args:
            weather_ico (str): The weather icon code.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(current_directory, f"weather_status_image/{weather_ico}.png")

        image = ctk.CTkImage(Image.open(icon_path), size=(50, 50))
        self.ico_label.configure(image=image)

        
        
class Weather5DaysPanel(ctk.CTkFrame):
    """
    A class representing a panel for displaying 5 days weather forecast.
    """

    def __init__(self, parent, col, row):
        """
        Initializes a Weather5DaysPanel instance.

        Args:
            parent: The parent widget.
            col (int): The column in the grid.
            row (int): The row in the grid.
        """
        super().__init__(parent, fg_color=themes_manager.get_color("foreground_infobar"), corner_radius=5)
        self.grid(column=col, row=row, sticky='nsew', padx=3, pady=3)
        
        # Fetch the default 5-day weather forecast
        self.default_weather = OpenWeaterMap.get_5_days_forecast(ApiLocation().get_location_with_default_state(), self.format_date)
        
        self.configure_layout()
        self.create_date_labels()
        self.create_temp_labels()
        
    def configure_layout(self):
        """
        Configure the layout of the panel.
        """
        self.columnconfigure((0,1), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3,4), weight=1, uniform='a')
        self.grid_propagate(False)
    
    def create_date_labels(self):
        """
        Create labels for displaying dates.
        """
        row = 0
        font = ctk.CTkFont(family='Arial Black', size=12)
        
        for date in self.default_weather.keys():
            day_of_week, day_and_month = date.split(', ')
            formatted_date = f"{day_of_week}\n{day_and_month}"
            ctk.CTkLabel(self, text=formatted_date, font=themes_manager.get_ctk_font("default")).grid(column=0, row=row, sticky="nsew", padx=2, pady=2)
            row += 1
    
    def create_temp_labels(self):
        """
        Create labels for displaying temperatures and weather icons.
        """
        row = 0
        
        for key, value in self.default_weather.items():
            avg_temp = value['średnia_temperatura']
            icon = value['icon']
            current_directory = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_directory, f"weather_status_image/{icon}.png")
            
            frame = ctk.CTkFrame(self, fg_color='transparent')
            frame.grid(column=1, row=row, sticky='nsew', padx=2, pady=2)
            
            ctk.CTkLabel(frame,
                         text='',
                         image=ctk.CTkImage(Image.open(icon_path), size=(30,30))).pack(side='left')
            
            ctk.CTkLabel(frame,
                         text=f"{avg_temp}\N{DEGREE SIGN}C",
                         font=themes_manager.get_ctk_font("default")).pack(side='left')
            row += 1
    
    def update_forecast_weather(self):
        """
        Update the forecasted weather information.
        """
        location = ApiLocation().get_location_with_default_state()
        self.default_weather = OpenWeaterMap.get_5_days_forecast(location, self.format_date)
        
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        self.configure_layout()
        self.create_date_labels()
        self.create_temp_labels()
             
    def set_icon_based_on_weather_status(self, weather_ico):
        """
        Set the weather icon based on the weather status.

        Args:
            weather_ico (str): The weather icon code.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(current_directory, f"weather_widget/weather_status_image/{weather_ico}.png")

        image = ctk.CTkImage(Image.open(icon_path), size=(50,50))
        self.ico_label.configure(image=image)
    
    def format_date(self, date_str):
        """
        Format the date string.

        Args:
            date_str (str): The date string in the format "YYYY-MM-DD".

        Returns:
            str: The formatted date string.
        """
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        days_pl = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Niedz"]
        months_pl = ["Sty", "Lut", "Mar", "Kwi", "Maj", "Cze", "Lip", "Sie", "Wrz", "Paź", "Lis", "Gru"]
        
        formatted_date = f"{days_pl[date_obj.weekday()]}, {date_obj.day} {months_pl[date_obj.month-1]}"
        
        return formatted_date

    
    