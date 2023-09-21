import os

class UserManager:
    """
    Singleton class representing a user. This class ensures that only one instance
    of the user is created throughout the application's lifecycle.
    
    Attributes:
        _instance (UserSingleton): The single instance of the UserSingleton class.
        password (str): The password of the user.
        folder_path (str): The path to the user's data folder.
    """
    
    _instance = None
    password = None
    folder_path = None
    
    def __new__(cls):
        """
        Override the __new__ method to ensure only one instance of the class is created.
        
        Returns:
            UserSingleton: The single instance of the UserSingleton class.
        """
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def set_folder_path(cls, username):
        """
        Set the folder path for the user's data based on the provided username.
        
        Args:
            username (str): The username of the user.
        """
        # Get the current directory path
        current_path = os.path.dirname(os.path.realpath(__file__))
        
        # Construct the folder path for the user's data
        cls.folder_path = os.path.join(current_path, "users_data", username)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(cls.folder_path):
            os.makedirs(cls.folder_path)
    
    @classmethod
    def set_password(cls, password):
        """
        Set the password for the user.
        
        Args:
            password (str): The password of the user.
        """
        cls.password = password