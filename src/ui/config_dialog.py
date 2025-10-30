"""
Configuration Dialog
Settings window for application preferences
"""
import tkinter as tk
from tkinter import messagebox
from .styles import Colors, Fonts, Layout, Icons
from .components import StyledButton, StyledLabel, StyledFrame


class ConfigDialog:
    """Configuration dialog window"""
    
    def __init__(self, parent, config):
        """
        Initialize configuration dialog
        
        Args:
            parent: Parent window
            config: Dictionary with current configuration
        """
        self.parent = parent
        self.config = config.copy()  # Work with a copy
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("550x500")
        self.dialog.configure(bg=Colors.BG_MAIN)
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self._center_on_parent()
        
        # Create UI
        self._create_ui()
    
    def _center_on_parent(self):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_ui(self):
        """Create dialog UI"""
        # Header
        header_frame = StyledFrame(self.dialog, bg_type="main")
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        StyledLabel(
            header_frame,
            text=f"{Icons.SETTINGS} Settings",
            size="header",
            bold=True,
            color=Colors.ACCENT
        ).pack()
        
        StyledLabel(
            header_frame,
            text="Configure application preferences",
            size="subtitle",
            color=Colors.TEXT_SECONDARY
        ).pack()
        
        # Settings panel
        settings_panel = StyledFrame(self.dialog, bg_type="panel")
        settings_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Content
        content = StyledFrame(settings_panel, bg_type="panel")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Section: Cleanup Options
        StyledLabel(
            content,
            text=f"{Icons.FOLDER} Cleanup Options",
            size="section",
            bold=True,
            bg=Colors.BG_PANEL
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Delete frames option
        self.delete_frames_var = tk.BooleanVar(value=self.config.get('delete_frames_after_merge', True))
        
        delete_frame = StyledFrame(content, bg_type="panel")
        delete_frame.pack(fill=tk.X, pady=5)
        
        delete_check = tk.Checkbutton(
            delete_frame,
            text="Delete extracted frames after merging video",
            variable=self.delete_frames_var,
            font=(Fonts.FAMILY, Fonts.SIZE_BUTTON),
            bg=Colors.BG_PANEL,
            fg=Colors.TEXT_PRIMARY,
            selectcolor=Colors.BG_DARK,
            activebackground=Colors.BG_PANEL,
            activeforeground=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            highlightthickness=0,
            cursor="hand2"
        )
        delete_check.pack(anchor=tk.W)
        
        StyledLabel(
            delete_frame,
            text="Automatically clean up temporary frame files to save disk space",
            size="subtitle",
            color=Colors.TEXT_SECONDARY,
            bg=Colors.BG_PANEL
        ).pack(anchor=tk.W, padx=(25, 0), pady=(2, 0))
        
        # Separator
        tk.Frame(content, height=1, bg=Colors.SEPARATOR).pack(fill=tk.X, pady=15)
        
        # Section: Processing Options
        StyledLabel(
            content,
            text=f"{Icons.PROCESSING} Processing Options",
            size="section",
            bold=True,
            bg=Colors.BG_PANEL
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Auto-save progress option
        self.auto_save_var = tk.BooleanVar(value=self.config.get('auto_save_progress', True))
        
        save_frame = StyledFrame(content, bg_type="panel")
        save_frame.pack(fill=tk.X, pady=5)
        
        save_check = tk.Checkbutton(
            save_frame,
            text="Auto-save progress after each frame",
            variable=self.auto_save_var,
            font=(Fonts.FAMILY, Fonts.SIZE_BUTTON),
            bg=Colors.BG_PANEL,
            fg=Colors.TEXT_PRIMARY,
            selectcolor=Colors.BG_DARK,
            activebackground=Colors.BG_PANEL,
            activeforeground=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            highlightthickness=0,
            cursor="hand2"
        )
        save_check.pack(anchor=tk.W)
        
        StyledLabel(
            save_frame,
            text="Enable crash recovery by saving progress continuously",
            size="subtitle",
            color=Colors.TEXT_SECONDARY,
            bg=Colors.BG_PANEL
        ).pack(anchor=tk.W, padx=(25, 0), pady=(2, 0))
        
        # Button panel
        button_panel = StyledFrame(self.dialog, bg_type="main")
        button_panel.pack(fill=tk.X, padx=20, pady=20)
        
        button_frame = StyledFrame(button_panel, bg_type="main")
        button_frame.pack(anchor=tk.CENTER)
        
        StyledButton(
            button_frame,
            text=f"{Icons.SUCCESS} Save",
            style="success",
            command=self._on_save
        ).pack(side=tk.LEFT, padx=10, pady=5)
        
        StyledButton(
            button_frame,
            text="Cancel",
            style="secondary",
            command=self._on_cancel
        ).pack(side=tk.LEFT, padx=10, pady=5)
    
    def _on_save(self):
        """Save settings and close dialog"""
        self.config['delete_frames_after_merge'] = self.delete_frames_var.get()
        self.config['auto_save_progress'] = self.auto_save_var.get()
        self.result = self.config
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Cancel and close dialog"""
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        """Show dialog and wait for result"""
        self.dialog.wait_window()
        return self.result
