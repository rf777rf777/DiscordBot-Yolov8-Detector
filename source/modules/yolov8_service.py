from PIL import Image
import io
import requests
from configs.config import Config

class yolov8_service:
    def __init__(self):
        pass
    
    def detect_object(self, image: Image, filename: str) -> io.BytesIO: 
        new_stream = self.__resizeAndGetImageStream(image=image)
        #Post to detect api
        files = {'file': (filename, new_stream, 'multipart/form-data')}
        config = Config.get_config()     
        response = requests.put(config['DetectAPI']['Url'], files=files) 
        if response.status_code != 200:
            print(response.status_code)
            return None
        
        detected_stream = io.BytesIO(response.content)
        detected_stream.seek(0)
        return detected_stream
             
    def __resizeAndGetImageStream(self, image: Image) -> io.BytesIO:
        output = io.BytesIO()
        while True:
            output.seek(0)
            image.save(output, format='JPEG')

            file_size = output.tell()  # `tell()` return stream size
            print(file_size)
            if file_size <= 200 * 1024:  # stream size <= 200KB stop compression
                break
            else:
                #resize image
                width, height = image.size
                new_size = (int(width * 0.8), int(height * 0.8))  #80%
                image = image.resize(new_size, Image.Resampling.LANCZOS) 
        output.seek(0)
        return output         