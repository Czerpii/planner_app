import json
import csv
import os
import pyAesCrypt
from UserSingleton import UserSingleton

class TaskManager:
    """
    A class representing a task manager that handles tasks, priorities, statuses, and tags.
    """

    def __init__(self):
        """
        Initializes a TaskManager instance.
        """
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

        # Create task file
        if not os.path.exists(self.tasks_file_encrypted):
            with open(self.temp_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
            self.encrypt_file(self.temp_file)
            os.remove(self.temp_file)

        # Create priority file
        if not os.path.exists(self.priority_file):
            with open(self.priority_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["priority"])

            with open(self.priority_file, 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([["Niski"], ["Średni"], ["Wysoki"]])

        # Create status file
        if not os.path.exists(self.status_file):
            with open(self.status_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["status"])

            with open(self.status_file, 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([["Nie rozpoczęto"], ["W trakcie"], ["Zakończony"], ["Zarchiwizowane"]])

        # Create tag file
        if not os.path.exists(self.tag_file):
            with open(self.tag_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["tag"])

            with open(self.tag_file, 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([["Praca"], ["Nauka"], ["Rozwój"]])

    def import_tasks(self):
        """
        Import tasks from the encrypted CSV file.

        Returns:
            A list of dictionaries representing the imported tasks.
        """
        self.decrypt_file(self.tasks_file_encrypted)
        data = []
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        os.remove(self.temp_file)
        return data

    def import_all_status(self):
        """
        Import all status values from the status CSV file.

        Returns:
            A list of status values.
        """
        status = []
        with open(self.status_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                status.append(row)
        return status

    def save(self, task_information):
        """
        Save task information to the encrypted CSV file.

        Args:
            task_information: A dictionary representing the task information.
        """
        self.decrypt_file(self.tasks_file_encrypted)
        with open(self.temp_file, 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writerow(task_information)
        self.encrypt_file(self.temp_file)
        os.remove(self.temp_file)

    def delete(self, task_id):
        """
        Delete a task with the specified ID from the encrypted CSV file.

        Args:
            task_id: The ID of the task to be deleted.
        """
        self.decrypt_file(self.tasks_file_encrypted)

        # Read all rows from the CSV file
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Remove the task with the given ID
        rows = [row for row in rows if row['id'] != task_id]

        # Write the rows back to the CSV file
        with open(self.temp_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(rows)

        if os.path.exists(self.tasks_file_encrypted):
            os.remove(self.tasks_file_encrypted)
        self.encrypt_file(self.temp_file)
        os.remove(self.temp_file)

    def edit(self, chosen_task):
        """
        Edit a task with new information in the encrypted CSV file.

        Args:
            chosen_task: A dictionary representing the updated task information.
        """
        self.decrypt_file(self.tasks_file_encrypted)
        updated_row = chosen_task
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
        """
        Encrypt a file using AES encryption.

        Args:
            file_path: The path to the file to be encrypted.
        """
        pyAesCrypt.encryptFile(file_path, self.tasks_file_encrypted, self.password, self.bufferSize)

    def decrypt_file(self, file_path):
        """
        Decrypt an encrypted file.

        Args:
            file_path: The path to the encrypted file.
        """
        pyAesCrypt.decryptFile(file_path, self.temp_file, self.password, self.bufferSize)
