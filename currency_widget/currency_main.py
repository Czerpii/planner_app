
import customtkinter as ctk

from .ui_components import CurrencyCalculatorUI, CurrencyHistoryUi


class CurrencyMain(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew")
        
        
        self.configure_layout()
        
        
        self.currency_calculator = CurrencyCalculatorUI(self, col=1, row=0)
        self.currency_history = CurrencyHistoryUi(self, col=1, row=1)
        
        
      
    def configure_layout(self):
        self.columnconfigure((0,2), weight=1, uniform='a')
        self.columnconfigure(1, weight=20, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
    
