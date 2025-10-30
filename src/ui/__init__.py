"""
UI Package
Contains all user interface components and styling
"""

from .styles import Colors, Fonts, Layout, ButtonStyle, TextTags, Icons
from .components import (
    StyledButton,
    StyledLabel,
    StyledFrame,
    StyledText,
    StyledEntry,
    Separator,
    SectionHeader,
    StatusBar,
    Panel,
    ScrollableText,
    ToggleButton,
    ImagePreview
)
from .config_dialog import ConfigDialog
from .main_window import FaceSwapApp

__all__ = [
    # Main Application
    'FaceSwapApp',
    # Dialogs
    'ConfigDialog',
    # Styles
    'Colors',
    'Fonts',
    'Layout',
    'ButtonStyle',
    'TextTags',
    'Icons',
    # Components
    'StyledButton',
    'StyledLabel',
    'StyledFrame',
    'StyledText',
    'StyledEntry',
    'Separator',
    'SectionHeader',
    'StatusBar',
    'Panel',
    'ScrollableText',
    'ToggleButton',
    'ImagePreview'
]
