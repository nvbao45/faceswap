"""
Progress tracking and management
"""
import json
import os
import time


class ProgressManager:
    """Manage face swap progress for crash recovery"""
    
    def __init__(self, progress_file="progress.json"):
        self.progress_file = progress_file
    
    def save(self, current_index, total_files, input_face, input_video, input_type, processing_unit):
        """
        Save current progress to JSON file
        
        Args:
            current_index: Current frame index
            total_files: Total number of files
            input_face: Path to face image
            input_video: Path to video
            input_type: "Single Image" or "Face Model"
            processing_unit: "CPU" or "GPU (CUDA)"
        """
        progress_data = {
            "current_index": current_index,
            "total_files": total_files,
            "input_face": input_face,
            "input_video": input_video,
            "input_type": input_type,
            "processing_unit": processing_unit,
            "timestamp": time.time()
        }
        
        with open(self.progress_file, 'w') as f:
            json.dump(progress_data, f, indent=4)
    
    def load(self):
        """
        Load progress from JSON file
        
        Returns:
            Progress data dict or None if not found
        """
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def clear(self):
        """Clear progress file"""
        if os.path.exists(self.progress_file):
            os.remove(self.progress_file)
    
    def is_recent(self, progress_data, max_age_days=7):
        """
        Check if progress is recent
        
        Args:
            progress_data: Progress data dict
            max_age_days: Maximum age in days
            
        Returns:
            True if progress is recent, False otherwise
        """
        if not progress_data:
            return False
        
        timestamp = progress_data.get("timestamp", 0)
        max_age_seconds = max_age_days * 86400
        
        return (time.time() - timestamp) < max_age_seconds
