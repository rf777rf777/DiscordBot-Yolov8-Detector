from PIL import Image, ImageDraw, ImageFont
import io
import requests
from configs.config import Config

class yolov8_service:
    def __init__(self):
        pass
    
    def detect_object_info(self, image: Image, filename: str) -> io.BytesIO:
        new_stream = self.__resizeAndGetImageStream(image=image)
        
        #Post to detect api
        files = {'file': (filename, new_stream, 'multipart/form-data')}
        response = requests.put('http://45.130.166.218:8000/Detection/Image/Info', files=files) 
        #print(response.json())
        
        image = Image.open(new_stream)
        draw = ImageDraw.Draw(image)
       
        for detection in response.json()['detections']:
            
            #draw frame
            x, y, w, h = detection['box'][0]
            top_left = (x - w / 2, y - h / 2)
            bottom_right = (x + w / 2, y + h / 2)
            draw.rectangle([top_left, bottom_right], outline="red", width=5)
            
            className = detection['className']
            confidence = round(detection['confidence'], 2)
            font = ImageFont.load_default() 
            
            label_text = f"{className} {confidence}"

            bbox = draw.textbbox((0, 0), label_text, font=font, font_size=16)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            #text is on the top of frame
            label_position = (top_left[0], top_left[1] - text_height - 5)  
            
            #draw label
            draw.rectangle([label_position, (label_position[0] + text_width, label_position[1] + text_height)], fill="black")
            draw.text(label_position, label_text, fill="white", font=font)
            
        output = io.BytesIO()
        image.save(output, format="JPEG")
        output.seek(0)  
        return output
 
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