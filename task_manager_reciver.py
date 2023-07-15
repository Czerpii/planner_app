import json
import csv
import os


class TaskManager():
    def __init__(self):
        self.tasks_file = "tasks.csv"
        self.headers = ["title", "description", "deadline", "status", "priority", "tag"]
        
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
                file.close()
        
        
                
    
    def save_task(self, task_information):
        with open(self.tasks_file, 'a', encoding='utf-8') as file:
            writer=csv.DictWriter(file, fieldnames=self.headers)
            writer.writerow(task_information)
            file.close()
            
        


