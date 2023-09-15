from typing import Optional, Tuple, Union
import customtkinter as ctk
import pytz 
import time as tm
from .clock_logic import *
import themes_manager



class WorldClock(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky='nsew')
        
        self.api_instance = TimeZone()
        self.timezone = self.api_instance.get_actuall_timezone('both')
        
        
        self.configure_layout()
        self.create_timezones_button()
        self.create_clock_and_date_frame()
        
     
        self.api_instance.display_time(timezone_str=self.timezone, widget=self.digital_clock)
        
    def configure_layout(self):
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
        self.grid_propagate(False)
       
    
    
    def create_clock_and_date_frame(self):
        
        frame = ctk.CTkFrame(self, corner_radius=5, fg_color=themes_manager.get_color("foreground_infobar"))
        frame.grid(column=0, row=1, sticky='nsew', padx=3, pady=2)
        self.grid_propagate(False)
        #fonts
        digital_clock_font = ctk.CTkFont(family='Arial Black', size=22)
        date_font = ctk.CTkFont(family='Arial Black', size=10)
        
        self.date_label = ctk.CTkLabel(frame,
                                  text=self.api_instance.get_current_date_with_weekday(self.timezone),
                                  font =date_font )
        self.date_label.pack(side='top', anchor='center', pady=5)
        
        self.digital_clock = ctk.CTkLabel(frame, font = digital_clock_font)
        self.digital_clock.pack(side='top', anchor='center')
        
      
    
    def create_timezones_button(self):
       
        self.timezones = ctk.CTkButton(self,
                                 text =f"{self.api_instance.get_actuall_timezone('region')}, {self.api_instance.get_actuall_timezone('city')}",
                                 fg_color=themes_manager.get_color("button"),
                                 hover_color=themes_manager.get_color("button_hover"),
                                 font = ctk.CTkFont(family='Arial Black', size=10), 
                                 corner_radius=5,
                                 command= self.open_time_zone_window)
        self.timezones.grid(column=0, row=0, sticky='nsew', padx=3, pady=2)
        self.timezones.grid_propagate(False)
   
    def open_time_zone_window(self):
        button_text = self.timezones.cget('text')
        self.region, self.city = button_text.split(", ")
        
        TimezonesWindow(self, self.region, self.city, self.timezone)
    
    def change_timezone(self, region, city, timezone):
        self.timezone = timezone
        self.timezones.configure(text=f"{region}, {city}")
        
        self.api_instance.stop_display_time(self.digital_clock)
        self.api_instance.start_display_time(timezone=timezone, widget=self.digital_clock)
        self.date_label.configure(self.api_instance.get_current_date_with_weekday(timezone))
        
class TimezonesWindow(ctk.CTkToplevel):
    def __init__(self, parent, region, city, timezone):
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
        # screen_width = self.winfo_screenwidth()
        # screen_height = self.winfo_screenheight()
        # center_x = int(screen_width / 2 - 700 / 2)
        # center_y = int(screen_height / 2 - 400 / 2)
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
            ctk.CTkButton(frame, text=region, fg_color=themes_manager.get_color('button'), hover_color=themes_manager.get_color('button_hover'),command=lambda region=region: self.set_region(region)).pack(side='left', padx=2, fill='both')
        
    
    def cities_frame(self, region):
        
        self.cities = self.api_instance.get_cities(region)
        self.search_var = ctk.StringVar()
        
        search_entry = ctk.CTkEntry(self, placeholder_text='Szukaj', fg_color=themes_manager.get_color('entry'), border_width=0, textvariable=self.search_var)
        search_entry.grid(column=0, columnspan=3, row=2, sticky='nsew', padx=10, pady=5)
        self.search_var.trace('w', self.filter_cities)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self.scroll_frame.grid(column=0, row=3, sticky='nsew')
        
        self.scroll_frame.columnconfigure((0,1,2), weight=1, uniform='a')
        
        self.create_cities_buttons(self.cities)
        
    
    def create_save_and_cancel_button(self):
        
        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.grid(column=0, row=4, sticky='nsew')
        
        save_button = ctk.CTkButton(frame, text='Zapisz',fg_color=themes_manager.get_color('button'), hover_color=themes_manager.get_color('button_hover'), command=self.save_button_click)
        save_button.pack(side='right', fill='both', padx=4, pady=4)
        
        cancel_button = ctk.CTkButton(frame, text='Anuluj',fg_color=themes_manager.get_color('button'), hover_color=themes_manager.get_color('button_hover'), command=lambda: self.destroy())
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
                         fg_color=themes_manager.get_color('button'),
                         hover_color=themes_manager.get_color('button_hover'),
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
        