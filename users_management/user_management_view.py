import customtkinter as ctk
from users_management.user_management_local import Users




class LoginView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color='#0c3377', corner_radius=10, width=200, height=300)
        self.pack(pady = 150)
        
        self.parent=parent
        self.users_management = Users(self)
        
        self.configure_layout()
        
        self.main_label = ctk.CTkLabel(self,
                                       text = "Logowanie",
                                       font=ctk.CTkFont(family="Abril Fatface", size=30, weight="bold"))
        self.main_label.grid(column=0, columnspan=2, row=0, sticky='nsew', pady=10)
        
        self.create_userdata_frame()
        
        self.remember_me_state = ctk.StringVar(value=self.users_management.find_remembered_user())
        
        self.create_login_buttons_frame()
        self.create_additional_buttons()
        self.info_label()
        
           
    def configure_layout(self):
        self.columnconfigure((0,1), weight=1, uniform='b')
        self.rowconfigure(0, weight=2, uniform='b')
        self.rowconfigure(1, weight=4, uniform='b')
        self.rowconfigure((2,3,4,5,6,7), weight=1, uniform='b')
        
    def create_userdata_frame(self):
        
        self.userdata_frame = ctk.CTkFrame(self,fg_color='transparent')
        self.userdata_frame.grid(column = 0, columnspan=2, row=1, sticky='nsew', padx=15,)
        
        self.userdata_frame.columnconfigure(0, weight=1, uniform='b')
        self.userdata_frame.rowconfigure((0,2), weight=1, uniform='b')
        # self.userdata_frame.rowconfigure((1), weight=1, uniform='b')
        
        
        self.username_entry = ctk.CTkEntry(self.userdata_frame, placeholder_text='Nazwa użytkownika')
        self.username_entry.grid(column=0, row=0, columnspan=2, sticky='nsew',  pady=10)
        
        self.userpassword_entry = ctk.CTkEntry(self.userdata_frame, placeholder_text='Hasło', show="*")
        self.userpassword_entry.grid(column=0, row=2, columnspan=2, sticky='nsew', pady=10)
        
        self.userpassword_entry.bind("<Return>", self.enter_click)

    def create_login_buttons_frame(self):
        
        self.buttons_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.buttons_frame.grid(column=0, columnspan=2, row=3, sticky='nsew', padx=15,)
        
        self.buttons_frame.columnconfigure((0,1), weight=1, uniform='b')
        self.buttons_frame.rowconfigure(0, weight=1, uniform='b')
        
        self.login_button = ctk.CTkButton(self.buttons_frame, text="Zaloguj się", command=self.login_button_click)
        self.login_button.grid(column=1, row=0, sticky='nsew')
        
        self.remember_me_button = ctk.CTkCheckBox(self.buttons_frame,
                                                  text='Zapamiętaj mnie',
                                                  command=self.remember_me_func,
                                                  variable=self.remember_me_state,
                                                  onvalue='on',
                                                  offvalue='off')
        self.remember_me_button.grid(column=0, row=0, sticky='nsew')
        
    def create_additional_buttons(self):
        
        self.forget_password_button = ctk.CTkButton(self, text="Nie pamiętasz hasła?", fg_color="#0c3377", hover_color="#0a295f")
        self.forget_password_button.grid(column=0, row=5, columnspan=2, sticky='nsew', padx=15, pady=2)
        
        self.registration_button = ctk.CTkButton(self, text="Zarejestruj się", fg_color="#0c3377", hover_color="#0a295f", command=self.open_registration_form)
        self.registration_button.grid(column=0, row=6, columnspan=2, sticky='nsew', padx=15, pady=2)

    def info_label(self):
        self.info_message = ctk.CTkLabel(self, text="", font=ctk.CTkFont(family="Abril Fatface", size=15), text_color='red')
        self.info_message.grid(column=0, columnspan=2, row=2, sticky='nsew' )
        
    def login_button_click(self):
        
        login_status = self.users_management.login(self.username_entry.get(),
                                                    self.userpassword_entry.get())
        if login_status:
            self.parent.main_view(self)
       
    def remember_me_func(self):
        if self.remember_me_state.get() == "on":
            self.users_management.on_remembered_user(self.username_entry.get())
        elif self.remember_me_state.get() == "off":
            self.users_management.off_remembered_user()
             
    def open_registration_form(self):
        self.destroy()
        RegistrationView(self.parent)

    def enter_click(self, event):
        self.login_button_click()
        
