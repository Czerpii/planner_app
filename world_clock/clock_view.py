from typing import Optional, Tuple, Union
import customtkinter as ctk
import pytz 
import time as tm
from .clock_logic import *
import themes_manager



class WorldClock(ctk.CTkFrame):
    """
    A class representing a world clock widget.
    """
    
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky='nsew')
        
        # Initialize the API instance and get the current timezone
        self.api_instance = TimeZone()
        self.timezone = self.api_instance.get_actuall_timezone('both')
        
        # Configure layout and create widgets
        self.configure_layout()
        self.create_timezones_button()
        self.create_clock_and_date_frame()
        
        # Display the current time
        self.api_instance.display_time(timezone_str=self.timezone, widget=self.digital_clock)
        
    def configure_layout(self):
        """Configures the layout of the WorldClock widget."""
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
        self.grid_propagate(False)
       
    def create_clock_and_date_frame(self):
        """Creates the frame containing the digital clock and date."""
        frame = ctk.CTkFrame(self, corner_radius=5, fg_color=themes_manager.get_color("foreground_infobar"))
        frame.grid(column=0, row=1, sticky='nsew', padx=3, pady=2)
        self.grid_propagate(False)
        
        # Set fonts
        digital_clock_font = ctk.CTkFont(family='Arial Black', size=22)
        date_font = ctk.CTkFont(family='Arial Black', size=10)
        
        # Create date and time labels
        self.date_label = ctk.CTkLabel(frame,
                                  text=self.api_instance.get_current_date_with_weekday(self.timezone),
                                  font=themes_manager.get_ctk_font("date"))
        self.date_label.pack(side='top', anchor='center', pady=5)
        
        self.digital_clock = ctk.CTkLabel(frame, font=themes_manager.get_ctk_font("clock"))
        self.digital_clock.pack(side='top', anchor='center')
        
    def create_timezones_button(self):
        """Creates the button displaying the current timezone."""
        self.timezones = ctk.CTkButton(self,
                                 text =f"{self.api_instance.get_actuall_timezone('region')}, {self.api_instance.get_actuall_timezone('city')}",
                                 fg_color=themes_manager.get_color("fg_frame"),
                                 hover = False,
                                 font=themes_manager.get_ctk_font("date"), 
                                 corner_radius=5,
                                 command= self.open_time_zone_window)
        self.timezones.grid(column=0, row=0, sticky='nsew', padx=3, pady=2)
        self.timezones.grid_propagate(False)
   
    def open_time_zone_window(self):
        """Opens a window to select a different timezone."""
        button_text = self.timezones.cget('text')
        self.region, self.city = button_text.split(", ")
        TimezonesWindow(self, self.region, self.city, self.timezone)
    
    def change_timezone(self, region, city, timezone):
        """Changes the displayed timezone."""
        self.timezone = timezone
        self.timezones.configure(text=f"{region}, {city}")
        
        # Stop the current time display and start displaying the new timezone
        self.api_instance.stop_display_time(self.digital_clock)
        self.api_instance.start_display_time(timezone=timezone, widget=self.digital_clock)
        self.date_label.configure(self.api_instance.get_current_date_with_weekday(timezone))

        
