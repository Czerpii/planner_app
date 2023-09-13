from typing import Optional, Tuple, Union
from datetime import timedelta, date
from tkcalendar import Calendar
import customtkinter as ctk
import tkinter as tk



class DeadlineWindow(ctk.CTkToplevel):
    def __init__(self, parent, widget, callback_func):
        super().__init__(parent )
        
        self.parent = parent
        self.widget= widget
        self.callback = callback_func
        
        self.setup_window()
        self.setup_variables()
        self.configure_layout()
        self.show_widgets()
        
    
    def setup_window(self):
        x_pos = self.widget.winfo_rootx()
        y_pos = self.widget.winfo_rooty()-100
        self.geometry(f'300x500+{x_pos}+{y_pos}')
        self.lift(self.parent)
        self.transient(self.parent)
                
    def configure_layout(self):
        self.columnconfigure((0,1), weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=6, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        self.rowconfigure(3, weight=1, uniform='a')
        self.rowconfigure(4, weight=1, uniform='a')
        # self.grid_propagate(False)
    
    def setup_variables(self):
        self.switch_date_var = ctk.StringVar(value="off")
        self.switch_time_var = ctk.StringVar(value="off")
        self.start_time_var = ctk.StringVar(value='__:__')
        self.end_time_var = ctk.StringVar(value="__:__")
        
        self.start_date_selected = True
        self.c1 = None
        self.c2 = None
        self.callback_data = {}

    def show_widgets(self):
        self.create_info_frame()  
        self.calendar_widget()
        self.create_start_date_widget(col=0, row=0)
        self.create_date_switch()
        self.create_time_switch()
        self.create_action_buttons()
        
    #Create widgets                    
    def calendar_widget(self):
        self.calendar = Calendar(self, 
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
        self.calendar.grid(column=0, row=1, columnspan=2, sticky='nsew', padx=10, pady=3)
        self.calendar.bind("<<CalendarSelected>>", self.on_date_select)
        
    def on_date_select(self, event):
        selected_date = self.calendar.selection_get()
        self.start_date.delete(0,'end')
        self.start_date.insert("end", self.format_date(selected_date))

    def on_date_range_select(self, event):
        
        if self.c1 and self.c2:
            self.calendar.calevent_remove('all')
            self.c1, self.c2 = None, None
            self.start_date_selected = True

        if self.start_date_selected:
            self.c1 = self.calendar.selection_get()
            self.calendar.calevent_create(self.c1, 'highlighted')
            self.start_date.delete(0,'end')
            self.start_date.insert("end", self.format_date(self.c1))
            self.start_date_selected = False
        else:
            self.c2 = self.calendar.selection_get()
            self.calendar.calevent_create(self.c2, 'highlighted')
            self.start_date_selected = True

        if self.c1 and self.c2:
            start_date = min(self.c1, self.c2)
            end_date = max(self.c1, self.c2)
            self.start_date.delete(0,'end')
            self.start_date.insert("end", self.format_date(start_date))
            self.end_date.delete(0,'end')
            self.end_date.insert("end", self.format_date(end_date))
      
    def create_info_frame(self):
        self.info_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.info_frame.grid(column=0, row=0, columnspan=2, sticky='nsew')
        self.info_frame.columnconfigure(0, weight=1, uniform='b')
        self.info_frame.rowconfigure(0, weight=1, uniform='b')

    def create_start_date_widget(self, col, row):
        
        self.start_date = ctk.CTkEntry(self.info_frame, placeholder_text='Start')
        self.start_date.grid(column=col, row=row, sticky='nsew', padx=10)
        
    def create_end_date_widget(self, col, row):
        self.end_date = ctk.CTkEntry(self.info_frame, placeholder_text="Koniec")
        self.end_date.grid(column = col, row=row, sticky='nsew', padx=10)
        
    def create_start_time_widget(self, col, row):
        self.start_time = ctk.CTkEntry(self.info_frame,textvariable=self.start_time_var)
        self.start_time.grid(column=col, row=row, sticky='nsew', padx=10)
        
        self.start_time_var.trace_add('write', lambda *args: self.on_time_change('start_time', *args))
        self.start_time.bind('<FocusIn>', self.set_cursor_at_start)
    
    def create_end_time_widget(self, col, row):
        self.end_time = ctk.CTkEntry(self.info_frame, textvariable=self.end_time_var)
        self.end_time.grid(column=col, row=row, sticky='nsew', padx=10)
        
        self.end_time_var.trace_add('write', lambda *args: self.on_time_change('end_time', *args))
        self.end_time.bind('<FocusIn>', self.set_cursor_at_start)
    
    def create_date_switch(self):
        
        label = ctk.CTkLabel(self, text="Dodaj zakres")
        label.grid(column=0, row=2, sticky='nse', padx=10)
        self.date_switch = ctk.CTkSwitch(self, text=None, command=self.switches_event,
                                         variable=self.switch_date_var, onvalue='on', offvalue='off')
        
        self.date_switch.grid(column=1, row=2, sticky='nsew', padx=10)
    
    def create_time_switch(self):
        label = ctk.CTkLabel(self, text="Dodaj czas")
        label.grid(column=0, row=3, sticky='nse', padx=10)
        
        self.time_switch = ctk.CTkSwitch(self, text=None, command=self.switches_event,
                                         variable=self.switch_time_var, onvalue='on', offvalue='off')
        
        self.time_switch.grid(column=1, row=3, sticky='nsew', padx=10)
    
    def create_action_buttons(self):
        action_buttons_frame = ctk.CTkFrame(self, fg_color='transparent')
        action_buttons_frame.grid(column=0, row=4, columnspan=2, sticky='nsew', padx=10)
        
        ok_button = ctk.CTkButton(action_buttons_frame, text='Ok', command=self.ok_button_click)
        ok_button.pack(side='left', padx=2)
    
        cancel_button = ctk.CTkButton(action_buttons_frame, text='Anuluj')
        cancel_button.pack(side='left', padx=2)
    #Class logic
    def on_time_change(self, time_var_name, *args):
        time_var = getattr(self, time_var_name + "_var")
        time_widget = getattr(self, time_var_name)
        
        value = time_var.get()
        cursor_position = time_widget.index(ctk.INSERT)
        clean_value = value.replace("_", "").replace(":", "")

        # jeżeli wprowadzono zbyt wiele znaków
        if len(clean_value) > 4:
            clean_value = clean_value[:4]

        # Obsługa wprowadzenia godzin
        if len(clean_value) == 2 and cursor_position == 2:
            time_var.set(clean_value[:2] + ':' + clean_value[2:])
            time_widget.icursor(cursor_position + 1)
            return

        # Walidacja zakresu godzin i minut
        if len(clean_value) == 4:
            hours, minutes = int(clean_value[:2]), int(clean_value[2:])
            if hours > 23:
                clean_value = "23" + clean_value[2:]
            if minutes > 59:
                clean_value = clean_value[:2] + "59"

        # Dodawanie zer do wartości, jeżeli jest to konieczne
        if len(clean_value) == 1:
            if int(clean_value) > 2:
                clean_value = "0" + clean_value

        if len(clean_value) == 3:
            if int(clean_value[2:]) > 5:
                clean_value = clean_value[:2] + "0" + clean_value[2]

        # Ustalanie wartości z maską
        masked_value = clean_value.ljust(4, '_')
        if len(masked_value) > 2:
            masked_value = masked_value[:2] + ':' + masked_value[2:]
        time_var.set(masked_value)

    def format_date(self, date_obj):
        days_of_week = ["Pn", "Wt", "Śr", "Cz", "Pt", "So", "Nd"]
    
        day_name = days_of_week[date_obj.weekday()]
        formatted_date = "{}, {}.{}.{}".format(day_name, date_obj.day, date_obj.month, date_obj.year)
        return formatted_date
    
    def switches_event(self): 
        state_date = self.switch_date_var.get()
        state_time = self.switch_time_var.get()

        self.destroy_if_exist("start_date")
        self.destroy_if_exist("end_date")
        self.destroy_if_exist("start_time")
        self.destroy_if_exist("end_time")
        self.destroy_if_exist("info_frame")

        if state_date=="off" and state_time=="off":
            self.create_info_frame()
            self.info_frame.columnconfigure(0, weight=1, uniform='b')
            self.info_frame.rowconfigure(0, weight=1, uniform='b')
            self.create_start_date_widget(col=0, row=0)
            self.calendar.bind("<<CalendarSelected>>", self.on_date_select)
            
        elif state_date =="on" and state_time=="off":
            self.create_info_frame()
            self.info_frame.columnconfigure((0,1), weight=1, uniform='b')
            self.info_frame.rowconfigure(0, weight=1, uniform='b')
            self.create_start_date_widget(col=0, row=0)
            self.create_end_date_widget(col=1, row=0)
            self.calendar.bind("<<CalendarSelected>>", self.on_date_range_select)

        elif state_date=="off" and state_time=="on":
            self.create_info_frame()
            self.info_frame.columnconfigure((0,1), weight=1, uniform='b')
            self.info_frame.rowconfigure(0, weight=1, uniform='b')
            self.create_start_date_widget(col=0, row=0)
            self.create_start_time_widget(col=1, row=0)
        
        elif state_date=="on" and state_time=="on":
            self.create_info_frame()
            self.info_frame.columnconfigure((0,1), weight=1, uniform='b')
            self.info_frame.rowconfigure((0,1), weight=1, uniform='b')
            self.create_start_date_widget(col=0,row=0)
            self.create_start_time_widget(col=1, row=0)
            self.create_end_date_widget(col=0, row=1)
            self.create_end_time_widget(col=1, row=1)
            self.calendar.bind("<<CalendarSelected>>", self.on_date_range_select)
         
    def destroy_if_exist(self, attr_name):
        if hasattr(self, attr_name):
            widget = getattr(self, attr_name)
            if widget.winfo_exists():
                widget.destroy()

    def set_cursor_at_start(self, event):
        event.widget.icursor(0)

    def ok_button_click(self):
        state_date = self.switch_date_var.get()
        state_time = self.switch_time_var.get()
        
        if state_date=="off" and state_time=="off":
            if not self.start_date.get().strip():
                return
            self.callback_data['start_date'] = self.start_date.get()
            
        elif state_date =="on" and state_time=="off":
            if not self.start_date.get().strip() or not self.end_date.get().strip(): 
                return
            self.callback_data['start_date'] = self.start_date.get()
            self.callback_data['end_date'] = self.end_date.get()
            
        elif state_date=="off" and state_time=="on":
            if not self.start_date.get().strip() or self.start_time.get() == "__:__": 
                return
            self.callback_data['start_date'] = self.start_date.get()
            self.callback_data['start_time'] = self.start_time.get()
            
        elif state_date=="on" and state_time=="on":
            if not self.start_date.get().strip() or not self.end_date.get().strip() or self.start_time.get() == "__:__" or self.end_time.get() == "__:__": 
                return
            self.callback_data['start_date'] = self.start_date.get()
            self.callback_data['end_date'] = self.end_date.get()
            self.callback_data['start_time'] = self.start_time.get()
            self.callback_data['end_time'] = self.end_time.get()

        self.return_data()
        self.destroy()
            
    def return_data(self):
        self.callback(self.callback_data)
 
