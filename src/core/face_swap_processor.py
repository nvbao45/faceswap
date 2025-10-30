"""
Face swap processing logic
"""
import os
import time
from .api_handler import Automatic1111API
from .progress_manager import ProgressManager


class FaceSwapProcessor:
    """Handle face swapping operations"""
    
    def __init__(self, api_url="http://127.0.0.1:7860"):
        self.api = Automatic1111API(api_url)
        self.progress_manager = ProgressManager()
        self.is_paused = False
        self.is_running = False
    
    def process_frames(self, face_image, input_video, input_type, processing_unit,
                      start_index=0, on_frame_complete=None, on_progress=None, on_complete=None, on_error=None):
        """
        Process frames with face swap
        
        Args:
            face_image: Path to face image or model
            input_video: Path to input video
            input_type: "Single Image" or "Face Model"
            processing_unit: "CPU" or "GPU (CUDA)"
            start_index: Frame index to start from (for resume)
            on_frame_complete: Callback(index, total, percentage, result_path)
            on_progress: Callback(message)
            on_complete: Callback()
            on_error: Callback(error_message)
        """
        self.is_running = True
        self.is_paused = False
        
        try:
            files = os.listdir("extracted_frames/")
            files.sort()  # Ensure consistent ordering
            
            if input_type == "Single Image":
                source_choice = 0
                input_model = ""
                temp_input_face = face_image
            else:
                source_choice = 1
                input_model = face_image
                temp_input_face = face_image
                face_image = ""
            
            for index, file in enumerate(files):
                # Skip already processed frames
                if index < start_index:
                    continue
                
                # Check if paused
                while self.is_paused and self.is_running:
                    time.sleep(0.1)
                
                # Check if stopped
                if not self.is_running:
                    if on_progress:
                        on_progress("Face swap stopped")
                    self.progress_manager.save(
                        index, len(files), temp_input_face, 
                        input_video, input_type, processing_unit
                    )
                    return
                
                file_path = os.path.join("extracted_frames/", file)
                
                # Perform face swap
                self.api.swap_face(file, face_image, input_model, 
                                  file_path, processing_unit, source_choice)
                
                # Save progress after each frame
                self.progress_manager.save(
                    index + 1, len(files), temp_input_face,
                    input_video, input_type, processing_unit
                )
                
                # Calculate progress percentage
                progress_pct = ((index + 1) / len(files)) * 100
                
                # Callback for frame completion
                result_path = os.path.join("finished_frames/", file)
                if on_frame_complete:
                    on_frame_complete(index + 1, len(files), progress_pct, result_path)
            
            # Clear progress after successful completion
            self.progress_manager.clear()
            
            if on_complete:
                on_complete()
                
        except Exception as e:
            if on_error:
                on_error(str(e))
        finally:
            self.is_running = False
    
    def pause(self):
        """Pause processing"""
        if self.is_running:
            self.is_paused = True
    
    def resume(self):
        """Resume processing"""
        if self.is_paused:
            self.is_paused = False
    
    def stop(self):
        """Stop processing"""
        self.is_running = False
