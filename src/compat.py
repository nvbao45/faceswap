"""
Compatibility wrapper for legacy code
Provides the old function interface while using new modular code
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.api_handler import Automatic1111API
from core.video_processor import VideoProcessor

# Create global instances for compatibility
_api = Automatic1111API()
_video = VideoProcessor()


def api_change_face(file, face_image, input_model, input_image, processing_unit, source_choice):
    """Legacy API wrapper"""
    return _api.swap_face(file, face_image, input_model, input_image, processing_unit, source_choice)


def get_frames(path):
    """Legacy frame extraction wrapper"""
    return _video.extract_frames(path)


def create_video(folder_path):
    """Legacy video creation wrapper"""
    return _video.create_video_from_frames(folder_path)


def add_sound(video_sound_path, video_no_sound_path):
    """Legacy audio addition wrapper"""
    return _video.add_audio(video_sound_path, video_no_sound_path)
