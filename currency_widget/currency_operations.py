
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from .api_currency import CurrencyApi


class  CurrencyConverter:
    def __init__(self):
        
        self.api = CurrencyApi()
        
    
    
    def get_currency_code_and_name(self):
        
        data = self.api.fetch_currency_table_A()
        
        currencies = data[0]['rates']
        
        currencies_list = [f"{currency['code']} - {currency['currency']}" for currency in currencies]
        currencies_list.insert(0, "PLN - polski złoty")

        return currencies_list

    
    def get_currency_rates(self):
        data = self.api.fetch_currency_table_A()
        
        currency_rates = {rate['code']: rate['mid'] for rate in data[0]['rates']}
        
        return currency_rates

    def get_rate_for_code(self, data, code):
        
        if code == "PLN":
            return 1
        return data.get(code)
    
    def convert_between_currencies(self, amount: float, from_code: str, to_code: str):
        
        data = self.get_currency_rates()
        
        from_rate = self.get_rate_for_code(data, from_code)
        to_rate = self.get_rate_for_code(data, to_code)
        
        
        result = round(amount * from_rate / to_rate, 2)
        formatted_result = "{:.2f}".format(result)
        
        return formatted_result
            
        
        
        
            
class CurrencyHistoryAnalyzer:
    def __init__(self):
        
        self.api = CurrencyApi()
        
        
    
    def get_currency_code(self):
        
        data = self.api.fetch_currency_table_A()
        
        currencies = data[0]['rates']
        
        currencies_list = [f"{currency['code']}" for currency in currencies]
        currencies_list.insert(0, "PLN")

        return currencies_list

    def get_currency_rate(self, from_code, to_code, start_date, end_date):
        
        if from_code == "PLN":
            from_dict = {date: 1 for date in self.get_dates_between(start_date, end_date)}
        else:
            from_data = self.api.fetch_currnecy_rate(from_code, start_date, end_date)
            from_dict = {entry["effectiveDate"]: entry["mid"] for entry in from_data["rates"]}

        if to_code == "PLN":
            to_dict = {date: 1 for date in self.get_dates_between(start_date, end_date)}
        else:
            to_data = self.api.fetch_currnecy_rate(to_code, start_date, end_date)
            to_dict = {entry["effectiveDate"]: entry["mid"] for entry in to_data["rates"]}
            
        return self._convert_currency_series(from_dict, to_dict)
            
    def _convert_currency_series(self, source_data, target_data):
        result = {}
            
        for date, source_value in source_data.items():
            target_value = target_data.get(date)
                    
            if target_value is None or source_value is None:
                continue
                
            conversion_rate = source_value / target_value
            result[date] = conversion_rate

        return result   
    
    def get_dates_formatted(self):
        today = date.today()
        one_week_ago = today - timedelta(weeks=1)
        one_month_ago = today - relativedelta(months=1)
        one_year_ago = today - relativedelta(years=1)

        return {
            'today': today.strftime('%Y-%m-%d'),
            'one_week_ago': one_week_ago.strftime('%Y-%m-%d'),
            'one_month_ago': one_month_ago.strftime('%Y-%m-%d'),
            'one_year_ago': one_year_ago.strftime('%Y-%m-%d')
        }
    
    def get_dates_between(self, start_date, end_date):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        date_list = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
        return [date.strftime('%Y-%m-%d') for date in date_list]
            

    def get_currency_from_c(self):
        data = self.api.fetch_currency_table_C()
        
        temp = data[0]['rates']
        
        currencies_codes = [f"{code['code']}" for code in temp]
        sell_rate = [f"{sell['ask']}" for sell in temp]
        buy_rate = [f"{buy['bid']}" for buy in temp]
        
        return currencies_codes, buy_rate, sell_rate