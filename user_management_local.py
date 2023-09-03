import json
import hashlib
import os




class Users:
    def __init__(self, parent):
        
       self.view_instance = parent
        
    def save_user(self, users):
        
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)
    
    def find_remembered_user(self):
        data = self.load_users()
        
        for username, user_info in data.items():
            if 'remembered' in user_info and user_info['remembered'] == "True":
                self.view_instance.username_entry.insert(0, username)
                return "on"
        
        return "off"
           
    def on_remembered_user(self, username):
        
        data = self.load_users()
              
        if username in data:
            data[username]['remembered'] = "True"
        else:
            self.view_instance.info_message.configure(text="Użytkownik nie istnieje. Zarejestruj się")
            return
        self.save_user(data)
    
    def off_remembered_user(self):
        
        data = self.load_users()
        
        for username, user_info in data.items():
            if 'remembered' in user_info:
                del user_info['remembered']
        
        self.save_user(data)  
        
    def load_users(self):
        try:
            with open("users.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
         
    def login(self, username, password):
        users = self.load_users()
        
        if username == "":
            self.view_instance.info_message.configure(text="Wpisz nazwę użytkownika")
            return False
        
        if  username not in users:
            self.view_instance.info_message.configure(text="Użytkownik nie istnieje. Zarejestruj się")
            return False
    
        if username in users and self.verify_password(users[username]['password'], password):
            pass
        else:
            self.view_instance.info_message.configure(text="Błędne hasło")
            return False

        user_folder = self.create_user_folder(username)

        return True, user_folder
    
    def registration(self, username, email, password, password_repeat):
        
        users = self.load_users()
        
        if username == "":
            self.view_instance.info_message.configure(text="Wpisz nazwę użytkownika")
            return False
        
        if username in users:
            self.view_instance.info_message.configure(text="Nazwa użytkownika jest już zajęta")
            return False
        
        if email == "":
            self.view_instance.info_message.configure(text="Wpisz adres e-mail")
            return False
        
        if password == "":
            self.view_instance.info_message.configure(text="Wpisz hasło")
            return False
        
        if password != password_repeat:
            self.view_instance.info_message.configure(text="Hasła nie są identyczne")
            return False
        
        hashed_password = self.hash_password(password)
        
        users[username] = {"email": email, "password": hashed_password}
        self.save_user(users)
        user_folder = self.create_user_folder(username)

        return True, user_folder
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, stored_password, provided_password):
        return stored_password == self.hash_password(provided_password)
    
    def create_user_folder(self, username):
    
        current_path = os.path.dirname(os.path.realpath(__file__))
        folder_path = os.path.join(current_path, "users_data", username)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        return folder_path  