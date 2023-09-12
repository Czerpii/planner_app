import json, csv, os
import pyAesCrypt
from UserSingleton import *




class NoteManager():
    def __init__(self):
        
        singleton = UserSingleton()
        self.pathname = singleton.folder_path
        self.bufferSize = 64 * 1024
        self.password = singleton.password
        
        self.note_file_encrypted = os.path.join(self.pathname, "notes.csv.aes")
        self.temp_file = os.path.join(self.pathname, "notes.csv")
        
        self.headers = ['id', 'title', 'description', "background_color"]
        
        
        if not os.path.exists(self.note_file_encrypted):
            with open(self.temp_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
            self.encrypt_file(self.temp_file)
            os.remove(self.temp_file)
    
    def import_notes(self):
        
        self.decrypt_file(self.note_file_encrypted)
        data = []
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        os.remove(self.temp_file)
        return data
           
    def save_note(self, note_content):
        
        self.decrypt_file(self.note_file_encrypted)
        with open(self.temp_file, 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writerow(note_content)
        self.encrypt_file(self.temp_file)
        os.remove(self.temp_file)
        
    
    def encrypt_file(self, file_path):
        pyAesCrypt.encryptFile(file_path, self.note_file_encrypted, self.password, self.bufferSize)

    def decrypt_file(self, file_path):
        pyAesCrypt.decryptFile(file_path, self.temp_file, self.password, self.bufferSize)