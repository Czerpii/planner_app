import json, csv, os
import pyAesCrypt
from UserSingleton import *

class TaskManager():
    def __init__(self):
        
        singleton = UserSingleton()
        self.pathname = singleton.folder_path
        self.bufferSize = 64 * 1024
        self.password = singleton.password
        
        self.tasks_file_encrypted = os.path.join(self.pathname, "tasks.csv.aes")
        self.temp_file = os.path.join(self.pathname, "tasks.csv")
        self.priority_file = os.path.join(self.pathname, "priority.csv")
        self.status_file = os.path.join(self.pathname, 'status.csv')
        self.tag_file = os.path.join(self.pathname, "tag.csv")
        
        self.headers = ["id", "title", "description", "start", "end", "status", "priority", "tag"]
        
        #create task file
        if not os.path.exists(self.tasks_file_encrypted):
            with open(self.temp_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
            self.encrypt_file(self.temp_file)
            os.remove(self.temp_file)    
            
        #create priority file
        if not os.path.exists(self.priority_file):
            with open(self.priority_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["priority"])
                
            with open(self.priority_file, 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([["Niski"], ["Średni"], ["Wysoki"]])
                
        #create status file      
        if not os.path.exists(self.status_file):
            with open(self.status_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["status"])
                
            with open(self.status_file, 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([["Nie rozpoczęto"], ["W trakcie"], ["Zakończony"], ["Zarchiwizowane"]])
        
        #create tag file       
        if not os.path.exists(self.tag_file):
            with open(self.tag_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["status"])
                
            with open(self.tag_file, 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([["Praca"], ["Nauka"], ["Rozwój"]])
    
    
    def import_tasks(self):
        
        self.decrypt_file(self.tasks_file_encrypted)
        data = []
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        os.remove(self.temp_file)
        return data   
    
    def import_all_status(self):
        status = []
        with open(self.status_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                status.append(row) 
        return status
    
    def save_task(self, task_information):
        self.decrypt_file(self.tasks_file_encrypted)
        with open(self.temp_file, 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writerow(task_information)
        self.encrypt_file(self.temp_file)
        os.remove(self.temp_file)  
            
        
    def delete_task(self, task_id):
        self.decrypt_file(self.tasks_file_encrypted)

        # Czytaj wszystkie wiersze z pliku CSV
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Usuń zadanie o podanym ID
        rows = [row for row in rows if row['id'] != task_id]

        # Zapisz wiersze z powrotem do pliku CSV
        with open(self.temp_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(rows)

        if os.path.exists(self.tasks_file_encrypted):
            os.remove(self.tasks_file_encrypted)
        self.encrypt_file(self.temp_file)
        os.remove(self.temp_file) 
            

    
    def edit_task(self, choosen_task):
        self.decrypt_file(self.tasks_file_encrypted)
        updated_row = choosen_task
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
        for index, data in enumerate(rows):
            if data['id'] == updated_row['id']:
                rows[index] = updated_row
                break

        with open(self.temp_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(rows)
        self.encrypt_file(self.temp_file)
        os.remove(self.temp_file) 
        
    def encrypt_file(self, file_path):
        pyAesCrypt.encryptFile(file_path, self.tasks_file_encrypted, self.password, self.bufferSize)

    def decrypt_file(self, file_path):
        pyAesCrypt.decryptFile(file_path, self.temp_file, self.password, self.bufferSize)