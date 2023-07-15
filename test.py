import tkinter as tk

class Receiver:
    def open_window(self):
        top_level_window = tk.Toplevel()
        top_level_window.title("Okno Toplevel")
        label = tk.Label(top_level_window, text="To jest okno Toplevel")
        label.pack()

    def close_window(self, window):
        window.destroy()

class Command:
    def execute(self):
        pass

class OpenWindowCommand(Command):
    def __init__(self, receiver, window):
        self.receiver = receiver
        self.window = window

    def execute(self):
        self.receiver.open_window()

class CloseWindowCommand(Command):
    def __init__(self, receiver, window):
        self.receiver = receiver
        self.window = window

    def execute(self):
        self.receiver.close_window(self.window)

class Invoker:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def execute_command(self):
        if self.command:
            self.command.execute()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Przyciski z poleceniami")

        receiver = Receiver()
        invoker = Invoker()

        open_window_command = OpenWindowCommand(receiver, self)
        close_window_command = CloseWindowCommand(receiver, self)

        invoker.set_command(open_window_command)
        open_button = tk.Button(self, text="Otwórz okno", command=invoker.execute_command)

        invoker.set_command(close_window_command)
        close_button = tk.Button(self, text="Zamknij okno", command=invoker.execute_command)

        open_button.pack()
        close_button.pack()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
