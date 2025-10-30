"""
Video processing utilities
"""
import cv2
import os
import datetime
import re
from moviepy.editor import VideoFileClip


class VideoProcessor:
    """Handle video frame extraction and merging"""
    
    @staticmethod
    def extract_frames(video_path, output_folder="extracted_frames"):
        """
        Extract frames from video
        
        Args:
            video_path: Path to input video
            output_folder: Folder to save extracted frames
            
        Returns:
            Number of frames extracted
        """
        vidcap = cv2.VideoCapture(video_path)
        success, image = vidcap.read()
        count = 0
        success = True
        
        while success:
            success, image = vidcap.read()
            if success:
                count += 1
                frame_path = f"{output_folder}/frame{count}.png"
                cv2.imwrite(frame_path, image)
        
        return count
    
    @staticmethod
    def _set_image_names(folder_path):
        """Rename images to consistent format"""
        for filename in os.listdir(folder_path):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                pattern = re.compile(r'(frame\d+)')
                match = pattern.search(filename)
                
                if match:
                    new_name = match.group(1)
                    new_path = os.path.join(folder_path, new_name + ".jpg")
                    old_path = os.path.join(folder_path, filename)
                    os.rename(old_path, new_path)
    
    @staticmethod
    def _extract_frame_number(filename):
        """Extract frame number from filename"""
        return int(filename.lstrip("frame").rstrip(".jpg"))
    
    @staticmethod
    def create_video_from_frames(frames_folder, output_folder="finished_videos", fps=30):
        """
        Create video from frames
        
        Args:
            frames_folder: Folder containing frames
            output_folder: Folder to save output video
            fps: Frames per second
            
        Returns:
            Path to created video
        """
        VideoProcessor._set_image_names(frames_folder)
        
        images = [img for img in os.listdir(frames_folder) if img.endswith(".jpg")]
        images = sorted(images, key=VideoProcessor._extract_frame_number)
        
        if not images:
            raise ValueError("No frames found in folder")
        
        frame = cv2.imread(os.path.join(frames_folder, images[0]))
        height, width, layers = frame.shape
        
        current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        video_name = f'{output_folder}/output_video_{current_datetime}.mp4'
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_name, fourcc, fps, (width, height))
        
        for image in images:
            img_path = os.path.join(frames_folder, image)
            frame = cv2.imread(img_path)
            out.write(frame)
        
        out.release()
        cv2.destroyAllWindows()
        
        return video_name
    
    @staticmethod
    def add_audio(source_video_path, target_video_path, output_folder="finished_videos"):
        """
        Add audio from source video to target video
        
        Args:
            source_video_path: Video with audio
            target_video_path: Video without audio
            output_folder: Folder to save final video
            
        Returns:
            Path to final video
        """
        video_with_sound = VideoFileClip(source_video_path)
        video_without_sound = VideoFileClip(target_video_path)
        
        video_without_sound = video_without_sound.set_audio(video_with_sound.audio)
        
        current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = f"{output_folder}/final_{current_datetime}.mp4"
        
        video_without_sound.write_videofile(output_path, codec='libx264')
        
        # Clean up temporary video
        if os.path.exists(target_video_path):
            os.remove(target_video_path)
        
        return output_path
