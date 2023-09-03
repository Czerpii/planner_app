import json, csv, os
from PathSingleton import *

class TaskManager():
    def __init__(self):
        
        singleton = PathSingleton()
        self.pathname = singleton.folder_path
        
        self.tasks_file = os.path.join(self.pathname, "tasks.csv")
        self.priority_file = os.path.join(self.pathname, "priority.csv")
        self.status_file = os.path.join(self.pathname, 'status.csv')
        self.tag_file = os.path.join(self.pathname, "tag.csv")
        
        self.headers = ["id", "title", "description", "deadline", "status", "priority", "tag"]
        
        #create task file
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
                
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
    
    
    def save_task(self, task_information):
        with open(self.tasks_file, 'a', encoding='utf-8') as file:
            writer=csv.DictWriter(file, fieldnames=self.headers)
            writer.writerow(task_information)
            
            
        
    def delete_task(self, task):
        with open(self.tasks_file, 'w', newline='', encoding='utf-8') as file:
            writer=csv.writer(file)
            writer.writerow(self.headers)
            writer.writerows(task)
            

    
    def edit_task(self, choosen_task):
        updated_row = choosen_task
        
        # Czytaj wszystkie wiersze z pliku CSV
        with open(self.tasks_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
        #zmiana taska  
        for index, data in enumerate(rows):
            if data['id'] == updated_row['id']:
                rows[index] = updated_row
                break   
        # Zapisz wiersze z powrotem do pliku CSV
        with open(self.tasks_file, 'w', newline='', encoding='utf-8') as  file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()  # zapisuje nagłówki kolumn
            writer.writerows(rows)  # zapisuje wiersze