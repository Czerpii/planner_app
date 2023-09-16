# import pytz
# from datetime import datetime
# import time
# import requests

# # api_url = "http://worldtimeapi.org/api/"

# # def display_time(timezone_str):
# #     timezone = pytz.timezone(timezone_str)
    
# #     while True:
# #         now = datetime.now(timezone)
# #         print(now.strftime('%Y-%m-%d %H:%M:%S'))
# #         time.sleep(1)  # Opóźnienie 1 sekunda
        
# # display_time("America/Mexico_City")



# # response = requests.get(f"{api_url}ip")    
# # return_request = response.json()
# # default_tm = return_request.get("timezone")
# # print(default_tm)
        
# # api_url = "http://worldtimeapi.org/api/timezone/"
   
# # response = requests.get(f"{api_url}America")


# # timezones = response.json()
# # print(timezones)
# # print("/n")     
# # timezones = [tz for tz in timezones if tz in pytz.all_timezones]
# # print([pytz.all_timezones])
# # cities = [timezone.split('/')[1] for timezone in timezones]
# # # cities = [city.replace('_', ' ') for city in cities]

# # timezone = pytz.timezone("America/Mexico_City")
# # now = datetime.now(timezone)

# # print(now)

# import requests
# from datetime import datetime, date



# URL_WEATHER = 'https://api.openweathermap.org/data/2.5/'
# API_WEATHER = 'a512baaa1f7ebef4371ae61a46eca628'

# def format_date(date_str):
#     # Przekształć łańcuch daty na obiekt datetime
#     date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
#     # Polskie nazwy dni tygodnia i miesięcy
#     days_pl = ["pon.", "wt.", "śr.", "czw.", "pt.", "sob.", "niedz."]
#     months_pl = ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paź", "lis", "gru"]
    
#     # Sformatuj datę zgodnie z pożądanym formatem w języku polskim
#     formatted_date = f"{days_pl[date_obj.weekday()]}, {date_obj.day} {months_pl[date_obj.month-1]}"
    
#     return formatted_date

# ef get_5_days_forecast(city):
#     full_url = f"{URL_WEATHER}forecast?q={city}&appid={API_WEATHER}&units=metric&lang=pl"
#     response = requests.get(full_url)
    
#     forecast_data = {}
    
#     if response.status_code == 200:
#         data = response.json()
#         today = date.today()
#         for entry in data['list']:
#             date_str = entry['dt_txt'].split()[0]  # Wyciągnięcie daty z formatu "YYYY-MM-DD HH:MM:SS"
#             entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
#             # Pomijanie wpisów z dzisiejszą datą
#             if entry_date <= today:
#                 continue
            
#             formatted_date = format_date(date_str)  # Formatowanie daty
#             temp = entry['main']['temp']
#             icon = entry['weather'][0]['icon']
            
#             if formatted_date not in forecast_data:
#                 forecast_data[formatted_date] = {"temperatures": [], "icons": []}
            
#             forecast_data[formatted_date]['temperatures'].append(temp)
#             forecast_data[formatted_date]['icons'].append(icon)
        
#         # Obliczenie średniej temperatury i wybranie najczęstszej ikonki dla każdego dnia
#         result = {}
#         for date1, values in forecast_data.items():
#             avg_temp = sum(values['temperatures']) / len(values['temperatures'])
#             # Wybieranie najczęstszej ikonki (w tym przypadku po prostu pierwszej z listy dla uproszczenia)
#             icon = values['icons'][0]
            
#             result[date1] = {
#                 "średnia_temperatura": round(avg_temp, 2),
#                 "icon": icon
#             }
        
#         return result

#     else:
#         print(f"Error {response.status_code}: Unable to fetch data.")
#         return None

# # Test
# city_name = "Nowy Sącz"
# forecast = get_5_days_forecast(city_name)
# print(forecast)
# d

# import tkinter as tk
# from tkinter import ttk

# def update_combobox_options(event):
#     current_text = combobox.get()
#     global last_text

#     # Sprawdź, czy tekst się zmienił, aby uniknąć rekursji
#     if current_text != last_text:
#         last_text = current_text

