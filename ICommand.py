from abc import ABC, abstractclassmethod

#interfejs komendy
class Command(ABC):
    
    @abstractclassmethod
    def execute(self):
        pass
    
    

#polecnie utworzenia nowego zadania
class CreateNewTask(Command):
    def execute(self):
        pass  
    