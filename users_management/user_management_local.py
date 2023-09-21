import json
import hashlib
import os
from UserSingleton import *


class Users:
    """
    A class that manages user data, including registration, login, and remembering users.
    """

    def __init__(self, parent):
        """
        Initializes a Users instance.

        Args:
            parent: The parent widget.
        """
        self.view_instance = parent
        self.pathname = os.path.join(os.path.dirname(os.path.realpath(__file__)), "users.json")
        self.singleton = UserManager()

    def save_user(self, users):
        """
        Saves user data to a JSON file.

        Args:
            users (dict): A dictionary containing user data.
        """
        with open(self.pathname, "w") as f:
            json.dump(users, f, indent=4)

    def find_remembered_user(self):
        """
        Finds and returns the remembered user, if any.

        Returns:
            str: "on" if a remembered user is found, "off" otherwise.
        """
        data = self.load_users()

        for username, user_info in data.items():
            if 'remembered' in user_info and user_info['remembered'] == "True":
                self.view_instance.username_entry.insert(0, username)
                return "on"

        return "off"

    def on_remembered_user(self, username):
        """
        Marks a user as remembered.

        Args:
            username (str): The username of the user to be remembered.
        """
        data = self.load_users()

        if username in data:
            data[username]['remembered'] = "True"
        else:
            self.view_instance.info_message.configure(text="Użytkownik nie istnieje. Zarejestruj się")
            return
        self.save_user(data)

    def off_remembered_user(self):
        """Clears the remembered user flag for all users."""
        data = self.load_users()

        for username, user_info in data.items():
            if 'remembered' in user_info:
                del user_info['remembered']

        self.save_user(data)

    def load_users(self):
        """
        Loads user data from the JSON file.

        Returns:
            dict: A dictionary containing user data.
        """
        try:
            with open(self.pathname, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def login(self, username, password):
        """
        Logs in a user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        users = self.load_users()

        if username == "":
            self.view_instance.info_message.configure(text="Wpisz nazwę użytkownika")
            return False

        if username not in users:
            self.view_instance.info_message.configure(text="Użytkownik nie istnieje. Zarejestruj się")
            return False

        if username in users and self.verify_password(users[username]['password'], password):
            pass
        else:
            self.view_instance.info_message.configure(text="Błędne hasło")
            return False

        hashed_password = self.hash_password(password)
        self.singleton.set_folder_path(username)
        self.singleton.set_password(hashed_password)

        return True

    def registration(self, username, email, password, password_repeat):
        """
        Registers a new user.

        Args:
            username (str): The username of the new user.
            email (str): The email of the new user.
            password (str): The password of the new user.
            password_repeat (str): The repeated password for confirmation.

        Returns:
            bool: True if registration is successful, False otherwise.
        """
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

        self.singleton.set_folder_path(username)
        self.singleton.set_password(hashed_password)

        return True

    def hash_password(self, password):
        """
        Hashes a password using SHA-256.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, stored_password, provided_password):
        """
        Verifies a password against a stored hashed password.

        Args:
            stored_password (str): The stored hashed password.
            provided_password (str): The password to be verified.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return stored_password == self.hash_password(provided_password)
