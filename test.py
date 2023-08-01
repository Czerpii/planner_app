import tkinter as tk
import customtkinter as ctk
import color_themes

def change_theme(theme):
    colors = getattr(color_themes, theme)
    root.config(bg=colors["background_color"])
    label.config(fg=colors["text_color"], bg=colors["background_color"])
    button.config(fg=colors["text_color"], bg=colors["button_color"], activebackground=colors["highlight_color"])
    entry.config(fg=colors["text_color"], bg=colors["background_color"], insertbackground=colors["text_color"])
    text_box.config(fg=colors["text_color"], bg=colors["background_color"])



root = tk.Tk()
root.title("Color Theme Tester")

label = tk.Label(root, text="Welcome to the Color Theme Tester!")
label.pack(pady=10)

button = tk.Button(root, text="Click me!")
button.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=10)

text_box = tk.Text(root)
text_box.pack(pady=10)


theme_button1 = tk.Button(root, text="Change to Theme 1", command=lambda: change_theme("color_theme_1"))
theme_button1.pack(pady=10)

theme_button2 = tk.Button(root, text="Change to Theme 2", command=lambda: change_theme("color_theme_2"))
theme_button2.pack(pady=10)

theme_button3 = tk.Button(root, text="Change to Theme 3", command=lambda: change_theme("color_theme_3"))
theme_button3.pack(pady=10)

theme_button4 = tk.Button(root, text="Change to Theme 4", command=lambda: change_theme("color_theme_4"))
theme_button4.pack(pady=10)

theme_button5 = tk.Button(root, text="Change to Theme 5", command=lambda: change_theme("color_theme_5"))
theme_button5.pack(pady=10)

theme_button6 = tk.Button(root, text="Change to Theme 6", command=lambda: change_theme("color_theme_6"))
theme_button6.pack(pady=10)

theme_button7 = tk.Button(root, text="Change to Theme 7", command=lambda: change_theme("color_theme_7"))
theme_button7.pack(pady=10)

theme_button8 = tk.Button(root, text="Change to Theme 8", command=lambda: change_theme("color_theme_8"))
theme_button8.pack(pady=10)

theme_button9 = tk.Button(root, text="Change to Theme 9", command=lambda: change_theme("color_theme_9"))
theme_button9.pack(pady=10)

theme_button10 = tk.Button(root, text="Change to Theme 10", command=lambda: change_theme("color_theme_10"))
theme_button10.pack(pady=10)


root.mainloop()

