import pytz 
import time as tm
import requests
from datetime import datetime




class TimeZone():
    """
    A class for managing time zones and displaying time information.
    """
    def __init__(self):
        """
        Initializes a TimeZone instance.
        """
        self.update_time = True
        self.after_id = None
        self.api_url = "http://worldtimeapi.org/api/timezone/"
        
    def get_cities(self, region): 
        """
        Get a list of cities in the specified region.

        Args:
            region (str): The name of the region.

        Returns:
            list: A list of city names in the region.
        """
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
                print(f"Error: Unable to fetch data, status code: {response.status_code}")
                return
            
            timezones = response.json()
       
        return timezones

    def get_actuall_timezone(self, return_type = 'both'):
        """
        Get the actual (user's) timezone information.

        Args:
            return_type (str, optional): The type of information to return ('region', 'city', or 'both').

        Returns:
            str: The timezone information based on the return_type.
        """
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
        """
        Display the current time in the specified timezone.

        Args:
            timezone_str (str): The timezone identifier.
            widget: The widget to display the time.

        Notes:
            This method updates the widget with the current time every second.
        """
        if self.update_time is False:
            return 
        
        timezone = pytz.timezone(timezone_str)
        now = datetime.now(timezone)
        formatted_time = now.strftime('%H:%M:%S %p')
        widget.configure(text=formatted_time)
        self.after_id = widget.after(1000, self.display_time, timezone_str, widget)
            
    def get_current_date_with_weekday(self, timezone_str):
        """
        Get the current date with the weekday in the specified timezone.

        Args:
            timezone_str (str): The timezone identifier.

        Returns:
            str: A formatted date string including the weekday.
        """
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
        """
        Stop updating the time display.

        Args:
            widget: The widget displaying the time.
        """
        if self.after_id:
            widget.after_cancel(self.after_id)
            self.after_id = None
        self.update_time = False
        
    def start_display_time(self, timezone, widget):
        """
        Start updating the time display.

        Args:
            timezone (str): The timezone identifier.
            widget: The widget to display the time.
        """
        self.update_time = True
        self.display_time(timezone_str=timezone, widget=widget)

def show_actual_time(widget):
    """
    Display the actual time in a widget.

    Args:
        widget: The widget to display the time.

    Notes:
        This function updates the widget with the current time every 200 milliseconds.
    """
    time = tm.strftime('%H:%M:%S')
    widget.configure(text=time)
    widget.after(200, show_actual_time, widget)