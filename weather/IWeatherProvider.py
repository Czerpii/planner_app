from abc import ABC, abstractmethod



class IWeatherProvider(ABC):
    
    @abstractmethod
    def get_weather_today(city): 
        pass
       