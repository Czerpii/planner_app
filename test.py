import tkinter as tk
from tkcalendar import Calendar
import datetime

class DateDisplay:
    def __init__(self, parent):
        self.label = tk.Label(parent, text="")
        self.label.pack(padx=10, pady=10)

    def update_date(self, event):
        date = event.widget.selection_get()
        if date is not None:
            self.label.config(text=date.strftime('%Y-%m-%d'))

class App:
    def __init__(self, root):
        self.root = root
        self.cal = Calendar(root)
        self.cal.pack(padx=10, pady=10)

        self.date_display = DateDisplay(root)

        self.cal.bind("<<CalendarSelected>>", self.date_display.update_date)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Kalendarz")
    
    app = App(root)
    
    root.mainloop()
