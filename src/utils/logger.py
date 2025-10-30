"""
Logging Utilities
Simple logging helpers for the application
"""
import logging
import os
from datetime import datetime
from typing import Optional


class AppLogger:
    """Application logger with file and console output"""
    
    def __init__(self, name: str = "FaceSwapTool", log_dir: Optional[str] = None):
        """
        Initialize logger
        
        Args:
            name: Logger name
            log_dir: Directory for log files (optional)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Avoid adding handlers multiple times
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
            # File handler (if log_dir provided)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
                log_file = os.path.join(
                    log_dir,
                    f"face_swap_{datetime.now().strftime('%Y%m%d')}.log"
                )
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(logging.DEBUG)
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)


# Global logger instance
_global_logger: Optional[AppLogger] = None


def get_logger(name: str = "FaceSwapTool", log_dir: Optional[str] = None) -> AppLogger:
    """
    Get or create global logger instance
    
    Args:
        name: Logger name
        log_dir: Directory for log files
    
    Returns:
        AppLogger instance
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = AppLogger(name, log_dir)
    return _global_logger


def log_debug(message: str):
    """Quick debug log"""
    get_logger().debug(message)


def log_info(message: str):
    """Quick info log"""
    get_logger().info(message)


def log_warning(message: str):
    """Quick warning log"""
    get_logger().warning(message)


def log_error(message: str):
    """Quick error log"""
    get_logger().error(message)


def log_critical(message: str):
    """Quick critical log"""
    get_logger().critical(message)
