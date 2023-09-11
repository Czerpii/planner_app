import json
import urllib.request
import csv
import os
from location.ILocationProvider import *




class ApiLocation(ILocationProvider):
    def __init__(self):
        
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.location_file = os.path.join(current_path, "location.csv")
        self.headers = ["city", "state"]

        if not os.path.exists(self.location_file):
            with open(self.location_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
                file.close()   
        self.get_ip_location()
           
    def add_location(self, city,):
        new_location = {"city": city, "state": ''}
        if not self.check_duplicate_location(new_location):
            with open(self.location_file, 'a', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writerow(new_location)
                file.close()
    
    def check_duplicate_location(self, new_location):
        with open(self.location_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["city"] == new_location["city"]:
                    file.close()
                    return True
            file.close()    
        return False
         
    def set_default_state(self, city):
        with open(self.location_file, 'r', encoding='utf-8') as file:
            locations = list(csv.DictReader(file))

        
        for location in locations:
            if location["city"] == city:
                location["state"] = 'default'
                
            else:
                location['state'] = ' '

        with open(self.location_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(locations)
            file.close()
  
    def remove_location(self, city):
        with open(self.location_file, 'r') as file:
            locations = list(csv.DictReader(file))
        
        locations = [location for location in locations if location["city"] != city]
        
        with open(self.location_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(locations)
            file.close()
     
    def get_location_with_default_state(self):
        # active_location = []
        
        with open(self.location_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                    if row["state"] == "default":
                        active_location =(f"{row['city']}")
                    else:
                        if index == 0:
                            active_location =(f"{row['city']}")
            file.close()
        
        
        return active_location
      
    def get_all_location(self):
        all_location = []
        
        with open(self.location_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                all_location.append(f"{row['city']}")       
            file.close()
        return all_location
             
    def get_ip_location(self):
        with urllib.request.urlopen("https://ipapi.co/json/") as url:
            data = json.loads(url.read().decode())
            self.add_location(data['city'])
                  

# loc = IpapiLocation()
# loc.get_all_location()
