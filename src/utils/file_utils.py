"""
File Utilities
Helper functions for file and directory operations
"""
import os
import re
from datetime import datetime
from typing import List, Optional


def ensure_directory(path: str) -> None:
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        path: Directory path to ensure exists
    """
    if not os.path.exists(path):
        os.makedirs(path)


def list_files(directory: str, extension: Optional[str] = None) -> List[str]:
    """
    List files in a directory with optional extension filter
    
    Args:
        directory: Directory to list files from
        extension: File extension to filter (e.g., '.jpg', '.mp4')
    
    Returns:
        List of file paths
    """
    if not os.path.exists(directory):
        return []
    
    files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            if extension is None or file.lower().endswith(extension.lower()):
                files.append(file_path)
    
    return sorted(files)


def list_image_files(directory: str) -> List[str]:
    """
    List image files in a directory
    
    Args:
        directory: Directory to list images from
    
    Returns:
        List of image file paths
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
    
    if not os.path.exists(directory):
        return []
    
    files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            if ext.lower() in image_extensions:
                files.append(file_path)
    
    return sorted(files)


def list_video_files(directory: str) -> List[str]:
    """
    List video files in a directory
    
    Args:
        directory: Directory to list videos from
    
    Returns:
        List of video file paths
    """
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    
    if not os.path.exists(directory):
        return []
    
    files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            if ext.lower() in video_extensions:
                files.append(file_path)
    
    return sorted(files)


def clear_directory(directory: str, pattern: Optional[str] = None) -> int:
    """
    Clear files in a directory with optional pattern matching
    
    Args:
        directory: Directory to clear
        pattern: Optional regex pattern to match files
    
    Returns:
        Number of files deleted
    """
    if not os.path.exists(directory):
        return 0
    
    count = 0
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            if pattern is None or re.match(pattern, file):
                try:
                    os.remove(file_path)
                    count += 1
                except Exception:
                    pass
    
    return count


def get_filename_without_ext(path: str) -> str:
    """
    Get filename without extension
    
    Args:
        path: File path
    
    Returns:
        Filename without extension
    """
    basename = os.path.basename(path)
    name, _ = os.path.splitext(basename)
    return name


def get_file_size(path: str) -> int:
    """
    Get file size in bytes
    
    Args:
        path: File path
    
    Returns:
        File size in bytes, or 0 if file doesn't exist
    """
    if os.path.exists(path):
        return os.path.getsize(path)
    return 0


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def generate_timestamp_filename(prefix: str = "", extension: str = "") -> str:
    """
    Generate a filename with timestamp
    
    Args:
        prefix: Filename prefix
        extension: File extension (with or without dot)
    
    Returns:
        Filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if extension and not extension.startswith('.'):
        extension = f".{extension}"
    
    if prefix:
        return f"{prefix}_{timestamp}{extension}"
    else:
        return f"{timestamp}{extension}"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    
    return sanitized


def count_files(directory: str, extension: Optional[str] = None) -> int:
    """
    Count files in a directory with optional extension filter
    
    Args:
        directory: Directory to count files in
        extension: File extension to filter (e.g., '.jpg')
    
    Returns:
        Number of files
    """
    return len(list_files(directory, extension))


def get_latest_file(directory: str, extension: Optional[str] = None) -> Optional[str]:
    """
    Get the most recently modified file in a directory
    
    Args:
        directory: Directory to search
        extension: File extension to filter
    
    Returns:
        Path to latest file, or None if no files found
    """
    files = list_files(directory, extension)
    if not files:
        return None
    
    latest_file = max(files, key=os.path.getmtime)
    return latest_file
