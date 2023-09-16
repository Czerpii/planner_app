import json
import urllib.request
import csv
import os
from location.ILocationProvider import *

class ApiLocation(ILocationProvider):
    def __init__(self):
        """
        Initialize the ApiLocation class.

        This class provides location-related functionalities using API data and a CSV file.

        Attributes:
            location_file (str): The path to the CSV file storing locations.
            headers (list): The headers for the CSV file.
        """
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.location_file = os.path.join(current_path, "location.csv")
        self.headers = ["city", "state"]

        # If the location file doesn't exist, create it with headers.
        if not os.path.exists(self.location_file):
            with open(self.location_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
                file.close()

        # Retrieve location information based on the IP address.
        self.get_ip_location()

    def add_location(self, city):
        """
        Add a new location to the CSV file.

        Args:
            city (str): The name of the city to be added.
        """
        new_location = {"city": city, "state": ''}
        if not self.check_duplicate_location(new_location):
            with open(self.location_file, 'a', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writerow(new_location)
                file.close()

    def check_duplicate_location(self, new_location):
        """
        Check if a location already exists in the CSV file.

        Args:
            new_location (dict): A dictionary containing location data.

        Returns:
            bool: True if the location is a duplicate, False otherwise.
        """
        with open(self.location_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["city"] == new_location["city"]:
                    file.close()
                    return True
            file.close()
        return False

    def set_default_state(self, city):
        """
        Set a location as the default location in the CSV file.

        Args:
            city (str): The city to be set as default.
        """
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
        """
        Remove a location from the CSV file.

        Args:
            city (str): The city to be removed.
        """
        with open(self.location_file, 'r') as file:
            locations = list(csv.DictReader(file))

        locations = [location for location in locations if location["city"] != city]

        with open(self.location_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(locations)
            file.close()

    def get_location_with_default_state(self):
        """
        Get the location marked as default in the CSV file.

        Returns:
            str: The name of the location marked as default.
        """
        active_location = ""

        with open(self.location_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                if row["state"] == "default":
                    active_location = row['city']
                else:
                    if index == 0:
                        active_location = row['city']
            file.close()

        return active_location

    def get_all_location(self):
        """
        Get a list of all locations stored in the CSV file.

        Returns:
            list: A list of city names.
        """
        all_location = []

        with open(self.location_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                all_location.append(row['city'])
            file.close()

        return all_location

    def get_ip_location(self):
        """
        Get location information based on the IP address using an API.
        """
        with urllib.request.urlopen("https://ipapi.co/json/") as url:
            data = json.loads(url.read().decode())
            self.add_location(data['city'])
