
import customtkinter as ctk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .controller import CurrencyController
import themes_manager

class CurrencyCalculatorUI(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color="transparent")
        self.grid(column = col, row=row, sticky = "nsew", pady=5)

        self.controler = CurrencyController()
        self.initialize_variables()
        self.configure_layout()
        self.conversion_view()
        self.result_view()
        
    def initialize_variables(self):
        self.convert_from_var = ctk.StringVar()
        self.convert_to_var = ctk.StringVar()
        
    def configure_layout(self):
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure((0,1), weight=1, uniform='a')
   
    def conversion_view(self):
        frame = ctk.CTkFrame(self, fg_color=themes_manager.get_color('fg_frame'), border_color=themes_manager.get_color("border_entry"), border_width=2, corner_radius=10)
        frame.grid(column=0, row=0, sticky='nsew', padx=10, pady=10 )
        
        #setup layout
        frame.columnconfigure((0,9), weight=1, uniform='a')
        frame.columnconfigure((1,2,3,4,6,7,8), weight=4, uniform='a')
        frame.columnconfigure(5, weight=2, uniform='a')
        frame.rowconfigure((0,3), weight=1, uniform='a')
        frame.rowconfigure((1,2), weight=2, uniform='a')
        frame.grid_propagate(False)
        
        #create labels
        self.create_conversion_labels(frame, col=[1,3,6], row=1)
        
        #create input widget
        self.create_parameters_entry(frame, col=[1,3,6], row=2)
        
        #create action button 
        self.create_action_buttons(frame, col=[5,8], row=2)
     
    def result_view(self):
        frame = ctk.CTkFrame(self, fg_color=themes_manager.get_color('fg_frame'), border_color=themes_manager.get_color("border_entry"), border_width=2, corner_radius=10)
        frame.grid(column=0, row=1, sticky='nsew', padx=10, pady=10)

        #setup layout
        frame.columnconfigure((0,2), weight=1, uniform='a')
        frame.columnconfigure(1, weight=10, uniform='a')
        frame.rowconfigure((0,3), weight=1, uniform='a')
        frame.rowconfigure((1,2), weight=5, uniform='a')
        
        #create conversion result labels
        self.create_result_labels(frame, col=1, row=[1,2])
    
    def create_conversion_labels(self, parent, col, row):
        
        font = themes_manager.get_ctk_font("default_bold")
        ctk.CTkLabel(parent, text="Kwota:", font=font).grid(column=col[0], row=row, sticky='sw')
        ctk.CTkLabel(parent, text="Przelicz z:", font=font).grid(column=col[1], row=row, sticky='sw')
        ctk.CTkLabel(parent, text="Przelicz na:",font=font).grid(column=col[2], row=row, sticky='sw',)
        
    def create_parameters_entry(self, parent, col, row):
        
        currencies_name = self.controler.get_currency_code_and_name()
        
        self.entry_value = ctk.CTkEntry(parent,
                                        placeholder_text='Podaj kwotę',
                                        font = themes_manager.get_ctk_font("entry"),
                                        fg_color=themes_manager.get_color("entry"),
                                        border_color=themes_manager.get_color("border_entry"),
                                        justify ='right')
        self.entry_value.grid(column=col[0], row=row, columnspan=2, sticky='nw')
        
        self.convert_from_label = ctk.CTkComboBox(parent,
                                                  font = themes_manager.get_ctk_font("entry"),
                                                  fg_color=themes_manager.get_color("entry"),
                                                  border_color=themes_manager.get_color("border_entry"),
                                                  button_color=themes_manager.get_color("button"),
                                                  button_hover_color=themes_manager.get_color("button_hover"),
                                                  values=currencies_name,
                                                  state='readonly',
                                                  variable=self.convert_from_var)
        self.convert_from_var.set(currencies_name[0])
        self.convert_from_label.grid(column=col[1], row=row,columnspan=2, sticky='nwe')
        
        self.convert_to_label = ctk.CTkComboBox(parent,
                                                font = themes_manager.get_ctk_font("entry"),
                                                fg_color=themes_manager.get_color("entry"),
                                                border_color=themes_manager.get_color("border_entry"),
                                                button_color=themes_manager.get_color("button"),
                                                button_hover_color=themes_manager.get_color("button_hover"),
                                                values=currencies_name,
                                                state='readonly',
                                                variable=self.convert_to_var)
        self.convert_to_var.set(currencies_name[8])
        self.convert_to_label.grid(column=col[2], row=row,columnspan=2, sticky='nwe')

    def create_action_buttons(self, parent, col, row):
        change_image = ctk.CTkImage(dark_image= Image.open("./button_image/change.png"),
                                     light_image= Image.open("./button_image/change.png"))
        
        self.switch_button = ctk.CTkButton(parent,
                                          text='',
                                          image=change_image,
                                          fg_color=themes_manager.get_color("button"),
                                          hover_color=themes_manager.get_color("button_hover"),
                                          command=self.replace_button_click)
        self.switch_button.grid(column=col[0], row=row, sticky='n', padx=5)

        self.calculate_button = ctk.CTkButton(parent,
                                              text='Oblicz',
                                              font = themes_manager.get_ctk_font("button"),
                                              fg_color=themes_manager.get_color("button"),
                                              hover_color=themes_manager.get_color("button_hover"),
                                              command=self.calculate_button_click)
        self.calculate_button.grid(column=col[1], row=row, sticky='nw', padx=3)
    
    def create_result_labels(self, parent, col, row):
        
        self.result_value_label = ctk.CTkLabel(parent, text='', font=themes_manager.get_ctk_font("small_header"))
        self.result_value_label.grid(column=col, row=row[0], sticky='sew')
        
        self.unit_value_label = ctk.CTkLabel(parent, text='',font=themes_manager.get_ctk_font("default_bold"))
        self.unit_value_label.grid(column=col, row=row[1], sticky='new')
               
    def replace_button_click(self):
        temp = self.convert_from_var.get()
        self.convert_from_var.set(self.convert_to_var.get())
        self.convert_to_var.set(temp)
        
        self.calculate_button_click()
    
    def calculate_button_click(self):
        
        from_code = self.convert_from_var.get().split()[0]
        to_code = self.convert_to_var.get().split()[0]
        
        try:
            amount = float(self.entry_value.get())
        except ValueError:
            self.result_value_label.configure(text="Nieprawidłowa wartość kwoty!")
            self.unit_value_label.configure(text='')
            return 
    
        result_text = f"{amount:.2f} {from_code} = {self.controler.convert_currencies(amount, from_code, to_code)} {to_code}"
        result_unit_text  = f"1 {from_code} = {self.controler.convert_currencies(1, from_code, to_code)} {to_code}" 
        
        self.result_value_label.configure(text= result_text)
        self.unit_value_label.configure(text=result_unit_text)
    

