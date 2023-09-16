from abc import ABC, abstractclassmethod

# Command interface
class Command(ABC):
    """
    Abstract base class representing a command.
    """
    
    @abstractclassmethod
    def execute(self):
        """
        Abstract method to execute the command.
        """
        pass
    

class Save(Command):
    """
    Concrete command to save data.
    """
    
    def __init__(self, reciver, **input):
        """
        Initializes the Save command with a receiver and input data.

        Args:
            reciver (class): The receiver of the command.
            **input (any): All provided values will be saved.
        """
        self.reciver = reciver
        self.to_save = input
        
    def execute(self):
        """
        Executes the save command.
        """
        self.reciver.save(self.to_save)
    

class Delete(Command):
    """
    Concrete command to delete data.
    """
    
    def __init__(self, reciver, input):
        """
        Initializes the Delete command with a receiver and input data.

        Args:
            reciver (class): The receiver of the command.
            input (any): Data to be deleted.
        """
        self.reciver = reciver
        self.to_delete = input
    
    def execute(self):
        """
        Executes the delete command.
        """
        self.reciver.delete(self.to_delete)
        
        
class Edit(Command):
    """
    Concrete command to edit data.
    """
    
    def __init__(self, reciver, **input):
        """
        Initializes the Edit command with a receiver and input data.

        Args:
            reciver (class): The receiver of the command.
            **input (any): Data to be edited.
        """
        self.reciver = reciver
        self.to_edit = input
    
    def execute(self):
        """
        Executes the edit command.
        """
        self.reciver.edit(self.to_edit)
