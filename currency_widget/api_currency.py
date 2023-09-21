
import requests

class CurrencyApi:
    def __init__(self):
        """
        Initialize the CurrencyApi class.
        """
        self.api_parameters = None
        self.api_url = None


    def build_url(self, parameters):
        """
        Build a URL for the NBP (National Bank of Poland) API.

        Args:
            parameters (str): The API parameters to append to the base URL.

        Returns:
            str: The complete API URL.
        """
        return f"http://api.nbp.pl/api/exchangerates/{parameters}?format=json"
    
    def fetch_currency_table_A(self):
        """
        Fetch currency exchange rate data from NBP for table A.

        Returns:
            dict: JSON data containing currency exchange rates.
        """
        
        self.api_parameters = f"tables/A/"
        self.api_url = self.build_url(self.api_parameters)
        
        response = requests.get(self.api_url)
        if response.status_code != 200:
            print(f"Error: Unable to fetch data, status code: {response.status_code}")
            return
        
        data = response.json()
        
        return data
    
    def fetch_currnecy_rate(self, code, start_date, end_date):
        """
        Fetch currency exchange rate data for a specific currency and date range.

        Args:
            code (str): The currency code (e.g., USD).
            start_date (str): The start date for the exchange rate data (format: yyyy-mm-dd).
            end_date (str): The end date for the exchange rate data (format: yyyy-mm-dd).

        Returns:
            dict: JSON data containing currency exchange rates for the specified currency and date range.
        """
        
        self.api_parameters = f"rates/a/{code}/{start_date}/{end_date}"
        self.api_url = self.build_url(self.api_parameters)

        response = requests.get(self.api_url)
        if response.status_code != 200:
            print(f"Error: Unable to fetch data, status code: {response.status_code}")
            return
        
        data = response.json()
        
        return data

    def fetch_currency_table_C(self):
        """
        Fetch currency exchange rate data from NBP for table C.

        Returns:
            dict: JSON data containing currency exchange rates.
        """
        self.api_parameters = f"tables/C/"
        self.api_url = self.build_url(self.api_parameters)
        
        response = requests.get(self.api_url)
        if response.status_code != 200:
            print(f"Error: Unable to fetch data, status code: {response.status_code}")
            return
        
        data = response.json()
        
        return data
        