class TimezonesWindow(ctk.CTkToplevel):
    """
    A class representing a window for selecting timezones.

    Attributes:
        parent: The parent window.
        region: The current region.
        city: The current city.
        timezone: The current timezone.
    """

    def __init__(self, parent, region, city, timezone):
        """
        Initializes a TimezonesWindow.

        Args:
            parent: The parent window.
            region: The current region.
            city: The current city.
            timezone: The current timezone.
        """
        super().__init__(parent, fg_color=themes_manager.get_color('background'))
        
        self.parent = parent
        self.api_instance = TimeZone()
        self.start_region = region
        self.start_city = city
        self.start_timezone = timezone
        
        self.setup_window()
        self.configure_layout()
        self.region_frame()
        self.create_time_frame()
        self.create_save_and_cancel_button()
        
    def setup_window(self):
        """
        Set up the window's properties.
        """
        x_pos = self.parent.winfo_rootx()
        y_pos = self.parent.winfo_rooty()
        
        self.geometry(f'700x500+{x_pos-800}+{y_pos+100}')
        self.maxsize(700, 500)
        self.minsize(700, 500)
        self.lift(self.parent)
        self.transient(self.parent)
        self.title("Strefy czasowe")
        self.focus()
    
    def configure_layout(self):
        """
        Configure the layout of the window.
        """
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        self.rowconfigure(3, weight=8, uniform='a')
        self.rowconfigure(4, weight=1, uniform='a')
    
    def create_time_frame(self):
        """
        Create the frame for displaying time.
        """
        tm_frame = ctk.CTkFrame(self, fg_color="transparent")
        tm_frame.grid(column=0, row=0, sticky='nsew', padx=4, pady=4)
        
        tm_frame.columnconfigure((0,3), weight=1, uniform='a')
        tm_frame.columnconfigure((1,2), weight=3, uniform='a')
        tm_frame.rowconfigure(0, weight=1, uniform='a')
        
        self.city_label = ctk.CTkLabel(tm_frame,
                                       font=themes_manager.get_ctk_font("small_header"),
                                       text=f"{self.start_region}, {self.start_city}"
                                       )
        self.city_label.grid(column=1, row=0, sticky='nse', padx=2)
        
        self.time_label = ctk.CTkLabel(tm_frame, font=themes_manager.get_ctk_font("small_header"))
        self.time_label.grid(column=2, row=0, sticky='nsew', padx=2)
        
        self.api_instance.display_time(timezone_str=self.start_timezone,
                                       widget=self.time_label)
       
    def region_frame(self):
        """
        Create the frame for selecting regions.
        """
        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.grid(column=0, row=1, sticky='nsew')
        
        regions = ["Europa", "Ameryka", "Afryka", "Azja", "Oceania"]
        
        for region in regions:
            ctk.CTkButton(frame,
                          font=themes_manager.get_ctk_font("button"),
                          text=region,
                          fg_color=themes_manager.get_color('button'),
                          hover_color=themes_manager.get_color('button_hover'),
                          command=lambda region=region: self.set_region(region)).pack(side='left', padx=2, fill='both')
        
    
        # ... Previous code ...

    def cities_frame(self, region):
        """
        Create the frame for displaying cities within the selected region.

        Args:
            region (str): The selected region.
        """
        self.cities = self.api_instance.get_cities(region)
        self.search_var = ctk.StringVar()
        
        search_entry = ctk.CTkEntry(self,
                                    placeholder_text='Szukaj',
                                    font=themes_manager.get_ctk_font("entry"),
                                    fg_color=themes_manager.get_color('entry'),
                                    border_width=0,
                                    textvariable=self.search_var)
        search_entry.grid(column=0, columnspan=3, row=2, sticky='nsew', padx=10, pady=5)
        self.search_var.trace('w', self.filter_cities)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self,
                                                   fg_color='transparent',
                                                   scrollbar_button_color=themes_manager.get_color('button'),
                                                   scrollbar_button_hover_color=themes_manager.get_color("button_hover"))
        self.scroll_frame.grid(column=0, row=3, sticky='nsew')
        
        self.scroll_frame.columnconfigure((0,1,2), weight=1, uniform='a')
        
        self.create_cities_buttons(self.cities)
    
    def create_save_and_cancel_button(self):
        """
        Create the Save and Cancel buttons at the bottom of the window.
        """
        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.grid(column=0, row=4, sticky='nsew')
        
        save_button = ctk.CTkButton(frame, text='Zapisz',
                                    font=themes_manager.get_ctk_font("button"),
                                    fg_color=themes_manager.get_color('button'),
                                    hover_color=themes_manager.get_color('button_hover'),
                                    command=self.save_button_click)
        save_button.pack(side='right', fill='both', padx=4, pady=4)
        
        cancel_button = ctk.CTkButton(frame, text='Anuluj',
                                      font=themes_manager.get_ctk_font("button"),
                                      fg_color=themes_manager.get_color('button'),
                                      hover_color=themes_manager.get_color('button_hover'),
                                      command=lambda: self.destroy())
        cancel_button.pack(side='right', fill='both', padx=4, pady=4)
                
    def filter_cities(self, *args):
        """
        Filter and display cities based on the search input.
        """
        search_text = self.search_var.get().title()
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        filtered_cities = [city for city in self.cities if search_text in city]

        self.create_cities_buttons(filtered_cities)

    def create_cities_buttons(self, timezones):
        """
        Create buttons for selecting cities.

        Args:
            timezones (list): A list of timezones (city names).
        """
        row = 1
        column = 0
        
        for timezone in timezones:
            city = timezone.split('/')[-1].replace('_', ' ')
            ctk.CTkButton(self.scroll_frame,
                         text=city,
                         font=themes_manager.get_ctk_font("button"),
                         fg_color=themes_manager.get_color('button'),
                         hover_color=themes_manager.get_color('button_hover'),
                        command=lambda city=city, timezone=timezone: self.city_button_click(city, timezone)).grid(column=column, row=row, sticky='nsew', padx=2, pady=2)
            column += 1
            if column == 3:
                column = 0
                row += 1

    def set_region(self, region):
        """
        Set the selected region and update the cities frame.

        Args:
            region (str): The selected region.
        """
        if region == "Europa":
            self.region = "Europe"
        elif region == "Afryka":
            self.region = "Africa"
        elif region == "Ameryka":
            self.region = "America"
        elif region == "Azja":
            self.region = "Asia"
        else:
            self.region = region
            
        self.cities_frame(self.region)

    def city_button_click(self, city, timezone):
        """
        Handle the click event of a city button.

        Args:
            city (str): The selected city.
            timezone (str): The timezone associated with the city.
        """
        self.timezone_selected = timezone
        self.city_selected = city
        
        self.city_label.configure(text=f"{self.region}, {city}")
        
        self.api_instance.stop_display_time(self.time_label)
        self.api_instance.start_display_time(timezone=timezone, widget=self.time_label)

    def save_button_click(self):
        """
        Handle the click event of the Save button.
        """
        self.api_instance.stop_display_time(self.time_label)
        self.parent.change_timezone(self.region, self.city_selected, self.timezone_selected)
        self.destroy()
    
    def set_choosen_timezone(self, region, city):
        """
        Set the chosen timezone based on the selected region and city.

        Args:
            region (str): The selected region.
            city (str): The selected city.
        """
        pass  # Add your implementation here if needed
