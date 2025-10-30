"""
Face Swap Tool - Main Entry Point
Modern GUI application for face swapping with pause/resume and crash recovery
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui.main_window import FaceSwapApp


def main():
    """Main entry point"""
    app = FaceSwapApp()
    app.run()


if __name__ == "__main__":
    main()
