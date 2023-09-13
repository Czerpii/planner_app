

class Theme:
    """Base class for themes.Contains default colors and fonts"""
    
    #Colors
    BAR_COLOR = 0x8B451380  # Półprzezroczysty brąz
    BACKGROUND_MAIN_COLOR = "#8B4513"  # Główny kolor tła - ciemny brąz
    FOREGROUND_INFOBAR_COLOR = "#A0522D"  # Kolor tekstu na pasku informacyjnym - średni brąz
    TASK_FRAME_COLOR = "#D2691E"  # Kolor ramki zadania - jasny brąz
    BUTTON_COLOR = "#CD853F"  # Kolor przycisku - beżowy
    BUTTON_HOVER_COLOR = "#F4A460"  # Kolor przycisku po najechaniu - jasny beż
    SCROLLBAR_COLOR = "#8B4513"  # Kolor paska przewijania - ciemny brąz
    SCROLLBAR_HOVER_COLOR = "#A0522D"  # Kolor paska przewijania po najechaniu - średni brąz
    TILE_TASK_COLOR = "#CD853F"  # Kolor kafelka zadania - beżowy
    TILE_TASK_HOVER_COLOR = "#F4A460"  # Kolor kafelka zadania po najechaniu - jasny beż
    ENTRY_COLOR = "#DEB887"  # Kolor wpisu - jasny beż
    TEXT_BUTTON_COLOR = ""

    
    
    #Fonts
    DEFAULT_FONT = ("Arial", )
    HEADER_FONT = ("Arial Bold",)
    BUTTON_FONT = ("Arial")
    
    
    
    @classmethod
    def get_colors(cls):
        """Returns a dictionary with colors for the given theme"""
        return {
            "bar": cls.BAR_COLOR,
            "background": cls.BACKGROUND_MAIN_COLOR,
            "foreground_infobar": cls.FOREGROUND_INFOBAR_COLOR,
            "task_frame": cls.TASK_FRAME_COLOR,
            "button": cls.BUTTON_COLOR,
            "button_hover": cls.BUTTON_HOVER_COLOR,
            "scrollbar": cls.SCROLLBAR_COLOR,
            "scrollbar_hover": cls.SCROLLBAR_HOVER_COLOR,
            "tile": cls.TILE_TASK_COLOR,
            "tile_hover": cls.TILE_TASK_HOVER_COLOR,
            "entry": cls.ENTRY_COLOR
        }
    
    

_current_theme = Theme

def set_theme(theme_name):
    """Sets the theme based on the provided name"""
    global _current_theme
    themes = {
        "base": Theme,
        
    }
    _current_theme = themes.get(theme_name, Theme)
    


def get_color(color_name):
    """Returns the color based on the color name"""
    colors = _current_theme.get_colors()
    return colors.get(color_name)

