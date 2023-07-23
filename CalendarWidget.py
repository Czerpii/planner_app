from tkcalendar import Calendar
import customtkinter as ctk


class CalendarView:
    def __init__(self, parent, col, row, on_date_select):
        
        self.cal = Calendar(parent)
        self.cal.grid(column = col, row =row, sticky='nsew')
        
        #funckja zwrotna callback
        self.cal_on_date = on_date_select
        
    
        self.cal.bind("<<CalendarSelected>>", self.print_date)

    #funkcja przekazujaca wybraną 
    def print_date(self, event):
        date = self.cal.selection_get()
        self.cal_on_date(date)
        
        
        
        
class CurrentDateWidget(ctk.CTkFrame):
    def __init__(self, parent, col, row, on_date_chosen):
        super().__init__(parent, fg_color='transparent')
        
        self.parent= parent
        self.on_date_chosen = on_date_chosen
        
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        
        self.date_label = ctk.CTkLabel(self, text='')
        self.date_label.grid(column=0, row=0)
        
        self.choose_date = ctk.CTkButton(self, text='Wybierz', command=self.close_window)
        self.choose_date.grid(column=1, row=0)
        
        self.grid(column=col, row=row, sticky='nsew')   


    def update_date(self, date):
        self.date = date
        self.date_label.configure(text=self.date)
        
        
    def close_window(self):
        if hasattr(self, 'date'):
            self.on_date_chosen(self.date)
        self.parent.destroy()
