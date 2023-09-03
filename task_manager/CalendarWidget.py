from tkcalendar import Calendar
import customtkinter as ctk
import tkinter as tk

class CalendarDateEntry:
    def __init__(self, parent, on_date_select):
        
        self.cal = Calendar(parent, 
                            locale = 'pl_PL',
                            showweeknumbers = False,
                            showothermonthdays = False,
                            borderwidth = 0, 
                            background = '#2F2F2F',
                            headersbackground ="#2F2F2F",
                            headersforeground = "WHITE",
                            normalbackground = '#2F2F2F',
                            normalforeground = 'WHITE',
                            weekendbackground = '#2F2F2F',
                            weekendforeground = 'WHITE',
                            othermonthbackground = '#2F2F2F',
                            othermonthforeground = '#1F1F1F',
                            bordercolor = '#2F2F2F'
                            )
        self.cal.pack(fill='both', expand='true')
        
    
        
        #funckja zwrotna callback
        self.cal_on_date = on_date_select
        
        
        #event wybrania daty z kalendarza
        self.cal.bind("<<CalendarSelected>>", self.print_date)

    #funkcja przekazujaca wybraną 
    def print_date(self, event):
        date = self.cal.selection_get()
        formatted_date = date.strftime('%d-%m-%Y') # Konwersja na format 'dd-mm-yyyy'
        self.cal_on_date(formatted_date)
        
