import requests
from settings import *
from weather.IWeatherProvider import*
import ssl


#wyłaczenie certyfikacji - potrzebne do działania na macos
ssl._create_default_https_context = ssl._create_unverified_context
    
class OpenWeaterMap(IWeatherProvider):

    
    def get_weather_today(city): 
        
        
        full_url = f"{URL_WEATHER}weather?q={city}&appid={API_WEATHER}&units=metric&lang=pl"
        response = requests.get(full_url)
        
        today_data={}
        
        if response.status_code == 200:
            data = response.json()
            
            for key, value in data.items():
                if key =='main':
                    today_data['temp'] = int(round(value['temp'],0))
                    today_data['feels_like'] = int(round(value['feels_like'],0))
                    today_data['pressure'] = int(value['pressure'])
                    today_data['humidity'] = int(value['humidity'])
                
                if key == 'wind':
                    today_data['wind'] = float(value['speed'])
                    
                if key == 'weather':
                    today_data['description'] = value[0]['description']
            
        return today_data    
        
