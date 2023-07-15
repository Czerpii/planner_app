from abc import ABC, abstractclassmethod

#interfejs komendy
class Command(ABC):
    
    @abstractclassmethod
    def execute(self):
        pass
    
    


class Save(Command):
    def __init__(self, reciver, **input):
        """funkcja zapisuje podane dane do **input

        Args:
            reciver (class): odbiorca funckji
            **input (any): wszystkie podane wartości zostaną zapisane
        """
        self.reciver = reciver
        self.to_save = input
        
    def execute(self):
        self.reciver.save_task(self.to_save)
    