#         # Filtrowanie opcji
#         filtered_options = [option for option in all_options if current_text.lower() in option.lower()]
        
#         # Aktualizacja dostępnych opcji
#         combobox["values"] = filtered_options

# root = tk.Tk()

# # Lista wszystkich dostępnych opcji
# all_options = ["Opcja 1", "Opcja 2", "Opcja 3", "Opcja 4"]

# combobox = ttk.Combobox(root, values=all_options)
# combobox.pack(pady=20, padx=20)

# # Ustawienie początkowej wartości dla globalnej zmiennej
# last_text = ""

# # Dodanie funkcji obsługi dla zdarzenia zmiany tekstu
# combobox.bind('<KeyRelease>', update_combobox_options)

# root.mainloop()

# parameters = ""

# api = f"http://api.nbp.pl/api/exchangerates/{parameters}?format=json"

# parameters= "tables"
# api = f"http://api.nbp.pl/api/exchangerates/{parameters}?format=json"
# print(api)

# import matplotlib.pyplot as plt

# def plot_currency_rate_over_time(data, currency_code):
#     # Pobierz daty i kursy dla podanej waluty
#     dates = [item['effectiveDate'] for item in data if currency_code in [rate['code'] for rate in item['rates']]]
#     rates = [rate['mid'] for item in data for rate in item['rates'] if rate['code'] == currency_code]

#     # Stwórz wykres
#     plt.figure(figsize=(15, 7))
#     plt.plot(dates, rates, marker='o', linestyle='-', color='blue')
#     plt.xlabel('Data')
#     plt.ylabel('Kurs wobec PLN')
#     plt.title(f'Kurs {currency_code} wobec PLN w czasie')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.grid(True)
#     plt.show()

# # Przykładowe dane
# data = [
#     {
#         "table":"A",
#         "no":"175/A/NBP/2023",
#         "effectiveDate":"2023-09-11",
#         "rates":[
#             {"currency":"dolar amerykański","code":"USD","mid":4.3410},
#             {"currency":"euro","code":"EUR","mid":4.6305},
#         ]
#     },
#     {
#         "table":"A",
#         "no":"176/A/NBP/2023",
#         "effectiveDate":"2023-09-12",
#         "rates":[
#             {"currency":"dolar amerykański","code":"USD","mid":4.3420},
#             {"currency":"euro","code":"EUR","mid":4.6310},
#         ]
#     },
#     {
#         "table":"A",
#         "no":"177/A/NBP/2023",
#         "effectiveDate":"2023-09-13",
#         "rates":[
#             {"currency":"dolar amerykański","code":"USD","mid":4.3430},
#             {"currency":"euro","code":"EUR","mid":4.6320},
#         ]
#     },
#     {
#         "table":"A",
#         "no":"178/A/NBP/2023",
#         "effectiveDate":"2023-09-14",
#         "rates":[
#             {"currency":"dolar amerykański","code":"USD","mid":4.3440},
#             {"currency":"euro","code":"EUR","mid":4.6330},
#         ]
#     },
# ]

# # Wywołanie funkcji
# plot_currency_rate_over_time(data, 'USD')

# import tkinter as tk
# from tkinter import Frame
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# class CurrencyPlotter(Frame):
#     def __init__(self, master=None, **kwargs):
#         super().__init__(master, **kwargs)
#         self.grid()
#         self.create_widgets()

#     def create_widgets(self):
#         # Tworzenie przykładowego wykresu
#         figure = plt.Figure(figsize=(6, 4), dpi=100)
#         ax = figure.add_subplot(111)
#         ax.plot(np.arange(10), np.random.rand(10))
#         ax.set_title("Przykładowy wykres")

#         # Umieszczanie wykresu w oknie Tkinter
#         canvas = FigureCanvasTkAgg(figure, self)
#         canvas.draw()
#         canvas.get_tk_widget().grid(row=0, column=0)

# root = tk.Tk()
# root.title("Wykres w Tkinter")
# app = CurrencyPlotter(master=root)
# app.mainloop()
# from datetime import date, timedelta
# from dateutil.relativedelta import relativedelta

