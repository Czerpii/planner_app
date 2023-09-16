from .currency_operations import CurrencyConverter, CurrencyHistoryAnalyzer

class CurrencyController:
    def __init__(self):
        """
        Initialize the CurrencyController class with a CurrencyConverter and CurrencyHistoryAnalyzer.
        """
        self.converter = CurrencyConverter()
        self.analyzer = CurrencyHistoryAnalyzer()
    
    def get_currency_code_and_name(self):
        """
        Get a dictionary of currency codes and their names.

        Returns:
            dict: A dictionary mapping currency codes to their names.
        """
        return self.converter.get_currency_code_and_name()

    def convert_currencies(self, amount, from_code, to_code):
        """
        Convert an amount from one currency to another.

        Args:
            amount (float): The amount to convert.
            from_code (str): The source currency code.
            to_code (str): The target currency code.

        Returns:
            float: The converted amount.
        """
        return self.converter.convert_between_currencies(amount, from_code, to_code)

    def get_currency_code(self):
        """
        Get the currency code used by the CurrencyHistoryAnalyzer.

        Returns:
            str: The currency code.
        """
        return self.analyzer.get_currency_code()

    def get_currency_rate(self, from_code, to_code, start_date, end_date):
        """
        Get historical currency exchange rates for a specific currency pair and date range.

        Args:
            from_code (str): The source currency code.
            to_code (str): The target currency code.
            start_date (str): The start date for the exchange rate data (format: yyyy-mm-dd).
            end_date (str): The end date for the exchange rate data (format: yyyy-mm-dd).

        Returns:
            dict: Historical exchange rates for the specified currency pair and date range.
        """
        return self.analyzer.get_currency_rate(from_code, to_code, start_date, end_date)

    def get_dates(self):
        """
        Get formatted dates from the CurrencyHistoryAnalyzer.

        Returns:
            list: A list of formatted date strings.
        """
        return self.analyzer.get_dates_formatted()

    def get_sell_and_but_rate(self):
        """
        Get currency buy and sell rates from the CurrencyHistoryAnalyzer.

        Returns:
            dict: Buy and sell rates for the currency.
        """
        return self.analyzer.get_currency_from_c()
