"""
API Handler for Automatic1111 Reactor face swap
"""
import requests
import base64
import os


class Automatic1111API:
    """Handler for Automatic1111 Reactor API"""
    
    def __init__(self, url="http://127.0.0.1:7860"):
        self.url = url
    
    def swap_face(self, file, face_image, input_model, input_image, processing_unit, source_choice):
        """
        Perform face swap using Reactor API
        
        Args:
            file: Output filename
            face_image: Path to face image
            input_model: Face model path
            input_image: Input image path
            processing_unit: "CPU" or "GPU (CUDA)"
            source_choice: 0 for single image, 1 for face model
        """
        if processing_unit == "GPU (CUDA)":
            device_choice = "CUDA"
        else:
            device_choice = "CPU"

        # Open the image file in binary mode
        with open(input_image, "rb") as image_file:
            image_binary = image_file.read()

        base64_image = base64.b64encode(image_binary).decode('utf-8')

        if face_image != "":
            with open(face_image, "rb") as image_file:
                image_binary_face = image_file.read()
            base64_image_face = base64.b64encode(image_binary_face).decode('utf-8')
        else:
            base64_image_face = face_image

        current_directory = os.getcwd()
        path = os.path.join(current_directory, "finished_frames/")
        result_path = os.path.join(path, file)

        payload = {
            "face_model": input_model,
            "source_image": base64_image_face,
            "target_image": base64_image,
            "source_faces_index": [0],
            "face_index": [0],
            "upscaler": "None",
            "scale": 1,
            "upscale_visibility": 1,
            "face_restorer": "CodeFormer",
            "restorer_visibility": 1,
            "codeformer_weight": 0.5,
            "restore_first": 1,
            "model": "inswapper_128.onnx",
            "gender_source": 0,
            "gender_target": 0,
            "save_to_file": 1,
            "result_file_path": result_path,
            "device": device_choice,
            "select_source": source_choice,
        }

        response = requests.post(url=f'{self.url}/reactor/image', json=payload)
        return response
