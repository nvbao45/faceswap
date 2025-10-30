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
        self.dialog.geometry("550x750")
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
        
        # Separator
        tk.Frame(content, height=1, bg=Colors.SEPARATOR).pack(fill=tk.X, pady=15)
        
        # Section: Skip Frame Range
        StyledLabel(
            content,
            text=f"{Icons.SCISSORS} Skip Frame Range",
            size="section",
            bold=True,
            bg=Colors.BG_PANEL
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Enable skip option
        self.skip_enabled_var = tk.BooleanVar(value=self.config.get('skip_swap_enabled', False))
        
        skip_enabled_frame = StyledFrame(content, bg_type="panel")
        skip_enabled_frame.pack(fill=tk.X, pady=5)
        
        skip_check = tk.Checkbutton(
            skip_enabled_frame,
            text="Skip face swap for a range of frames (just copy original)",
            variable=self.skip_enabled_var,
            font=(Fonts.FAMILY, Fonts.SIZE_BUTTON),
            bg=Colors.BG_PANEL,
            fg=Colors.TEXT_PRIMARY,
            selectcolor=Colors.BG_DARK,
            activebackground=Colors.BG_PANEL,
            activeforeground=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            highlightthickness=0,
            cursor="hand2",
            command=self._toggle_skip_inputs
        )
        skip_check.pack(anchor=tk.W)
        
        StyledLabel(
            skip_enabled_frame,
            text="Useful to skip frames without faces or problematic sections",
            size="subtitle",
            color=Colors.TEXT_SECONDARY,
            bg=Colors.BG_PANEL
        ).pack(anchor=tk.W, padx=(25, 0), pady=(2, 0))
        
        # Range inputs
        range_frame = StyledFrame(content, bg_type="panel")
        range_frame.pack(fill=tk.X, pady=(10, 5))
        
        # Start frame
        start_label_frame = StyledFrame(range_frame, bg_type="panel")
        start_label_frame.pack(fill=tk.X, pady=3)
        
        StyledLabel(
            start_label_frame,
            text="Start frame:",
            size="button",
            bg=Colors.BG_PANEL
        ).pack(side=tk.LEFT, padx=(25, 10))
        
        self.skip_start_var = tk.StringVar(value=str(self.config.get('skip_swap_start', 0)))
        self.skip_start_entry = tk.Entry(
            start_label_frame,
            textvariable=self.skip_start_var,
            font=(Fonts.FAMILY, Fonts.SIZE_BUTTON),
            bg=Colors.BG_DARK,
            fg=Colors.TEXT_PRIMARY,
            insertbackground=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            width=15
        )
        self.skip_start_entry.pack(side=tk.LEFT)
        
        # End frame
        end_label_frame = StyledFrame(range_frame, bg_type="panel")
        end_label_frame.pack(fill=tk.X, pady=3)
        
        StyledLabel(
            end_label_frame,
            text="End frame:",
            size="button",
            bg=Colors.BG_PANEL
        ).pack(side=tk.LEFT, padx=(25, 10))
        
        self.skip_end_var = tk.StringVar(value=str(self.config.get('skip_swap_end', 0)))
        self.skip_end_entry = tk.Entry(
            end_label_frame,
            textvariable=self.skip_end_var,
            font=(Fonts.FAMILY, Fonts.SIZE_BUTTON),
            bg=Colors.BG_DARK,
            fg=Colors.TEXT_PRIMARY,
            insertbackground=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            width=15
        )
        self.skip_end_entry.pack(side=tk.LEFT)
        
        StyledLabel(
            range_frame,
            text="Example: Start=10, End=50 will copy frames 10-50 without swapping",
            size="subtitle",
            color=Colors.TEXT_SECONDARY,
            bg=Colors.BG_PANEL
        ).pack(anchor=tk.W, padx=(25, 0), pady=(5, 0))
        
        # Set initial state
        self._toggle_skip_inputs()
        
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
    
    def _toggle_skip_inputs(self):
        """Enable/disable skip range inputs based on checkbox"""
        if self.skip_enabled_var.get():
            self.skip_start_entry.config(state=tk.NORMAL)
            self.skip_end_entry.config(state=tk.NORMAL)
        else:
            self.skip_start_entry.config(state=tk.DISABLED)
            self.skip_end_entry.config(state=tk.DISABLED)
    
    def _on_save(self):
        """Save settings and close dialog"""
        self.config['delete_frames_after_merge'] = self.delete_frames_var.get()
        self.config['auto_save_progress'] = self.auto_save_var.get()
        self.config['skip_swap_enabled'] = self.skip_enabled_var.get()
        
        # Validate and save skip range
        try:
            start = int(self.skip_start_var.get())
            end = int(self.skip_end_var.get())
            
            if start < 0 or end < 0:
                messagebox.showerror("Invalid Range", "Frame numbers must be positive")
                return
            
            if self.skip_enabled_var.get() and start >= end:
                messagebox.showerror("Invalid Range", "Start frame must be less than end frame")
                return
            
            self.config['skip_swap_start'] = start
            self.config['skip_swap_end'] = end
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for frame range")
            return
        
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
