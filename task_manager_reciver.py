import json
import csv
import os


class TaskManager():
    def __init__(self):
        self.tasks_file = "tasks.csv"
        self.headers = ["title", "description", "date", "status", "priority", "tag"]
        
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
                file.close()
                
    
    def save_task(self, task_information):
        print(task_information)
        


