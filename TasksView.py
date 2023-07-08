import customtkinter as ctk



class NewTaskWindow(ctk.CTkToplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("300x400+700+350")

        self.transient(parent)
        self.title("Nowe zadanie")
        
        
        #layout
        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure((1,2,3,4,5), weight=1, uniform='a')
        
        
        #fonts
        self.name_font = ctk.CTkFont(family="Abril Fatface", size=30, weight="bold")
        
        
        
        
        #title frame
        self.title_frame = ctk.CTkFrame(self, border_width=0, fg_color='transparent')
        self.title_frame.grid(row=0, column=0,sticky='nsew')
        
        self.title_entry = ctk.CTkEntry(self.title_frame,
                                        placeholder_text="Nazwa",
                                        font=self.name_font,
                                        corner_radius=10,
                                        fg_color='transparent',
                                        border_width=0
                                        )
        self.title_entry.pack(fill = "both", expand = True, side = "top")
        
        
        
        
        
        
        
        #description frame
        
        
        
    
