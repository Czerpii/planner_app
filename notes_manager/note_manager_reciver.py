import json
import csv
import os
import pyAesCrypt
from UserSingleton import *


class NoteManager():
    def __init__(self):
        """
        Initialize the NoteManager.

        This class manages notes stored in a CSV file that is encrypted with AES encryption.

        Attributes:
            pathname (str): The folder path where the notes file is stored.
            bufferSize (int): The buffer size used for encryption and decryption.
            password (str): The encryption password.
            note_file_encrypted (str): The path to the encrypted notes file.
            temp_file (str): The path to the temporary unencrypted file used for operations.
            headers (list): The headers for the CSV file.
        """
        singleton = UserSingleton()
        self.pathname = singleton.folder_path
        self.bufferSize = 64 * 1024
        self.password = singleton.password
        
        self.note_file_encrypted = os.path.join(self.pathname, "notes.csv.aes")
        self.temp_file = os.path.join(self.pathname, "notes.csv")
        
        self.headers = ['id', 'title', 'description', "background_color"]
        
        # If the encrypted notes file doesn't exist, create it with headers.
        if not os.path.exists(self.note_file_encrypted):
            with open(self.temp_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
            self.encrypt_file(self.temp_file)
            os.remove(self.temp_file)

    def import_notes(self):
        """
        Import notes from the encrypted CSV file.

        Returns:
            list: A list of dictionaries containing note data.
        """
        self.decrypt_file(self.note_file_encrypted)
        data = []
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        os.remove(self.temp_file)
        data = reversed(data)
        return data

    def save(self, note_content):
        """
        Save a new note to the encrypted CSV file.

        Args:
            note_content (dict): A dictionary containing note data.
        """
        self.decrypt_file(self.note_file_encrypted)
        with open(self.temp_file, 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writerow(note_content)
        self.encrypt_file(self.temp_file)
        os.remove(self.temp_file)

    def delete(self, id_note):
        """
        Delete a note with a given ID from the encrypted CSV file.

        Args:
            id_note (int): The ID of the note to be deleted.
        """
        self.decrypt_file(self.note_file_encrypted)
        # Read all rows from the CSV file.
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Remove the task with the specified ID.
        rows = [row for row in rows if row['id'] != str(id_note)]
        # Write rows back to the CSV file.
        with open(self.temp_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(rows)

        if os.path.exists(self.note_file_encrypted):
            os.remove(self.note_file_encrypted)
        self.encrypt_file(self.temp_file)
        os.remove(self.temp_file)

    def edit(self, chosen_task):
        """
        Edit an existing note in the encrypted CSV file.

        Args:
            chosen_task (dict): A dictionary containing the updated note data.
        """
        self.decrypt_file(self.note_file_encrypted)
        updated_id = chosen_task['id']

        with open(self.temp_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for index, data in enumerate(rows):
            if data['id'] == updated_id:
                rows[index] = chosen_task
                break

        with open(self.temp_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(rows)

        self.encrypt_file(self.temp_file)
        os.remove(self.temp_file)

    def encrypt_file(self, file_path):
        """
        Encrypt a file using AES encryption.

        Args:
            file_path (str): The path to the file to be encrypted.
        """
        pyAesCrypt.encryptFile(file_path, self.note_file_encrypted, self.password, self.bufferSize)

    def decrypt_file(self, file_path):
        """
        Decrypt a file using AES decryption.

        Args:
            file_path (str): The path to the file to be decrypted.
        """
        pyAesCrypt.decryptFile(file_path, self.temp_file, self.password, self.bufferSize)
