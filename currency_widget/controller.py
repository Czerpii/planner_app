
from .currency_operations import CurrencyConverter, CurrencyHistoryAnalyzer



class CurrencyController:
    
    def __init__(self):
        
        self.converter = CurrencyConverter()
        self.analyzer = CurrencyHistoryAnalyzer()
        
        
    
    def get_currency_code_and_name(self):
        return self.converter.get_currency_code_and_name()

    def convert_currencies(self,amount, from_code, to_code):
        return self.converter.convert_between_currencies(amount, from_code, to_code)
    
    def get_currency_code(self):
        return self.analyzer.get_currency_code()

    def get_currency_rate(self, from_code, to_code, start_date, end_date):
        return self.analyzer.get_currency_rate(from_code, to_code, start_date, end_date)
    
    def get_dates(self):
        return self.analyzer.get_dates_formatted()
    
    def get_sell_and_but_rate(self):
        return self.analyzer.get_currency_from_c()
        