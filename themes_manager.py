
import customtkinter as ctk


class Theme:
    """Base class for themes.Contains default colors and fonts"""
    
    #Colors
    BAR_COLOR = 0x201E26 
    BACKGROUND_MAIN_COLOR = "#201E26"
    FOREGROUND_FRAME = "#2B2C39"
    FOREGROUND_HOVER_FRAME = "#272834"
    
    BUTTON_COLOR = "#3F6E58"
    BUTTON_HOVER_COLOR = "#38624E" 
    
    ENTRY_COLOR = "#272834"
    BORDER_ENTRY_COLOR = "#1F2029"
    
    TILE_TASK_COLOR = "#2D3364" 
    TILE_TASK_HOVER_COLOR = "#333A71" 
    
    SCROLLBAR_COLOR = "#555661"
    SCROLLBAR_HOVER_COLOR = "#6b6b74"
    

    
    
    @classmethod
    def get_colors(cls):
        """Returns a dictionary with colors for the given theme"""
        return {
            "bar": cls.BAR_COLOR,
       
            "background": cls.BACKGROUND_MAIN_COLOR,
            "fg_frame": cls.FOREGROUND_FRAME,
            "fg_hover_frame": cls.FOREGROUND_HOVER_FRAME,
            
            "button": cls.BUTTON_COLOR,
            "button_hover": cls.BUTTON_HOVER_COLOR,
            
            "entry": cls.ENTRY_COLOR,
            "border_entry": cls.BORDER_ENTRY_COLOR,
            
            "tile": cls.TILE_TASK_COLOR,
            "tile_hover": cls.TILE_TASK_HOVER_COLOR,
            
            "scrollbar": cls.SCROLLBAR_COLOR,
            "scrollbar_hover": cls.SCROLLBAR_HOVER_COLOR,
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


#Fonts
DEFAULT_FONT = {"family": "San Francisco", "size": 13, "weight": "normal"}
DEFAULT_BOLD_FONT = {"family": "San Francisco", "size": 13, "weight": "bold"}
HEADER_FONT = {"family": "San Francisco", "size": 35, "weight": "bold"}
SMALL_HEADER_FONT = {"family": "San Francisco", "size": 22, "weight": "bold"}
BUTTON_FONT = {"family": "San Francisco", "size": 15, "weight": "normal"}
ENTRY_FONT = {"family": "San Francisco", "size": 15, "weight": "normal"}

CLOCK_FONT = {"family": "San Francisco", "size": 25, "weight": "bold"}
DATE_FONT = {"family": "San Francisco", "size": 15, "weight": "bold"}


FONTS = {
    "default": DEFAULT_FONT,
    "default_bold": DEFAULT_BOLD_FONT,
    "header": HEADER_FONT,
    "small_header": SMALL_HEADER_FONT,
    "button": BUTTON_FONT,
    "entry": ENTRY_FONT,
    "clock": CLOCK_FONT,
    "date": DATE_FONT,
}  

def get_font_attributes(font_name):
    """Returns the font attributes based on the font name"""
    return FONTS.get(font_name, DEFAULT_FONT)

def get_ctk_font(font_name):
    """Returns the CTkFont instance based on the font name"""
    font_attributes = get_font_attributes(font_name)
    return ctk.CTkFont(family=font_attributes["family"],
                       size=font_attributes["size"],
                       weight=font_attributes["weight"])
