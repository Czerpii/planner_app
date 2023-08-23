import json, csv, os


class TaskManager():
    def __init__(self):
        self.tasks_file = "./task_file/tasks.csv"
        self.headers = ["id", "title", "description", "deadline", "status", "priority", "tag"]
        
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
                file.close()
        
        
                
    
    def save_task(self, task_information):
        with open(self.tasks_file, 'a', encoding='utf-8') as file:
            writer=csv.DictWriter(file, fieldnames=self.headers)
            writer.writerow(task_information)
            file.close()
            
        
    def delete_task(self, task):
        with open(self.tasks_file, 'w', newline='', encoding='utf-8') as file:
            writer=csv.writer(file)
            writer.writerow(self.headers)
            writer.writerows(task)
            file.close()

    
    def edit_task(self, choosen_task):
        updated_row = choosen_task
        
        # Czytaj wszystkie wiersze z pliku CSV
        with open(self.tasks_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            file.close()
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