class RegistrationView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color='#0c3377', corner_radius=10)
        self.pack(pady = 150)
        
        self.users_management = Users(self)
        self.parent = parent
        
        self.configure_layout()
        
        self.main_label = ctk.CTkLabel(self,
                                       text = "Rejestracja",
                                       font=ctk.CTkFont(family="Abril Fatface", size=30, weight="bold"))
        self.main_label.grid(column=0, columnspan=2, row=0, sticky='nsew', pady=10, padx=100)
        
        self.create_userdata_frame()
        self.create_registration_buttons_frame()
        self.info_label()

    def configure_layout(self):
        self.columnconfigure((0,1), weight=1, uniform='b')
        self.rowconfigure(0, weight=2, uniform='b')
        self.rowconfigure(1, weight=5, uniform='b')
        self.rowconfigure((2,3,4), weight=1, uniform='b')
        
    def create_userdata_frame(self):
        
        self.userdata_frame = ctk.CTkFrame(self,fg_color='transparent')
        self.userdata_frame.grid(column = 0, columnspan=2, row=1, sticky='nsew', padx=15,)
        
        self.userdata_frame.columnconfigure(0, weight=1, uniform='b')
        self.userdata_frame.rowconfigure((0,1,2,3), weight=2, uniform='b')
        # self.userdata_frame.rowconfigure((1), weight=1, uniform='b')
        
        self.username_entry = ctk.CTkEntry(self.userdata_frame, placeholder_text='Nazwa użytkownika')
        self.username_entry.grid(column=0, row=0, sticky='nsew',  pady=10)
        
        self.email_entry = ctk.CTkEntry(self.userdata_frame, placeholder_text='Adres e-mail')
        self.email_entry.grid(column=0, row=1, sticky='nsew', pady=10)
        
        self.userpassword_entry = ctk.CTkEntry(self.userdata_frame, placeholder_text='Hasło', show="*")
        self.userpassword_entry.grid(column=0, row=2, sticky='nsew', pady=10)
        
        self.userpassword_repeat_entry = ctk.CTkEntry(self.userdata_frame, placeholder_text='Powtórz hasło', show="*")
        self.userpassword_repeat_entry.grid(column=0, row=3, sticky='nsew', pady=10)
             
    def create_registration_buttons_frame(self):
        
        self.buttons_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.buttons_frame.grid(column=0, columnspan=2, row=3, sticky='nsew', padx=15,)
        
        self.buttons_frame.columnconfigure((0,1), weight=1, uniform='b')
        self.buttons_frame.rowconfigure(0, weight=1, uniform='b')
        
        self.login_button = ctk.CTkButton(self.buttons_frame, text="Zarejestruj się", command=self.registration_button)
        self.login_button.grid(column=0, row=0, columnspan=2, sticky='nsew')
    
    def info_label(self):
        self.info_message = ctk.CTkLabel(self, text="", font=ctk.CTkFont(family="Abril Fatface", size=15), text_color='red')
        self.info_message.grid(column=0, columnspan=2, row=2, sticky='nsew' )
    
    def registration_button(self):
        
        users = self.users_management.load_users()
        
        registration_status = self.users_management.registration( self.username_entry.get(),
                                           self.email_entry.get(),
                                           self.userpassword_entry.get(),
                                           self.userpassword_repeat_entry.get())
        if registration_status:
            self.parent.main_view(self)
