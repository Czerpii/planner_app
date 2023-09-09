import pytz 
import time as tm
import requests
from datetime import datetime




class TimeZone():
    def __init__(self):
        self.update_time = True
        self.after_id = None
        self.api_url = "http://worldtimeapi.org/api/timezone/"
        
    def get_cities(self, region): 
        
        if region == "Oceania":
            response = requests.get(f"{self.api_url}Australia")
            response1 = requests.get(f"{self.api_url}Atlantic")
            response2 = requests.get(f"{self.api_url}Pacific")
            
            timezones0 = response.json()
            timezones1 = response1.json()
            timezones2 = response2.json()
            timezones = timezones0 + timezones1 + timezones2
              
        else:    
            response = requests.get(f"{self.api_url}{region}")
            if response.status_code != 200:
                return []
            
            timezones = response.json()
       
        return timezones

    def get_actuall_timezone(self, return_type = 'both'):
        
        response = requests.get("http://worldtimeapi.org/api/ip")    
        return_request = response.json()
        default_tm = return_request.get("timezone")
        region, city = default_tm.split('/')
        
        if return_type == "region":
            return region
        elif return_type == "city":
            return city
        elif return_type == "both":
            return default_tm
        else:
            raise ValueError("Invalid return_type. Choose from 'region', 'city', or 'both'.")
            
    
    def display_time(self, timezone_str, widget):
       
        if self.update_time == False:
            return 
        
        timezone = pytz.timezone(timezone_str)
        now = datetime.now(timezone)
        formatted_time = now.strftime('%H:%M:%S %p')
        widget.configure(text = formatted_time)
        self.after_id = widget.after(1000, self.display_time, timezone_str, widget)
            
    def get_current_date_with_weekday(self, timezone_str):
        days_translation = {
        'Monday': 'Poniedziałek',
        'Tuesday': 'Wtorek',
        'Wednesday': 'Środa',
        'Thursday': 'Czwartek',
        'Friday': 'Piątek',
        'Saturday': 'Sobota',
        'Sunday': 'Niedziela'
    }
    
        timezone = pytz.timezone(timezone_str)
        current_datetime = datetime.now(timezone)
        day_english = current_datetime.strftime('%A')
        day_polish = days_translation[day_english]
        
        formatted_date = current_datetime.strftime(f'{day_polish} %d-%m-%Y')
        return formatted_date
        
    
    
    def stop_display_time(self, widget):
        if self.after_id:
            widget.after_cancel(self.after_id)
            self._after_id = None
        self.update_time = False
        
        
    def start_display_time(self, timezone, widget):
        self.update_time=True
        self.display_time(timezone_str=timezone, widget=widget)
        


def show_actuall_time(widget):
        time = tm.strftime('%H:%M:%S')
        widget.configure(text = time)
        widget.after(200, show_actuall_time, widget)