# def get_dates_formatted():
#     today = date.today()
#     one_week_ago = today - timedelta(weeks=1)
#     one_month_ago = today - relativedelta(months=1)
#     one_year_ago = today - relativedelta(years=1)

#     return {
#         'today': today.strftime('%Y-%m-%d'),
#         'one_week_ago': one_week_ago.strftime('%Y-%m-%d'),
#         'one_month_ago': one_month_ago.strftime('%Y-%m-%d'),
#         'one_year_ago': one_year_ago.strftime('%Y-%m-%d')
#     }

# print(get_dates_formatted())

# def extract_date_and_mid(data):
#     return {entry["effectiveDate"]: entry["mid"] for entry in data["rates"]}

# # Przykład użycia:
# data = {"table":"A","currency":"funt szterling","code":"GBP","rates":[{"no":"157/A/NBP/2023","effectiveDate":"2023-08-16","mid":5.2091},{"no":"158/A/NBP/2023","effectiveDate":"2023-08-17","mid":5.2240},{"no":"159/A/NBP/2023","effectiveDate":"2023-08-18","mid":5.2515},{"no":"160/A/NBP/2023","effectiveDate":"2023-08-21","mid":5.2317},{"no":"161/A/NBP/2023","effectiveDate":"2023-08-22","mid":5.2306},{"no":"162/A/NBP/2023","effectiveDate":"2023-08-23","mid":5.2539},{"no":"163/A/NBP/2023","effectiveDate":"2023-08-24","mid":5.2291},{"no":"164/A/NBP/2023","effectiveDate":"2023-08-25","mid":5.2128},{"no":"165/A/NBP/2023","effectiveDate":"2023-08-28","mid":5.2065},{"no":"166/A/NBP/2023","effectiveDate":"2023-08-29","mid":5.2132},{"no":"167/A/NBP/2023","effectiveDate":"2023-08-30","mid":5.2023},{"no":"168/A/NBP/2023","effectiveDate":"2023-08-31","mid":5.2158},{"no":"169/A/NBP/2023","effectiveDate":"2023-09-01","mid":5.2301},{"no":"170/A/NBP/2023","effectiveDate":"2023-09-04","mid":5.2241},{"no":"171/A/NBP/2023","effectiveDate":"2023-09-05","mid":5.2203},{"no":"172/A/NBP/2023","effectiveDate":"2023-09-06","mid":5.2626},{"no":"173/A/NBP/2023","effectiveDate":"2023-09-07","mid":5.3518},{"no":"174/A/NBP/2023","effectiveDate":"2023-09-08","mid":5.3645},{"no":"175/A/NBP/2023","effectiveDate":"2023-09-11","mid":5.3926},{"no":"176/A/NBP/2023","effectiveDate":"2023-09-12","mid":5.4495},{"no":"177/A/NBP/2023","effectiveDate":"2023-09-13","mid":5.3931},{"no":"178/A/NBP/2023","effectiveDate":"2023-09-14","mid":5.3845},{"no":"179/A/NBP/2023","effectiveDate":"2023-09-15","mid":5.4005}]}
# result = extract_date_and_mid(data)
# print(result)
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

style = ttk.Style()
style.configure("Treeview", 
                font=('San Francisco', 10), 
                foreground="black", 
                background="gray",  # Kolor tła Treeview (działa jako kolor linii)
                fieldbackground="lightblue", 
                rowheight=25)

tree = ttk.Treeview(root, columns=("Spacer1", "Column1", "Spacer2", "Column2"), show='headings')
tree.column("Spacer1", width=2, stretch=tk.NO)
tree.column("Column1", width=100)
tree.column("Spacer2", width=2, stretch=tk.NO)
tree.column("Column2", width=100)

tree.heading("Column1", text="Nagłówek 1")
tree.heading("Column2", text="Nagłówek 2")

# Ustawienie koloru tła dla wierszy
tree.tag_configure("rowColor", background="white")

tree.insert("", "end", values=("", "Wartość 1", "", "Wartość 2"), tags=("rowColor",))
tree.insert("", "end", values=("", "Wartość 3", "", "Wartość 4"), tags=("rowColor",))

tree.pack(fill='both', expand=True)

root.mainloop()
