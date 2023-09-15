
import customtkinter as ctk
from controller import CurrencyController


class CurrencyCalculatorUI(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color='black')
        self.grid(column = col, row=row, sticky = "nsew")

        self.configure_layout()
        self.conversion_view()
        self.result_view()

    def configure_layout(self):
        self.columnconfigure((0,1), weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
   
    def conversion_view(self):
        frame = ctk.CTkFrame(self, fg_color='transparent', border_width=2, corner_radius=10)
        frame.grid(column=0, row=0, sticky='nsew', padx=10, pady=10 )
        
        #layout
        frame.columnconfigure((0,2), weight=1, uniform='a')
        frame.columnconfigure(1, weight=10, uniform='a')
        frame.rowconfigure((0,8), weight=1, uniform='a')
        frame.rowconfigure((1,3,5), weight=3, uniform='a')
        frame.rowconfigure((2,4,6,7), weight=6, uniform='a')
        
        #labels
        self.create_conversion_labels(frame, col=1, row=[1,3,5])
        self.create_parameters_entry(frame, col=1, row=[2,4,6])
        self.create_action_buttons(frame, col=1, row=7)
    
    
    def result_view(self):
        frame = ctk.CTkFrame(self, fg_color='transparent', border_width=2, corner_radius=10)
        frame.grid(column=1, row=0, sticky='nsew', padx=10, pady=10)
    
    
    def create_conversion_labels(self, parent, col, row):
        
        font = ctk.CTkFont(family='Arial', size=15)
        ctk.CTkLabel(parent, text="Kwota:", font=font, corner_radius=10).grid(column=col, row=row[0], sticky='nsw')
        ctk.CTkLabel(parent, text="Przelicz z:", font=font, corner_radius=10).grid(column=col, row=row[1], sticky='nw')
        ctk.CTkLabel(parent, text="Przelicz na:",font=font, corner_radius=10).grid(column=col, row=row[2], sticky='nw')
    
        
    def create_parameters_entry(self, parent, col, row):
        
        self.entry_value = ctk.CTkEntry(parent, placeholder_text='Podaj kwotę')
        self.entry_value.grid(column=col, row=row[0], sticky='new',padx=10)
        
        self.convert_from = ctk.CTkComboBox(parent)
        self.convert_from.grid(column=col, row=row[1], sticky='new',padx=10)
        
        self.convert_to = ctk.CTkComboBox(parent)
        self.convert_to.grid(column=col, row=row[2], sticky='new',padx=10)

    def create_action_buttons(self, parent, col, row):
        
        frame_button = ctk.CTkFrame(parent, fg_color='transparent')
        frame_button.grid(column=col, row=row, sticky='nsew')
        frame_button.columnconfigure((0,1), weight=1, uniform='a')
        frame_button.rowconfigure(0, weight=1, uniform='a')
        
        self.clear_button = ctk.CTkButton(frame_button, text='Wyczyść', command=self.clear_button_click)
        self.clear_button.grid(column=0, row=0, sticky='ew', padx=5)

        self.calculate_button = ctk.CTkButton(frame_button, text='Oblicz', command=self.calculate_button_click)
        self.calculate_button.grid(column=1, row=0, sticky='ew', padx=5)
    

    def clear_button_click(self):
        pass
    
    def calculate_button_click(self):
        pass
    