"""
Main Application Window
Refactored UI using modular components
"""
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import os
import sys

# Import UI components and styles
from .styles import Colors, Fonts, Layout, Icons
from .components import (
    StyledButton, StyledLabel, StyledFrame, Panel,
    ScrollableText, StatusBar, Separator, SectionHeader
)
from .config_dialog import ConfigDialog

# Import core modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core import (
    Automatic1111API,
    VideoProcessor,
    ProgressManager,
    FaceSwapProcessor
)
from src.utils import list_image_files, get_latest_file, ConfigManager


class FaceSwapApp:
    """Main application window for Face Swap Tool"""
    
    def __init__(self):
        """Initialize the application"""
        # Create main window
        self.root = tk.Tk()
        self.root.title("Face Swap Tool - Easy Face Swapping")
        self.root.geometry(f"{Layout.WINDOW_WIDTH}x{Layout.WINDOW_HEIGHT}")
        self.root.minsize(Layout.MIN_WIDTH, Layout.MIN_HEIGHT)
        self.root.resizable(True, True)  # Allow resizing
        self.root.configure(bg=Colors.BG_MAIN)
        
        # Initialize config manager and load config
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load()
        
        # Application state
        self.input_face = ""
        self.input_video = ""
        self.processing_unit = "CPU"
        self.input_type = "Single Image"
        self.is_paused = False
        self.is_running = False
        self.current_preview_image = None
        self.preview_visible = True
        
        # Initialize core components
        self.api = Automatic1111API()
        self.video_processor = VideoProcessor()
        self.progress_manager = ProgressManager()
        
        # Create UI
        self._create_ui()
        
        # Show welcome message and check for saved progress
        self.root.after(100, self._show_welcome_message)
        self.root.after(1000, self._check_and_resume_progress)
    
    def _create_ui(self):
        """Create the user interface"""
        # Main container
        main_container = StyledFrame(self.root, bg_type="main")
        main_container.pack(fill=tk.BOTH, expand=True, padx=Layout.PAD_MAIN, pady=Layout.PAD_MAIN)
        
        # Header
        self._create_header(main_container)
        
        # Content area (three-column layout)
        content_frame = StyledFrame(main_container, bg_type="main")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Controls (fixed width)
        self.left_panel = self._create_control_panel(content_frame)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, Layout.PANEL_GAP))
        self.left_panel.config(width=280)
        self.left_panel.pack_propagate(False)  # Prevent shrinking
        
        # Middle panel - Output log (fixed width)
        self.middle_panel = self._create_output_panel(content_frame)
        self.middle_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, Layout.PANEL_GAP))
        self.middle_panel.config(width=500)
        self.middle_panel.pack_propagate(False)  # Prevent shrinking
        
        # Right panel - Preview (responsive, takes remaining space)
        self.right_panel = self._create_preview_panel(content_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = StatusBar(main_container)
        self.status_bar.pack(fill=tk.X, pady=(Layout.SPACE_SECTION, 0))
    
    def _create_header(self, parent):
        """Create header section"""
        header_frame = StyledFrame(parent, bg_type="main")
        header_frame.pack(fill=tk.X, pady=(0, Layout.HEADER_PAD_BOTTOM))
        
        header_label = StyledLabel(
            header_frame,
            text=f"{Icons.APP} Face Swap Tool",
            size="header",
            bold=True,
            color=Colors.ACCENT
        )
        header_label.pack()
        
        subtitle_label = StyledLabel(
            header_frame,
            text="Easy Face Swapping with Pause & Resume",
            size="subtitle",
            color=Colors.TEXT_SECONDARY
        )
        subtitle_label.pack()
    
    def _create_control_panel(self, parent):
        """Create left control panel"""
        panel = StyledFrame(parent, bg_type="panel")
        
        # Settings Section
        SectionHeader(panel, Icons.SETTINGS, "Settings").pack(
            fill=tk.X, padx=Layout.PAD_SECTION, pady=(Layout.PAD_SECTION, Layout.SPACE_SECTION)
        )
        
        settings_frame = StyledFrame(panel, bg_type="panel")
        settings_frame.pack(fill=tk.X, padx=Layout.PAD_SECTION, pady=(0, Layout.SPACE_SECTION))
        
        # Config/Preferences button
        StyledButton(
            settings_frame,
            text=f"{Icons.SETTINGS} Preferences",
            style="secondary",
            command=self._open_config
        ).pack(fill=tk.X, pady=Layout.SPACE_BUTTON)
        
        self.processing_unit_button = StyledButton(
            settings_frame,
            text=f"{Icons.CPU} {self.processing_unit}",
            style="secondary",
            command=self._toggle_processing_unit
        )
        self.processing_unit_button.pack(fill=tk.X, pady=Layout.SPACE_BUTTON)
        
        self.input_type_button = StyledButton(
            settings_frame,
            text=f"{Icons.IMAGE} {self.input_type}",
            style="secondary",
            command=self._toggle_input_type
        )
        self.input_type_button.pack(fill=tk.X, pady=Layout.SPACE_BUTTON)
        
        Separator(panel).pack(fill=tk.X, padx=Layout.PAD_SECTION, pady=Layout.SPACE_SEPARATOR)
        
        # Input Files Section
        SectionHeader(panel, Icons.FOLDER, "Input Files").pack(
            fill=tk.X, padx=Layout.PAD_SECTION, pady=(Layout.SPACE_SEPARATOR, Layout.SPACE_SECTION)
        )
        
        input_frame = StyledFrame(panel, bg_type="panel")
        input_frame.pack(fill=tk.X, padx=Layout.PAD_SECTION, pady=(0, Layout.SPACE_SECTION))
        
        StyledButton(
            input_frame,
            text=f"{Icons.FACE} Choose Face",
            style="primary",
            command=self._select_face
        ).pack(fill=tk.X, pady=Layout.SPACE_BUTTON)
        
        StyledButton(
            input_frame,
            text=f"{Icons.VIDEO} Choose Video",
            style="primary",
            command=self._select_video
        ).pack(fill=tk.X, pady=Layout.SPACE_BUTTON)
        
        Separator(panel).pack(fill=tk.X, padx=Layout.PAD_SECTION, pady=Layout.SPACE_SEPARATOR)
        
        # Processing Section
        SectionHeader(panel, Icons.PROCESSING, "Processing").pack(
            fill=tk.X, padx=Layout.PAD_SECTION, pady=(Layout.SPACE_SEPARATOR, Layout.SPACE_SECTION)
        )
        
        processing_frame = StyledFrame(panel, bg_type="panel")
        processing_frame.pack(fill=tk.X, padx=Layout.PAD_SECTION, pady=(0, Layout.SPACE_SECTION))
        
        StyledButton(
            processing_frame,
            text=f"{Icons.SCISSORS} Split Video Into Frames",
            style="secondary",
            command=self._start_split_video
        ).pack(fill=tk.X, pady=Layout.SPACE_BUTTON)
        
        self.swap_button = StyledButton(
            processing_frame,
            text=f"{Icons.SWAP} Swap Face",
            style="success",
            command=self._start_swap_face
        )
        self.swap_button.pack(fill=tk.X, pady=Layout.SPACE_BUTTON)
        
        # Control buttons (pause/resume)
        control_frame = StyledFrame(processing_frame, bg_type="panel")
        control_frame.pack(fill=tk.X, pady=Layout.SPACE_BUTTON)
        
        self.pause_button = StyledButton(
            control_frame,
            text=f"{Icons.PAUSE} Pause",
            style="warning",
            size="small",
            command=self._pause_swap,
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        
        self.resume_button = StyledButton(
            control_frame,
            text=f"{Icons.PLAY} Resume",
            style="success",
            size="small",
            command=self._resume_swap,
            state=tk.DISABLED
        )
        self.resume_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))
        
        self.resume_crash_button = StyledButton(
            processing_frame,
            text=f"{Icons.SAVE} Resume from Crash",
            style="special",
            size="small",
            command=self._start_resume_swap
        )
        self.resume_crash_button.pack(fill=tk.X, pady=Layout.SPACE_BUTTON)
        
        self.merge_button = StyledButton(
            processing_frame,
            text=f"{Icons.MERGE} Merge Frames Into Video",
            style="secondary",
            command=self._start_merge_video
        )
        self.merge_button.pack(fill=tk.X, pady=Layout.SPACE_BUTTON)
        
        Separator(panel).pack(fill=tk.X, padx=Layout.PAD_SECTION, pady=Layout.SPACE_SEPARATOR)
        
        # Toggle Preview Button
        self.toggle_preview_button = StyledButton(
            panel,
            text=f"{Icons.HIDE} Hide Preview",
            style="utility",
            size="small",
            command=self._toggle_preview
        )
        self.toggle_preview_button.pack(fill=tk.X, padx=Layout.PAD_SECTION, pady=Layout.SPACE_BUTTON)
        
        # Exit Button
        StyledButton(
            panel,
            text=f"{Icons.EXIT} Exit",
            style="danger",
            size="small",
            command=self.root.quit
        ).pack(fill=tk.X, padx=Layout.PAD_SECTION, pady=(Layout.SPACE_SECTION, Layout.SPACE_BUTTON))
        
        return panel
    
    def _create_output_panel(self, parent):
        """Create middle output panel"""
        panel = StyledFrame(parent, bg_type="panel")
        
        SectionHeader(panel, Icons.LOG, "Output Log").pack(
            fill=tk.X, padx=Layout.PAD_SECTION, pady=(Layout.PAD_SECTION, Layout.SPACE_SECTION)
        )
        
        # Scrollable text output
        self.output_log = ScrollableText(panel)
        self.output_log.pack(fill=tk.BOTH, expand=True, padx=Layout.PAD_SECTION, pady=(0, Layout.PAD_SECTION))
        
        # Configure text tags for color coding
        text_widget = self.output_log.get_text_widget()
        text_widget.tag_config("error", foreground=Colors.ERROR, font=(Fonts.FAMILY_MONO, Fonts.SIZE_OUTPUT, Fonts.WEIGHT_BOLD))
        text_widget.tag_config("success", foreground=Colors.SUCCESS, font=(Fonts.FAMILY_MONO, Fonts.SIZE_OUTPUT))
        text_widget.tag_config("warning", foreground=Colors.WARNING, font=(Fonts.FAMILY_MONO, Fonts.SIZE_OUTPUT))
        text_widget.tag_config("info", foreground=Colors.INFO, font=(Fonts.FAMILY_MONO, Fonts.SIZE_OUTPUT))
        text_widget.tag_config("separator", foreground=Colors.SEPARATOR_LIGHT, font=(Fonts.FAMILY_MONO, Fonts.SIZE_OUTPUT))
        
        return panel
    
    def _create_preview_panel(self, parent):
        """Create right preview panel"""
        panel = StyledFrame(parent, bg_type="panel")
        
        self.preview_title_label = StyledLabel(
            panel,
            text=f"{Icons.PREVIEW} Result Preview",
            size="section",
            bold=True,
            bg=Colors.BG_PANEL
        )
        self.preview_title_label.pack(
            anchor=tk.W, padx=Layout.PAD_SECTION, pady=(Layout.PAD_SECTION, Layout.SPACE_SECTION)
        )
        
        # Preview frame
        preview_frame = StyledFrame(panel, bg_type="panel")
        preview_frame.configure(bg=Colors.BG_DARK, relief=tk.SUNKEN, borderwidth=2)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=Layout.PAD_SECTION, pady=(0, Layout.PAD_SECTION))
        
        self.preview_label = StyledLabel(
            preview_frame,
            text="No preview available\n\nProcessed frames will\nappear here",
            color=Colors.TEXT_SECONDARY,
            bg=Colors.BG_DARK,
            justify=tk.CENTER
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hidden state label (will be shown when preview is hidden)
        self.preview_hidden_label = StyledLabel(
            preview_frame,
            text=f"{Icons.HIDE}\n\nPreview Hidden\n\nClick 'Show Preview'\nto display",
            color=Colors.TEXT_SECONDARY,
            bg=Colors.BG_DARK,
            justify=tk.CENTER,
            size="section"
        )
        # Don't pack it yet - will show/hide as needed
        
        return panel
    
    # ===== Output Methods =====
    
    def _append_output(self, text):
        """Append text to output log with color coding"""
        text_widget = self.output_log.get_text_widget()
        text_widget.config(state=tk.NORMAL)
        
        # Add color tags
        start_index = text_widget.index(tk.END)
        text_widget.insert(tk.END, f"{text}\n")
        end_index = text_widget.index(tk.END)
        
        # Apply color based on content
        if any(keyword in text.lower() for keyword in ["error", "failed", "fail"]):
            text_widget.tag_add("error", start_index, end_index)
        elif any(keyword in text.lower() for keyword in ["finished", "completed", "ready", "success"]):
            text_widget.tag_add("success", start_index, end_index)
        elif any(keyword in text.lower() for keyword in ["warning", "pausing", "stopped"]):
            text_widget.tag_add("warning", start_index, end_index)
        elif "===" in text or "---" in text:
            text_widget.tag_add("separator", start_index, end_index)
        elif any(keyword in text.lower() for keyword in ["detected", "resuming", "selected"]):
            text_widget.tag_add("info", start_index, end_index)
        
        text_widget.config(state=tk.DISABLED)
        text_widget.see(tk.END)
        
        # Update status bar
        clean_message = text.strip()
        if clean_message and not clean_message.startswith("="):
            self.root.after(0, lambda: self._update_status(
                clean_message[:60] + "..." if len(clean_message) > 60 else clean_message
            ))
    
    def _update_status(self, message, color=None):
        """Update status bar"""
        self.status_bar.set_status(message, color)
    
    def _update_preview_image(self, image_path):
        """Update preview image with responsive sizing"""
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                
                # Get preview panel size dynamically
                self.right_panel.update_idletasks()
                panel_width = self.right_panel.winfo_width() - 60  # Account for padding
                panel_height = self.right_panel.winfo_height() - 120  # Account for title and padding
                
                # Use available panel size (much larger now)
                max_width = max(panel_width, 300) if panel_width > 0 else 600
                max_height = max(panel_height, 300) if panel_height > 0 else 600
                
                # Scale to fit the panel while maintaining aspect ratio
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(img)
                self.preview_label.config(image=photo, text="")
                self.preview_label.image = photo
                self.current_preview_image = image_path
                
                filename = os.path.basename(image_path)
                self.preview_title_label.config(text=f"{Icons.PREVIEW} Latest Result: {filename}")
        except Exception as e:
            print(f"Error loading preview: {e}")
    
    def _clear_preview_image(self):
        """Clear preview image"""
        self.preview_label.config(image="", text="No preview available\n\nProcessed frames will\nappear here")
        self.preview_label.image = None
        self.preview_title_label.config(text=f"{Icons.PREVIEW} Result Preview")
    
    # ===== UI Event Handlers =====
    
    def _toggle_preview(self):
        """Toggle preview panel visibility"""
        if self.preview_visible:
            # Hide preview content and show hidden message
            self.preview_label.pack_forget()
            self.preview_hidden_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.preview_title_label.config(text=f"{Icons.HIDE} Result Preview (Hidden)")
            self.preview_visible = False
            self.toggle_preview_button.config(text=f"{Icons.SHOW} Show Preview")
            self._append_output("Preview content hidden")
        else:
            # Show preview content and hide message
            self.preview_hidden_label.pack_forget()
            self.preview_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.preview_title_label.config(text=f"{Icons.PREVIEW} Result Preview")
            self.preview_visible = True
            self.toggle_preview_button.config(text=f"{Icons.HIDE} Hide Preview")
            self._append_output("Preview content shown")
    
    def _toggle_processing_unit(self):
        """Toggle processing unit (CPU/GPU)"""
        self.processing_unit = "GPU (CUDA)" if self.processing_unit == "CPU" else "CPU"
        self.processing_unit_button.config(text=f"{Icons.CPU} {self.processing_unit}")
        self._append_output("⚠️ Note: Automatic1111 needs to be restarted after changing")
        self._append_output("the processing unit for changes to apply!")
        self._update_status(f"Processing unit: {self.processing_unit}", Colors.SUCCESS)
    
    def _toggle_input_type(self):
        """Toggle input type (Single Image/Face Model)"""
        self.input_type = "Face Model" if self.input_type == "Single Image" else "Single Image"
        self.input_type_button.config(text=f"{Icons.IMAGE} {self.input_type}")
        self._update_status(f"Input type: {self.input_type}", Colors.SUCCESS)
    
    def _open_config(self):
        """Open configuration dialog"""
        dialog = ConfigDialog(self.root, self.config)
        result = dialog.show()
        
        if result:
            self.config = result
            # Save config to file
            if self.config_manager.save(self.config):
                self._append_output(f"{Icons.SUCCESS} Settings saved")
                self._update_status("Settings updated", Colors.SUCCESS)
            else:
                self._append_output(f"{Icons.ERROR} Failed to save settings")
                self._update_status("Failed to save settings", Colors.ERROR)
    
    def _select_face(self):
        """Open file dialog to select face"""
        path = "input_faces/" if self.input_type == "Single Image" else "input_faces_models"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        initial_dir = os.path.join(current_dir, "..", "..", path)
        
        file = filedialog.askopenfile(initialdir=initial_dir)
        if file:
            file_name = os.path.basename(file.name)
            self._append_output(f"{Icons.SUCCESS} Selected face: {file_name}")
            self.input_face = file.name
            self._update_status(f"Face selected: {file_name}", Colors.SUCCESS)
    
    def _select_video(self):
        """Open file dialog to select video"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        initial_dir = os.path.join(current_dir, "..", "..", "input_videos/")
        
        file = filedialog.askopenfile(initialdir=initial_dir)
        if file:
            file_name = os.path.basename(file.name)
            self._append_output(f"{Icons.SUCCESS} Selected video: {file_name}")
            self.input_video = file.name
            self._update_status(f"Video selected: {file_name}", Colors.SUCCESS)
    
    # ===== Processing Methods =====
    
    def _split_video(self):
        """Split video into frames"""
        if not self.input_video:
            self._append_output(f"{Icons.ERROR} Error: No video selected")
            self._update_status("Error: No video selected", Colors.ERROR)
            return
        
        self._append_output(f"{Icons.SCISSORS} Splitting video into frames...")
        self._update_status("Splitting video into frames...", Colors.WARNING)
        
        self.video_processor.extract_frames(self.input_video)
        
        self._append_output(f"{Icons.SUCCESS} Finished splitting video into frames")
        self._append_output("Ready to swap face")
        self._update_status(f"{Icons.SUCCESS} Video split complete - Ready to swap", Colors.SUCCESS)
    
    def _start_split_video(self):
        """Start video splitting in thread"""
        thread = threading.Thread(target=self._split_video)
        thread.start()
    
    def _swap_face(self, resume=False):
        """Perform face swapping"""
        if not resume and (not self.input_video or not self.input_face):
            self._append_output(f"{Icons.ERROR} Error: Select a face and a video first")
            self._update_status("Error: Select face and video", Colors.ERROR)
            return
        
        self.is_running = True
        self.is_paused = False
        
        if not resume:
            self.root.after(0, self._clear_preview_image)
        
        self.root.after(0, lambda: self._update_swap_buttons(True))
        
        files = sorted(os.listdir("extracted_frames/"))
        start_index = 0
        
        # Load progress if resuming
        if resume:
            progress = self.progress_manager.load()
            if progress:
                start_index = progress['current_index']
                self.input_face = progress['input_face']
                self.input_video = progress['input_video']
                self.input_type = progress['input_type']
                self.processing_unit = progress['processing_unit']
                self._append_output(f"Resuming from frame {start_index + 1}/{len(files)}")
            else:
                self._append_output("No progress found to resume")
                self.is_running = False
                self.root.after(0, lambda: self._update_swap_buttons(False))
                return
        
        # Determine source type
        source_choice = 0 if self.input_type == "Single Image" else 1
        input_model = "" if self.input_type == "Single Image" else self.input_face
        temp_input_face = self.input_face if self.input_type == "Face Model" else ""
        
        try:
            for index, file in enumerate(files):
                if index < start_index:
                    continue
                
                # Check pause
                while self.is_paused and self.is_running:
                    import time
                    time.sleep(0.1)
                
                # Check stop
                if not self.is_running:
                    self._append_output("Face swap stopped")
                    self.progress_manager.save(
                        index, len(files),
                        temp_input_face if self.input_type == "Face Model" else self.input_face,
                        self.input_video, self.input_type, self.processing_unit
                    )
                    self.root.after(0, lambda: self._update_swap_buttons(False))
                    return
                
                file_path = os.path.join("extracted_frames/", file)
                
                # Perform face swap
                face_input = "" if source_choice == 1 else self.input_face
                self.api.swap_face(file, face_input, input_model, file_path, self.processing_unit, source_choice)
                
                # Update preview
                result_path = os.path.join("finished_frames/", file)
                if os.path.exists(result_path):
                    self.root.after(0, lambda p=result_path: self._update_preview_image(p))
                
                # Save progress
                self.progress_manager.save(
                    index + 1, len(files),
                    temp_input_face if self.input_type == "Face Model" else self.input_face,
                    self.input_video, self.input_type, self.processing_unit
                )
                
                # Update progress
                progress_pct = ((index + 1) / len(files)) * 100
                self._append_output(f"{Icons.SUCCESS} Frame {index + 1}/{len(files)} ({progress_pct:.1f}%)")
                self.root.after(0, lambda p=progress_pct, i=index+1, t=len(files):
                               self._update_status(f"{Icons.PROCESSING} Processing: {i}/{t} frames ({p:.1f}%)", Colors.WARNING))
            
            self._append_output(f"{Icons.SUCCESS} Finished swapping faces")
            self._append_output("Ready to merge frames")
            self.progress_manager.clear()
            self._update_status(f"{Icons.SUCCESS} Face swap complete - Ready to merge", Colors.SUCCESS)
            
        except Exception as e:
            self._append_output(f"{Icons.ERROR} Error occurred: {str(e)}")
            self._append_output("Progress has been saved. You can resume later.")
            self._update_status(f"Error: {str(e)}", Colors.ERROR)
        finally:
            self.is_running = False
            self.root.after(0, lambda: self._update_swap_buttons(False))
    
    def _start_swap_face(self):
        """Start face swapping in thread"""
        thread = threading.Thread(target=self._swap_face, kwargs={'resume': False})
        thread.start()
    
    def _start_resume_swap(self):
        """Resume face swapping from crash"""
        thread = threading.Thread(target=self._swap_face, kwargs={'resume': True})
        thread.start()
    
    def _pause_swap(self):
        """Pause face swapping"""
        if self.is_running:
            self.is_paused = True
            self._append_output(f"{Icons.PAUSE} Pausing... (will pause after current frame)")
            self.root.after(0, self._toggle_pause_resume)
    
    def _resume_swap(self):
        """Resume face swapping"""
        if self.is_paused:
            self.is_paused = False
            self._append_output(f"{Icons.PLAY} Resuming face swap...")
            self.root.after(0, self._toggle_pause_resume)
    
    def _merge_video(self):
        """Merge frames into video"""
        self._append_output(f"{Icons.MERGE} Creating video from frames...")
        self._update_status("Creating video from frames...", Colors.WARNING)
        
        file_name_video = self.video_processor.create_video_from_frames("finished_frames/")
        
        self._append_output(f"{Icons.SOUND} Adding sound to video...")
        self._update_status("Adding sound to video...", Colors.WARNING)
        
        self.video_processor.add_audio(self.input_video, file_name_video)
        
        self._append_output(f"{Icons.SUCCESS} Finished creating video!")
        self._append_output(f"{Icons.FOLDER} Saved to: finished_videos/{file_name_video}")
        self._update_status(f"{Icons.SUCCESS} Video creation complete!", Colors.SUCCESS)
        
        self._delete_old_frames()
    
    def _start_merge_video(self):
        """Start video merging in thread"""
        thread = threading.Thread(target=self._merge_video)
        thread.start()
    
    def _delete_old_frames(self):
        """Delete processed frames based on config"""
        if not self.config.get('delete_frames_after_merge', True):
            self._append_output(f"{Icons.INFO} Keeping temporary frames (as per settings)")
            return
        
        from src.utils import clear_directory
        
        count1 = clear_directory("extracted_frames/")
        count2 = clear_directory("finished_frames/")
        
        self._append_output(f"Cleaned up {count1 + count2} temporary frames")
    
    # ===== UI Update Methods =====
    
    def _update_swap_buttons(self, is_running):
        """Update button states during swap"""
        if is_running:
            self.swap_button.config(state=tk.DISABLED, bg=Colors.BTN_DISABLED)
            self.pause_button.config(state=tk.NORMAL, bg=Colors.BTN_WARNING)
            self.resume_button.config(state=tk.DISABLED, bg=Colors.BTN_DISABLED)
            self.resume_crash_button.config(state=tk.DISABLED, bg=Colors.BTN_DISABLED)
            self.merge_button.config(state=tk.DISABLED, bg=Colors.BTN_DISABLED)
            self._update_status(f"{Icons.PROCESSING} Face swapping in progress...", Colors.WARNING)
        else:
            self.swap_button.config(state=tk.NORMAL, bg=Colors.BTN_SUCCESS)
            self.pause_button.config(state=tk.DISABLED, bg=Colors.BTN_DISABLED)
            self.resume_button.config(state=tk.DISABLED, bg=Colors.BTN_DISABLED)
            self.resume_crash_button.config(state=tk.NORMAL, bg="#5a4a7a")
            self.merge_button.config(state=tk.NORMAL, bg=Colors.BTN_SECONDARY)
            self._update_status(f"{Icons.SUCCESS} Ready", Colors.SUCCESS)
    
    def _toggle_pause_resume(self):
        """Toggle pause/resume buttons"""
        if self.is_paused:
            self.pause_button.config(state=tk.DISABLED, bg=Colors.BTN_DISABLED)
            self.resume_button.config(state=tk.NORMAL, bg=Colors.BTN_SUCCESS)
            self._update_status(f"{Icons.PAUSE} Paused - Click Resume to continue", Colors.WARNING)
        else:
            self.pause_button.config(state=tk.NORMAL, bg=Colors.BTN_WARNING)
            self.resume_button.config(state=tk.DISABLED, bg=Colors.BTN_DISABLED)
            self._update_status(f"{Icons.PLAY} Resumed - Processing...", Colors.SUCCESS)
    
    # ===== Startup Methods =====
    
    def _show_welcome_message(self):
        """Show welcome message"""
        self._append_output("=" * 50)
        self._append_output(f"{Icons.APP} Welcome to Face Swap Tool!")
        self._append_output("=" * 50)
        self._append_output(f"{Icons.SUCCESS} Pause/Resume feature enabled")
        self._append_output(f"{Icons.SUCCESS} Crash recovery enabled")
        self._append_output("")
        self._append_output("Quick Start:")
        self._append_output("1. Choose Face (input_faces folder)")
        self._append_output("2. Choose Video (input_videos folder)")
        self._append_output("3. Split Video Into Frames")
        self._append_output("4. Swap Face (requires Automatic1111 running)")
        self._append_output("5. Merge Frames Into Video")
        self._append_output("")
        self._append_output("Ready to begin!")
        self._append_output("=" * 50)
    
    def _check_and_resume_progress(self):
        """Check for saved progress on startup"""
        progress = self.progress_manager.load()
        if progress and self.progress_manager.is_recent(progress):
            self._append_output("=" * 50)
            self._append_output(f"{Icons.WARNING} PREVIOUS PROGRESS DETECTED!")
            self._append_output(f"Last processed: {progress['current_index']}/{progress['total_files']} frames")
            self._append_output(f"Video: {os.path.basename(progress['input_video'])}")
            face_name = os.path.basename(progress['input_face']) if progress['input_face'] else progress['input_type']
            self._append_output(f"Face: {face_name}")
            self._append_output("Click 'Resume from Crash' to continue from where you left off")
            self._append_output("or 'Swap Face' to start fresh")
            self._append_output("=" * 50)
            self._update_status(f"{Icons.WARNING} Previous progress found - Check output log", Colors.WARNING)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()