class CurrencyHistoryUi(ctk.CTkFrame):
    def __init__(self, parent, col, row):
        super().__init__(parent, fg_color='transparent')
        self.grid(column=col, row=row, sticky='nsew', pady=5)
    
        self.controler = CurrencyController()
    
        self.configure_layout()
        self.initialize_variables()
        self.initialize_dates()
        self.chart_layout_view()
        self.table_layout_view()
        self.draw_chart()
        
    def initialize_variables(self):
        self.convert_from_var = ctk.StringVar()
        self.convert_to_var = ctk.StringVar()
        self.chart_range_var = ctk.StringVar(value="Tydzień")
    
    def initialize_dates(self):
        date = self.controler.get_dates()
        self.start_date = date["one_week_ago"]
        self.end_date = date['today']
    
    def configure_layout(self):
        
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
       
        
    
    def chart_layout_view(self):
        self.char_frame = ctk.CTkFrame(self, fg_color=themes_manager.get_color("fg_frame"), corner_radius=10)
        self.char_frame.grid(column = 0, row = 0, sticky='nsew', padx=2)
        
        #layout
        self.char_frame.columnconfigure(0, weight=1, uniform='a')
        self.char_frame.rowconfigure(0, weight=1, uniform='a')
        self.char_frame.rowconfigure(1, weight=8, uniform='a')
          
        self.config_bar_chart_layout(self.char_frame)  
        
    def table_layout_view(self):
        frame = ctk.CTkScrollableFrame(self, fg_color=themes_manager.get_color("fg_frame"), corner_radius=10)
        frame.grid(column = 1, row=0, sticky='nsew', padx=2)
        font = themes_manager.get_ctk_font("default_bold")
        frame.columnconfigure((0,1,2), weight=1, uniform='a')

        ctk.CTkLabel(frame, text="Kod",font=font).grid(column=0, row=0, sticky='nsew', padx=2, pady=2)
        ctk.CTkLabel(frame, text="Kupno", font=font).grid(column=1, row=0, sticky='nsew', padx=2, pady=2)
        ctk.CTkLabel(frame, text="Sprzedaż", font=font).grid(column=2, row=0, sticky='nsew', padx=2, pady=2)
        
        self.creates_data_labels_for_table(frame)
       
        
    def creates_data_labels_for_table(self, parent):
        code, sell, buy = self.controler.get_sell_and_but_rate()
        font = themes_manager.get_ctk_font("default")
        row = 1
        for c in code:
            ctk.CTkLabel(parent, text=c, font=font).grid(column=0, row=row, sticky='nsew', padx=2, pady=2)
            row+=1
        
        row=1   
        for s in sell:
            ctk.CTkLabel(parent, text=s, font=font).grid(column=1, row=row, sticky='nsew', padx=2, pady=2)
            row+=1
            
        row=1   
        for b in buy:
            ctk.CTkLabel(parent, text=b, font=font).grid(column=2, row=row, sticky='nsew', padx=2, pady=2)
            row+=1

    def config_bar_chart_layout(self, parent):
        
        currencies_name = self.controler.get_currency_code()
        
        frame = ctk.CTkFrame(parent, fg_color='transparent', corner_radius=10)
        frame.grid(column = 0, row=0, sticky='nsew')
    
        self.convert_from_label = ctk.CTkComboBox(frame,
                                                font = themes_manager.get_ctk_font("entry"),
                                                fg_color=themes_manager.get_color("entry"),
                                                border_color=themes_manager.get_color("border_entry"),
                                                button_color=themes_manager.get_color("button"),
                                                button_hover_color=themes_manager.get_color("button_hover"),
                                                values=currencies_name, state='readonly',
                                                variable=self.convert_from_var)
        self.convert_from_var.set(currencies_name[8])
        self.convert_from_label.pack(side='left', fill='both', padx=2, pady=10)

        self.convert_to_label = ctk.CTkComboBox(frame,
                                                font = themes_manager.get_ctk_font("entry"),
                                                fg_color=themes_manager.get_color("entry"),
                                                border_color=themes_manager.get_color("border_entry"),
                                                button_color=themes_manager.get_color("button"),
                                                button_hover_color=themes_manager.get_color("button_hover"),
                                                values=currencies_name,state='readonly',
                                                variable=self.convert_to_var)
        self.convert_to_var.set(currencies_name[0])
        self.convert_to_label.pack(side='left', fill='both', padx=2, pady=10)
        
        self.draw_button = ctk.CTkButton(frame,
                                            font = themes_manager.get_ctk_font("button"),
                                            fg_color=themes_manager.get_color("button"),
                                            hover_color=themes_manager.get_color("button_hover"),
                                            text="Rysuj",
                                            command=self.draw_chart)
        self.draw_button.pack(side='right', fill='both', padx=2, pady=10)
    
        self.chart_range = ctk.CTkComboBox(frame,
                                            font = themes_manager.get_ctk_font("entry"),
                                            fg_color=themes_manager.get_color("entry"),
                                            border_color=themes_manager.get_color("border_entry"),
                                            button_color=themes_manager.get_color("button"),
                                            button_hover_color=themes_manager.get_color("button_hover"),
                                            values=['Tydzień', "Miesiąc", "Rok"],
                                            state='readonly', 
                                            variable=self.chart_range_var, 
                                            command=self.date_range_combobox_command)
        self.chart_range.pack(side='right', fill='both', padx=2, pady=10)
          
    def date_range_combobox_command(self, choice):
        dates = self.controler.get_dates()
        
        self.end_date = dates["today"]
        
        if self.chart_range_var.get() == "Tydzień":
            self.start_date = dates["one_week_ago"]
        elif self.chart_range_var.get() == "Miesiąc":
            self.start_date=dates["one_month_ago"] 
        elif self.chart_range_var.get() == "Rok":
            self.start_date=dates["one_year_ago"]
    
    def draw_chart(self):
        data = self.controler.get_currency_rate(from_code = self.convert_from_var.get(),
                                                to_code = self.convert_to_var.get(), 
                                                start_date=self.start_date,
                                                end_date=self.end_date)
        dates = list(data.keys())
        rates = list(data.values())
        self.chart_view(self.char_frame, dates, rates)

    def chart_view(self, parent, dates, rates):
        figure = plt.Figure(figsize=(6, 4), dpi=100)
        ax = figure.add_subplot(111)
        
        line, = ax.plot(dates, rates)
        
        ax.set_title(f"Z {self.convert_from_var.get()} na {self.convert_to_var.get()}")
        ax.set_xlabel("Data")
        ax.set_ylabel("Kurs")
        ax.grid(True)
        num_dates = len(dates)
        if num_dates >= 3:
            ticks = [dates[0], dates[num_dates//2], dates[-1]]
        else:
            ticks = dates
        ax.set_xticks(ticks)

        canvas = FigureCanvasTkAgg(figure, parent)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=1, sticky='nsew')
        
        annot = ax.annotate("", xy=(0, 0), xytext=(0, 20), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def update_annot(ind):
            x, y = line.get_data()
            annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
            text = f"{x[ind['ind'][0]]}, {y[ind['ind'][0]]:.2f}"
            annot.set_text(text)

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax:
                cont, ind = line.contains(event)
                if cont:
                    update_annot(ind)
                    annot.set_visible(True)
                    canvas.draw_idle()
                else:
                    if vis:
                        annot.set_visible(False)
                        canvas.draw_idle()

        canvas.mpl_connect("motion_notify_event", hover)