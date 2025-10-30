"""
Reusable UI Components
"""
import tkinter as tk
from tkinter import ttk
from .styles import Colors, Fonts, Layout, ButtonStyle


class StyledButton(tk.Button):
    """Styled button with consistent appearance"""
    def __init__(self, parent, text, style="primary", size="normal", **kwargs):
        # Get style configuration
        if style == "primary":
            style_config = ButtonStyle.primary()
        elif style == "success":
            style_config = ButtonStyle.success()
        elif style == "warning":
            style_config = ButtonStyle.warning()
        elif style == "danger":
            style_config = ButtonStyle.danger()
        elif style == "secondary":
            style_config = ButtonStyle.secondary()
        elif style == "special":
            style_config = ButtonStyle.special()
        elif style == "utility":
            style_config = ButtonStyle.utility()
        else:
            style_config = ButtonStyle.primary()
        
        # Get font size
        if size == "normal":
            font_size = Fonts.SIZE_BUTTON
            pad_x = Layout.PAD_BUTTON_H
            pad_y = Layout.PAD_BUTTON_V
        else:  # small
            font_size = Fonts.SIZE_BUTTON_SMALL
            pad_x = Layout.PAD_BUTTON_SMALL_H
            pad_y = Layout.PAD_BUTTON_SMALL_V
        
        # Merge configurations
        config = {
            "font": (Fonts.FAMILY, font_size),
            "padx": pad_x,
            "pady": pad_y,
            "borderwidth": 0,
            "highlightthickness": 0,
            **style_config,
            **kwargs
        }
        
        super().__init__(parent, text=text, **config)


class StyledLabel(tk.Label):
    """Styled label with consistent appearance"""
    def __init__(self, parent, text, size="normal", bold=False, color=None, **kwargs):
        # Get font size
        if size == "header":
            font_size = Fonts.SIZE_HEADER
        elif size == "section":
            font_size = Fonts.SIZE_SECTION
        elif size == "subtitle":
            font_size = Fonts.SIZE_SUBTITLE
        else:
            font_size = Fonts.SIZE_BUTTON
        
        # Get font weight
        weight = Fonts.WEIGHT_BOLD if bold else Fonts.WEIGHT_NORMAL
        
        # Get color
        fg = color if color else Colors.TEXT_PRIMARY
        
        config = {
            "font": (Fonts.FAMILY, font_size, weight),
            "bg": Colors.BG_MAIN,
            "fg": fg,
            **kwargs
        }
        
        super().__init__(parent, text=text, **config)


class StyledFrame(tk.Frame):
    """Styled frame with consistent background"""
    def __init__(self, parent, bg_type="panel", **kwargs):
        bg = Colors.BG_PANEL if bg_type == "panel" else Colors.BG_MAIN
        config = {
            "bg": bg,
            **kwargs
        }
        super().__init__(parent, **config)


class StyledText(tk.Text):
    """Styled text widget for output log"""
    def __init__(self, parent, **kwargs):
        config = {
            "font": (Fonts.FAMILY_MONO, Fonts.SIZE_OUTPUT),
            "bg": Colors.BG_PANEL,
            "fg": Colors.TEXT_PRIMARY,
            "insertbackground": Colors.TEXT_PRIMARY,
            "selectbackground": Colors.ACCENT,
            "relief": "flat",
            "borderwidth": 0,
            "highlightthickness": 0,
            **kwargs
        }
        super().__init__(parent, **config)


class StyledEntry(tk.Entry):
    """Styled entry widget"""
    def __init__(self, parent, **kwargs):
        config = {
            "font": (Fonts.FAMILY, Fonts.SIZE_BUTTON),
            "bg": Colors.BG_PANEL,
            "fg": Colors.TEXT_PRIMARY,
            "insertbackground": Colors.TEXT_PRIMARY,
            "selectbackground": Colors.ACCENT,
            "relief": "flat",
            "borderwidth": 1,
            "highlightthickness": 1,
            "highlightbackground": Colors.SEPARATOR,
            "highlightcolor": Colors.ACCENT,
            **kwargs
        }
        super().__init__(parent, **config)


class Separator(tk.Frame):
    """Horizontal separator line"""
    def __init__(self, parent, color=None, **kwargs):
        bg = color if color else Colors.SEPARATOR
        super().__init__(parent, height=1, bg=bg, **kwargs)


