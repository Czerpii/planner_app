import tkinter as tk

# Interfejs komendy
class Command:
    def execute(self):
        pass

# Komenda włączenia światła
class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

# Komenda wyłączenia światła
class LightOffCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.off()

# Komenda włączenia gniazdka
class SocketOnCommand(Command):
    def __init__(self, socket):
        self.socket = socket

    def execute(self):
        self.socket.on()

# Komenda wyłączenia gniazdka
class SocketOffCommand(Command):
    def __init__(self, socket):
        self.socket = socket

    def execute(self):
        self.socket.off()

# Komenda przyciemniania światła
class LightDimCommand(Command):
    def __init__(self, light, level):
        self.light = light
        self.level = level

    def execute(self):
        self.light.dim(self.level)

# Odbiornik dla światła
class Light:
    def on(self):
        print("Światło zostało włączone.")

    def off(self):
        print("Światło zostało wyłączone.")

    def dim(self, level):
        print("Światło jest przyciemnione na poziomie", level)

# Odbiornik dla gniazdka
class Socket:
    def on(self):
        print("Gniazdko zostało włączone.")

    def off(self):
        print("Gniazdko zostało wyłączone.")

# Obiekt, który obsługuje żądania (Invoker)
class RemoteControl:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def press_button(self):
        self.command.execute()

# Tworzenie GUI z użyciem biblioteki Tkinter
class GUI:
    def __init__(self, remote_control):
        self.remote_control = remote_control

        self.window = tk.Tk()
        self.window.title("Remote Control")

        self.light_button_on = tk.Button(
            self.window, text="Włącz światło", command=self.light_on_button_click
        )
        self.light_button_on.pack()

        self.light_button_off = tk.Button(
            self.window, text="Wyłącz światło", command=self.light_off_button_click
        )
        self.light_button_off.pack()

        self.socket_button_on = tk.Button(
            self.window, text="Włącz gniazdko", command=self.socket_on_button_click
        )
        self.socket_button_on.pack()

        self.socket_button_off = tk.Button(
            self.window, text="Wyłącz gniazdko", command=self.socket_off_button_click
        )
        self.socket_button_off.pack()

        self.dim_button = tk.Button(
            self.window, text="Przyciemnij światło", command=self.dim_button_click
        )
        self.dim_button.pack()

    def light_on_button_click(self):
        light = Light()
        light_on_command = LightOnCommand(light)
        self.remote_control.set_command(light_on_command)
        self.remote_control.press_button()

    def light_off_button_click(self):
        light = Light()
        light_off_command = LightOffCommand(light)
        self.remote_control.set_command(light_off_command)
        self.remote_control.press_button()

    def socket_on_button_click(self):
        socket = Socket()
        socket_on_command = SocketOnCommand(socket)
        self.remote_control.set_command(socket_on_command)
        self.remote_control.press_button()

    def socket_off_button_click(self):
        socket = Socket()
        socket_off_command = SocketOffCommand(socket)
        self.remote_control.set_command(socket_off_command)
        self.remote_control.press_button()

    def dim_button_click(self):
        light = Light()
        level = 50  # Poziom przyciemnienia
        dim_command = LightDimCommand(light, level)
        self.remote_control.set_command(dim_command)
        self.remote_control.press_button()

# Użycie wzorca Command z graficznym GUI
if __name__ == "__main__":
    light = Light()
    socket = Socket()
    remote_control = RemoteControl()
    gui = GUI(remote_control)
    gui.window.mainloop()

