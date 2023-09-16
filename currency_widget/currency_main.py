import customtkinter as ctk
from .ui_components import CurrencyCalculatorUI, CurrencyHistoryUi

class CurrencyMain(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        """
        Initialize the CurrencyMain class.

        Args:
            parent: The parent widget.
            col (int): The column to place the widget in.
            row (int): The row to place the widget in.
        """
        super().__init__(parent, fg_color="transparent")
        self.grid(column=col, row=row, sticky="nsew")

        self.configure_layout()

        # Create currency calculator and history components
        self.currency_calculator = CurrencyCalculatorUI(self, col=1, row=0)
        self.currency_history = CurrencyHistoryUi(self, col=1, row=1)

    def configure_layout(self):
        """
        Configure the layout of the CurrencyMain widget.
        """
        self.columnconfigure((0, 2), weight=1, uniform='a')
        self.columnconfigure(1, weight=20, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
