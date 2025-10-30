"""
UI Styling Constants and Theme Configuration
"""

# Color Palette
class Colors:
    """Color scheme for the application"""
    # Background colors
    BG_MAIN = "#1e1e1e"
    BG_PANEL = "#2d2d2d"
    BG_DARK = "#1a1a1a"
    BG_STATUS = "#252525"
    
    # Accent colors
    ACCENT = "#007acc"
    ACCENT_HOVER = "#005a9e"
    
    # Text colors
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#cccccc"
    
    # Status colors
    SUCCESS = "#4ec9b0"
    WARNING = "#ce9178"
    ERROR = "#f48771"
    INFO = "#569cd6"
    
    # Button colors
    BTN_PRIMARY = "#007acc"
    BTN_SUCCESS = "#4ec9b0"
    BTN_WARNING = "#ce9178"
    BTN_DANGER = "#8b0000"
    BTN_SECONDARY = "#3c3c3c"
    BTN_DISABLED = "#2a2a2a"
    
    # Separator
    SEPARATOR = "#444444"
    SEPARATOR_LIGHT = "#858585"


# Fonts
class Fonts:
    """Font configurations"""
    FAMILY = "Segoe UI"
    FAMILY_MONO = "Consolas"
    
    # Font sizes
    SIZE_HEADER = 24
    SIZE_SUBTITLE = 10
    SIZE_SECTION = 12
    SIZE_BUTTON = 10
    SIZE_BUTTON_SMALL = 9
    SIZE_OUTPUT = 10
    SIZE_STATUS = 9
    
    # Font weights
    WEIGHT_BOLD = "bold"
    WEIGHT_NORMAL = "normal"


# Layout
class Layout:
    """Layout spacing and dimensions"""
    # Window dimensions
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 990
    MIN_WIDTH = 1200
    MIN_HEIGHT = 990
    
    # Padding
    PAD_MAIN = 20
    PAD_SECTION = 15
    PAD_BUTTON_H = 20
    PAD_BUTTON_V = 10
    PAD_BUTTON_SMALL_H = 15
    PAD_BUTTON_SMALL_V = 8
    
    # Spacing
    SPACE_SECTION = 15
    SPACE_BUTTON = 2
    SPACE_SEPARATOR = 10
    
    # Header
    HEADER_PAD_BOTTOM = 20
    
    # Panel spacing
    PANEL_GAP = 10
    
    # Preview
    PREVIEW_MAX_SIZE = 400


# Button Styles
class ButtonStyle:
    """Button style configurations"""
    @staticmethod
    def primary():
        return {
            "bg": Colors.BTN_PRIMARY,
            "fg": Colors.TEXT_PRIMARY,
            "activebackground": Colors.ACCENT_HOVER,
            "relief": "flat",
            "cursor": "hand2"
        }
    
    @staticmethod
    def success():
        return {
            "bg": Colors.BTN_SUCCESS,
            "fg": "#000000",
            "activebackground": "#3da88a",
            "relief": "flat",
            "cursor": "hand2"
        }
    
    @staticmethod
    def warning():
        return {
            "bg": Colors.BTN_WARNING,
            "fg": "#000000",
            "activebackground": "#b87a5e",
            "relief": "flat",
            "cursor": "hand2"
        }
    
    @staticmethod
    def danger():
        return {
            "bg": Colors.BTN_DANGER,
            "fg": Colors.TEXT_PRIMARY,
            "activebackground": "#a00000",
            "relief": "flat",
            "cursor": "hand2"
        }
    
    @staticmethod
    def secondary():
        return {
            "bg": Colors.BTN_SECONDARY,
            "fg": Colors.TEXT_PRIMARY,
            "activebackground": "#4a4a4a",
            "relief": "flat",
            "cursor": "hand2"
        }
    
    @staticmethod
    def special():
        """Special button (e.g., resume from crash)"""
        return {
            "bg": "#5a4a7a",
            "fg": Colors.TEXT_PRIMARY,
            "activebackground": "#4a3a6a",
            "relief": "flat",
            "cursor": "hand2"
        }
    
    @staticmethod
    def utility():
        """Utility button (e.g., toggle preview)"""
        return {
            "bg": "#4a4a4a",
            "fg": Colors.TEXT_PRIMARY,
            "activebackground": "#5a5a5a",
            "relief": "flat",
            "cursor": "hand2"
        }


# Text Tag Styles (for output log)
class TextTags:
    """Text widget tag configurations"""
    ERROR = {
        "foreground": Colors.ERROR,
        "font": (Fonts.FAMILY_MONO, Fonts.SIZE_OUTPUT, Fonts.WEIGHT_BOLD)
    }
    
    SUCCESS = {
        "foreground": Colors.SUCCESS,
        "font": (Fonts.FAMILY_MONO, Fonts.SIZE_OUTPUT)
    }
    
    WARNING = {
        "foreground": Colors.WARNING,
        "font": (Fonts.FAMILY_MONO, Fonts.SIZE_OUTPUT)
    }
    
    INFO = {
        "foreground": Colors.INFO,
        "font": (Fonts.FAMILY_MONO, Fonts.SIZE_OUTPUT)
    }
    
    SEPARATOR = {
        "foreground": Colors.SEPARATOR_LIGHT,
        "font": (Fonts.FAMILY_MONO, Fonts.SIZE_OUTPUT)
    }


# Icons (Emojis)
class Icons:
    """Icon/Emoji constants"""
    APP = "🎬"
    SETTINGS = "⚙️"
    CPU = "🖥️"
    IMAGE = "📷"
    FOLDER = "📁"
    FACE = "👤"
    VIDEO = "🎥"
    PROCESSING = "⚡"
    SCISSORS = "✂️"
    SWAP = "🔄"
    PAUSE = "⏸️"
    PLAY = "▶️"
    SAVE = "💾"
    MERGE = "🎬"
    LOG = "📋"
    PREVIEW = "🖼️"
    HIDE = "🙈"
    SHOW = "👁️"
    EXIT = "🚪"
    SUCCESS = "✓"
    ERROR = "❌"
    WARNING = "⚠️"
    SOUND = "🔊"
