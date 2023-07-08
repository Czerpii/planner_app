from abc import ABC, abstractclassmethod

#interfejs komendy
class Command(ABC):
    
    @abstractclassmethod
    def execute(self):
        pass
    
    

#polecnie utworzenia nowego zadania
class CreateNewTask(Command):
    def __init__(self, task_manager,parent):
        self.task_manager = task_manager
        self.parent = parent
    def execute(self):
        self.task_manager.new_task(self.parent) 
    