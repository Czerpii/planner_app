import customtkinter as ctk

class Theme:
    """
    Base class representing a theme. This class contains default colors and fonts 
    for various UI elements.
    """
    
    # Colors for different UI elements
    BAR_COLOR = 0x201E26  # Color for bars
    BACKGROUND_MAIN_COLOR = "#201E26"  # Main background color
    FOREGROUND_FRAME = "#2B2C39"  # Foreground color for frames
    FOREGROUND_HOVER_FRAME = "#272834"  # Hover color for frames
    
    BUTTON_COLOR = "#3F6E58"  # Default button color
    BUTTON_HOVER_COLOR = "#38624E"  # Button color when hovered over
    
    ENTRY_COLOR = "#272834"  # Entry widget color
    BORDER_ENTRY_COLOR = "#1F2029"  # Border color for entry widgets
    
    TILE_TASK_COLOR = "#2D3364"  # Color for task tiles
    TILE_TASK_HOVER_COLOR = "#333A71"  # Hover color for task tiles
    
    SCROLLBAR_COLOR = "#555661"  # Scrollbar color
    SCROLLBAR_HOVER_COLOR = "#6b6b74"  # Hover color for scrollbar
    
    @classmethod
    def get_colors(cls):
        """
        Returns a dictionary containing colors for various UI elements based on the theme.
        
        Returns:
            dict: A dictionary mapping UI elements to their respective colors.
        """
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

# Current theme instance
_current_theme = Theme

def set_theme(theme_name):
    """
    Sets the application theme based on the provided theme name.
    
    Args:
        theme_name (str): The name of the theme to set.
    """
    global _current_theme
    themes = {
        "base": Theme,
    }
    _current_theme = themes.get(theme_name, Theme)
    
def get_color(color_name):
    """
    Fetches the color for a given UI element based on the current theme.
    
    Args:
        color_name (str): The name of the UI element.
        
    Returns:
        str: The color code for the UI element.
    """
    colors = _current_theme.get_colors()
    return colors.get(color_name)

# Font configurations for different UI elements
DEFAULT_FONT = {"family": "San Francisco", "size": 13, "weight": "normal"}
DEFAULT_BOLD_FONT = {"family": "San Francisco", "size": 13, "weight": "bold"}
HEADER_FONT = {"family": "San Francisco", "size": 35, "weight": "bold"}
SMALL_HEADER_FONT = {"family": "San Francisco", "size": 22, "weight": "bold"}
BUTTON_FONT = {"family": "San Francisco", "size": 15, "weight": "normal"}
ENTRY_FONT = {"family": "San Francisco", "size": 15, "weight": "normal"}
CLOCK_FONT = {"family": "San Francisco", "size": 25, "weight": "bold"}
DATE_FONT = {"family": "San Francisco", "size": 15, "weight": "bold"}

# Dictionary mapping font names to their configurations
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
    """
    Fetches the font attributes for a given font name.
    
    Args:
        font_name (str): The name of the font.
        
    Returns:
        dict: A dictionary containing font attributes.
    """
    return FONTS.get(font_name, DEFAULT_FONT)

def get_ctk_font(font_name):
    """
    Returns a CTkFont instance based on the provided font name.
    
    Args:
        font_name (str): The name of the font.
        
    Returns:
        ctk.CTkFont: An instance of CTkFont with the specified attributes.
    """
    font_attributes = get_font_attributes(font_name)
    return ctk.CTkFont(family=font_attributes["family"],
                       size=font_attributes["size"],
                       weight=font_attributes["weight"])