class SectionHeader(StyledFrame):
    """Section header with icon and title"""
    def __init__(self, parent, icon, title, **kwargs):
        super().__init__(parent, bg_type="main", **kwargs)
        
        label = StyledLabel(
            self,
            text=f"{icon} {title}",
            size="section",
            bold=True
        )
        label.pack(anchor="w")


class StatusBar(StyledFrame):
    """Status bar at the bottom of the window"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg_type="main", **kwargs)
        self.configure(bg=Colors.BG_STATUS)
        
        # Status label
        self.status_label = StyledLabel(
            self,
            text="Ready",
            size="subtitle",
            bg=Colors.BG_STATUS,
            fg=Colors.TEXT_SECONDARY
        )
        self.status_label.pack(side="left", padx=Layout.PAD_SECTION)
    
    def set_status(self, text, color=None):
        """Update status text and color"""
        self.status_label.configure(text=text)
        if color:
            self.status_label.configure(fg=color)


class Panel(StyledFrame):
    """Panel with title and content area"""
    def __init__(self, parent, title, icon=None, **kwargs):
        super().__init__(parent, bg_type="panel", **kwargs)
        
        # Title
        title_text = f"{icon} {title}" if icon else title
        title_label = StyledLabel(
            self,
            text=title_text,
            size="section",
            bold=True,
            bg=Colors.BG_PANEL
        )
        title_label.pack(anchor="w", padx=Layout.PAD_SECTION, pady=(Layout.PAD_SECTION, 10))
        
        # Content area
        self.content = StyledFrame(self, bg_type="panel")
        self.content.pack(fill="both", expand=True, padx=Layout.PAD_SECTION, pady=(0, Layout.PAD_SECTION))
    
    def get_content(self):
        """Get the content frame"""
        return self.content


class ScrollableText(StyledFrame):
    """Text widget with scrollbar"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg_type="panel", **kwargs)
        
        # Text widget
        self.text = StyledText(self, wrap="word")
        self.text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(
            self,
            command=self.text.yview,
            bg=Colors.BG_PANEL,
            troughcolor=Colors.BG_DARK,
            activebackground=Colors.ACCENT,
            highlightthickness=0,
            borderwidth=0
        )
        scrollbar.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=scrollbar.set)
    
    def get_text_widget(self):
        """Get the text widget"""
        return self.text
    
    def append(self, text, tag=None):
        """Append text with optional tag"""
        self.text.insert("end", text, tag)
        self.text.see("end")
    
    def clear(self):
        """Clear all text"""
        self.text.delete("1.0", "end")


class ToggleButton(StyledButton):
    """Button that toggles between two states"""
    def __init__(self, parent, text_on, text_off, command=None, **kwargs):
        self.text_on = text_on
        self.text_off = text_off
        self.is_on = False
        self._toggle_command = command
        
        super().__init__(
            parent,
            text=text_off,
            command=self._on_toggle,
            **kwargs
        )
    
    def _on_toggle(self):
        """Internal toggle handler"""
        self.toggle()
        if self._toggle_command:
            self._toggle_command(self.is_on)
    
    def toggle(self):
        """Toggle the button state"""
        self.is_on = not self.is_on
        self.configure(text=self.text_on if self.is_on else self.text_off)
    
    def set_state(self, is_on):
        """Set the button state explicitly"""
        if self.is_on != is_on:
            self.is_on = is_on
            self.configure(text=self.text_on if self.is_on else self.text_off)


class ImagePreview(StyledFrame):
    """Image preview widget"""
    def __init__(self, parent, max_size=Layout.PREVIEW_MAX_SIZE, **kwargs):
        super().__init__(parent, bg_type="panel", **kwargs)
        self.max_size = max_size
        
        # Image label
        self.image_label = StyledLabel(
            self,
            text="No preview available",
            bg=Colors.BG_PANEL,
            fg=Colors.TEXT_SECONDARY
        )
        self.image_label.pack(expand=True)
        
        self.current_image = None
    
    def set_image(self, image):
        """Set the preview image (PIL Image)"""
        from PIL import Image as PILImage, ImageTk
        
        if image:
            # Resize if needed
            image.thumbnail((self.max_size, self.max_size), PILImage.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Update label
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo  # Keep a reference
            self.current_image = photo
        else:
            self.clear()
    
    def clear(self):
        """Clear the preview"""
        self.image_label.configure(image="", text="No preview available")
        self.current_image = None
