from abc import ABC, abstractmethod



class IWeatherProvider(ABC):
    
    @abstractmethod
    def get_weather_today(city): 
        pass
    
    
    @abstractmethod
    def get_5_days_forecast(city, date_format):
        pass