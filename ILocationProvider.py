from abc import ABC, abstractclassmethod

class ILocationProvider(ABC):
    @abstractclassmethod
    def __init__(self):
        pass

    @abstractclassmethod       
    def add_location(self, city,):
        pass
    
    @abstractclassmethod 
    def check_duplicate_location(self, new_location):
        pass
    
    @abstractclassmethod     
    def set_default_state(self, city):
        pass
    
    @abstractclassmethod
    def remove_location(self, city):
        pass
    
    @abstractclassmethod
    def get_location_with_default_state(self):
        pass
    
    @abstractclassmethod 
    def get_all_location(self):
        pass
    
    @abstractclassmethod
    def get_ip_location(self):
        pass
