import pytz
from datetime import datetime
import time
import requests

# api_url = "http://worldtimeapi.org/api/"

# def display_time(timezone_str):
#     timezone = pytz.timezone(timezone_str)
    
#     while True:
#         now = datetime.now(timezone)
#         print(now.strftime('%Y-%m-%d %H:%M:%S'))
#         time.sleep(1)  # Opóźnienie 1 sekunda
        
# display_time("America/Mexico_City")



# response = requests.get(f"{api_url}ip")    
# return_request = response.json()
# default_tm = return_request.get("timezone")
# print(default_tm)
        
# api_url = "http://worldtimeapi.org/api/timezone/"
   
# response = requests.get(f"{api_url}America")


# timezones = response.json()
# print(timezones)
# print("/n")     
# timezones = [tz for tz in timezones if tz in pytz.all_timezones]
# print([pytz.all_timezones])
# cities = [timezone.split('/')[1] for timezone in timezones]
# cities = [city.replace('_', ' ') for city in cities]

timezone = pytz.timezone("America/Mexico_City")
now = datetime.now(timezone)

print(now)
