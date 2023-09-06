import json, csv, os
from PathSingleton import *




class NoteManager():
    def __init__(self):
        
        singleton = PathSingleton()
        self.pathname = singleton.folder_path
        
        self.note_file = os.path.join(self.pathname, "notes.csv")
        
        self.headers = ['id', 'title', 'description', "background_color"]
        
        
        if not os.path.exists(self.note_file):
            with open(self.note_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
                
                
    def save_note(self, note_content):
        with open(self.note_file, 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writerow(note_content)