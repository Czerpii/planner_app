
import requests

class CurrencyApi:
    def __init__(self):
    
        self.api_parameters = None
        self.api_url = None


    def build_url(self, parameters):
        return f"http://api.nbp.pl/api/exchangerates/{parameters}?format=json"
    
    
    def fetch_currency_table_A(self):
        
        self.api_parameters = f"tables/A/today"
        self.api_url = self.build_url(self.api_parameters)
        
        response = requests.get(self.api_url)
        if response.status_code != 200:
            print(f"Error: Unable to fetch data, status code: {response.status_code}")
            return
        
        data = response.json()
        
        return data
    
    def fetch_currnecy_rate(self, code, start_date, end_date):
        
        self.api_parameters = f"rates/a/{code}/{start_date}/{end_date}"
        self.api_url = self.build_url(self.api_parameters)

        response = requests.get(self.api_url)
        if response.status_code != 200:
            print(f"Error: Unable to fetch data, status code: {response.status_code}")
            return
        
        data = response.json()
        
        return data

    def fetch_currency_table_C(self):
        self.api_parameters = f"tables/C/today"
        self.api_url = self.build_url(self.api_parameters)
        
        response = requests.get(self.api_url)
        if response.status_code != 200:
            print(f"Error: Unable to fetch data, status code: {response.status_code}")
            return
        
        data = response.json()
        
        return data
        