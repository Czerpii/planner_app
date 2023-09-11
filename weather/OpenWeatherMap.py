import requests
from settings import *
from weather.IWeatherProvider import*
from datetime import datetime, date
import ssl

URL_WEATHER = 'https://api.openweathermap.org/data/2.5/'
API_WEATHER = 'a512baaa1f7ebef4371ae61a46eca628'


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
                    today_data['weather_main'] = value[0]['main']
                    today_data['weather_ico'] = value[0]['icon']
            return today_data      
        else:
            print(f"Error {response.status_code}: Unable to fetch data.")
            return None
        
           
        
    
    
    def get_5_days_forecast(city, date_format):
        full_url = f"{URL_WEATHER}forecast?q={city}&appid={API_WEATHER}&units=metric&lang=pl"
        response = requests.get(full_url)
        
        forecast_data = {}
        
        if response.status_code == 200:
            data = response.json()
            today = date.today()
            for entry in data['list']:
                date_str = entry['dt_txt'].split()[0]  # Wyciągnięcie daty z formatu "YYYY-MM-DD HH:MM:SS"
                entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                
                # Pomijanie wpisów z dzisiejszą datą
                if entry_date <= today:
                    continue
                
                formatted_date = date_format(date_str)  # Formatowanie daty
                temp = entry['main']['temp']
                icon = entry['weather'][0]['icon']
                
                if formatted_date not in forecast_data:
                    forecast_data[formatted_date] = {"temperatures": [], "icons": []}
                
                forecast_data[formatted_date]['temperatures'].append(temp)
                forecast_data[formatted_date]['icons'].append(icon)
            
            # Obliczenie średniej temperatury i wybranie najczęstszej ikonki dla każdego dnia
            result = {}
            for date1, values in forecast_data.items():
                avg_temp = sum(values['temperatures']) / len(values['temperatures'])
                # Wybieranie najczęstszej ikonki (w tym przypadku po prostu pierwszej z listy dla uproszczenia)
                icon = values['icons'][0]
                
                result[date1] = {
                    "średnia_temperatura": int(round(avg_temp)),
                    "icon": icon
                }
            
            return result

        else:
            print(f"Error {response.status_code}: Unable to fetch data.")
            return None
                
                
    