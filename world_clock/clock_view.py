from typing import Optional, Tuple, Union
import customtkinter as ctk
import pytz 
import time as tm
from world_clock.clock_logic import *




class WorldClock(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky='nsew')
        
        self.api_instance = TimeZone()
        
        self.configure_layout()
        self.digital_clock_widget()
        self.timezones_button()
        
        self.api_instance.display_time(timezone_str=self.api_instance.get_actuall_timezone('both',), widget=self.digital_clock)
        
        
    def configure_layout(self):
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        self.grid_propagate(False)
        
    
    
    
    def digital_clock_widget(self):
        
        #font for digital timer
        digital_clock_font = ctk.CTkFont(family='Arial Black', size=30)
        
        #label for digital timer
        self.digital_clock = ctk.CTkLabel(self, font = digital_clock_font)
        self.digital_clock.grid(column=0, row=1, sticky='nsew')
        
        
    
    def timezones_button(self):
       
        self.timezones = ctk.CTkLabel(self,
                                 text =f"{self.api_instance.get_actuall_timezone('region')}, {self.api_instance.get_actuall_timezone('city')}",
                                 fg_color='black',
                                 font = ctk.CTkFont(family='Arial Black', size=10), 
                                 corner_radius=10)
        self.timezones.grid(column=0, row=0, sticky='nsew', padx=2, pady=1)
        self.timezones.grid_propagate(False)
        
        
        self.timezones.bind("<Button-1>", self.open_time_zone_window )
        self.timezone = self.api_instance.get_actuall_timezone('both')
        
        
        
   
    def open_time_zone_window(self, event):
        button_text = self.timezones.cget('text')
        self.region, self.city = button_text.split(", ")
        
        TimezonesWindow(self, self.region, self.city, self.timezone)
    
    def change_timezone(self, region, city, timezone):
        self.timezone = timezone
        self.timezones.configure(text=f"{region}, {city}")
        
        self.api_instance.stop_display_time(self.digital_clock)
        self.api_instance.start_display_time(timezone=timezone, widget=self.digital_clock)
        
class TimezonesWindow(ctk.CTkToplevel):
    def __init__(self, parent, region, city, timezone):
        super().__init__(parent)
        
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
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - 700 / 2)
        center_y = int(screen_height / 2 - 400 / 2)
        self.geometry(f'700x500+{center_x}+{center_y}')
        self.maxsize(700, 500)
        self.minsize(700, 500)


        self.lift(self.parent)
        self.transient(self.parent)
        self.title("Strefy czasowe")
        self.focus()
    
    def configure_layout(self):
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        self.rowconfigure(3, weight=8, uniform='a')
        self.rowconfigure(4, weight=1, uniform='a')
        # self.grid_propagate(False)
    
    
    def create_time_frame(self):
        
        tm_frame = ctk.CTkFrame(self, fg_color="transparent")
        tm_frame.grid(column=0, row=0, sticky='nsew', padx=4, pady=4)
        
        
        tm_frame.columnconfigure((0,3), weight=1, uniform='a')
        tm_frame.columnconfigure((1,2), weight=3, uniform='a')
        tm_frame.rowconfigure(0, weight=1, uniform='a')
        
        
        font = ctk.CTkFont(family='Arial Black', size=20)
        
        self.city_label = ctk.CTkLabel(tm_frame,
                                       font = font,
                                       text=f"{self.start_region}, {self.start_city}"
                                       )
        self.city_label.grid(column=1, row=0, sticky='nse', padx=2)
        
        self.time_label = ctk.CTkLabel(tm_frame, font=font)
        self.time_label.grid(column=2, row=0, sticky='nsew', padx=2)
        
        self.api_instance.display_time(timezone_str=self.start_timezone,
                                       widget=self.time_label)
        
       
      
    def region_frame(self):
        
        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.grid(column=0, row=1,sticky='nsew')
        
        regions = ["Europa", "Ameryka", "Afryka", "Azja", "Oceania"]
        
        for region in regions:
            ctk.CTkButton(frame, text=region, command=lambda region=region: self.set_region(region)).pack(side='left', padx=2, fill='both')
        
    
    def cities_frame(self, region):
        
        self.cities = self.api_instance.get_cities(region)
        self.search_var = ctk.StringVar()
        
        search_entry = ctk.CTkEntry(self, placeholder_text='Szukaj', textvariable=self.search_var)
        search_entry.grid(column=0, columnspan=3, row=2, sticky='nsew', padx=10, pady=5)
        self.search_var.trace('w', self.filter_cities)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self.scroll_frame.grid(column=0, row=3, sticky='nsew')
        
        self.scroll_frame.columnconfigure((0,1,2), weight=1, uniform='a')
        
        self.create_cities_buttons(self.cities)
        
    
    def create_save_and_cancel_button(self):
        
        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.grid(column=0, row=4, sticky='nsew')
        
        save_button = ctk.CTkButton(frame, text='Zapisz', command=self.save_button_click)
        save_button.pack(side='right', fill='both', padx=4, pady=4)
        
        cancel_button = ctk.CTkButton(frame, text='Anuluj', command=lambda: self.destroy())
        cancel_button.pack(side='right', fill='both', padx=4, pady=4)
                
    
    def filter_cities(self, *args):
        search_text = self.search_var.get().title()
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        filtered_cities = [city for city in self.cities if search_text in city]

        self.create_cities_buttons(filtered_cities)

    def create_cities_buttons(self, timezones):
        row = 1
        column = 0
        
        for timezone in timezones:
            city = timezone.split('/')[-1].replace('_', ' ')
            ctk.CTkButton(self.scroll_frame,
                         text=city,
                        command=lambda city=city, timezone=timezone: self.city_button_click(city, timezone)).grid(column=column, row=row, sticky='nsew', padx=2, pady=2)
            column += 1
            if column == 3:
                column = 0
                row += 1
            
                   
    def set_region(self, region):
        
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
        

    def city_button_click(self,city, timezone):
        self.timezone_selected = timezone
        self.city_selected = city
        
        self.city_label.configure(text=f"{self.region}, {city}")
        
        
        
        self.api_instance.stop_display_time(self.time_label)
        
        
        self.api_instance.start_display_time(timezone=timezone, widget=self.time_label)
        
        
    
    def save_button_click(self):
        self.api_instance.stop_display_time(self.time_label)
        self.parent.change_timezone(self.region, self.city_selected, self.timezone_selected)
        self.destroy()
    
    def set_choosen_timezone(self, region, city):
        pass
        