class Invoker:
    """
    The Invoker class is responsible for initiating the execution of a command.
    It does not know anything about the concrete command, it only knows about the command interface.
    """
    
    def __init__(self):
        """
        Initializes a new instance of the Invoker class.
        """
        self.command = None  # Holds the command that will be executed
        
    def set_command(self, command):
        """
        Sets the command that will be executed.
        
        Args:
            command (Command): The command object to be executed.
        """
        self.command = command
        
    def press_button(self):
        """
        Executes the command. This simulates pressing a button that triggers the command.
        """
        if self.command:
            self.command.execute()
        else:
            print("No command set!")
