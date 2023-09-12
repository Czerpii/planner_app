import os

class UserSingleton:
    
    _instance = None
    password = None
    folder_path = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserSingleton, cls).__new__(cls)
        return cls._instance
    
    
    @classmethod
    def set_folder_path(cls, username):
        
        current_path = os.path.dirname(os.path.realpath(__file__))
        cls.folder_path = os.path.join(current_path, "users_data", username)
        
        if not os.path.exists(cls.folder_path):
            os.makedirs(cls.folder_path)
        
    
    @classmethod
    def set_password(cls, password):
        cls.password = password