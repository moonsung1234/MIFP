
from PIL import Image
import numpy as np
import json
import os

class FileManager :
    def __init__(self) :
        self.img_extensions = [
            "BMP", "RLE", "DIB", "JPEG", "JPG", "GIF", "PNG", "TIF", "TIFF", "JFIF",
            "bmp", "rle", "dib", "jpeg", "jpg", "gif", "png", "tif", "tiff", "jfif"
        ]

    def get_data(self, file_name) :
        if "." not in file_name :
            return None

        file_info = file_name.split(".")

        if file_info[1] in self.img_extensions :
            img = Image.open(file_name)
            img = np.array(img)

            return json.dumps(img.tolist())

        else :
            file = open(file_name, "r", encoding="utf-8")
            data = ""

            while True :
                line = file.readline()

                if not line :
                    break

                data += line

            return data

    def set_data(self, file_name, data) :
        if "." not in file_name :
            return None

        file_info = file_name.split(".")

        if file_info[1] in self.img_extensions :
            img = Image.fromarray(data)
            img.save(file_name)

        else :
            file = open(file_name, "w", encoding="utf-8")
            file.write(data)
    
    def get_info(self, file_name) :
        file_info = file_name.split(".")
        file_data = self.get_data(file_name)

        return {
            "file_extension" : file_info[1],
            "file_size" : os.path.getsize(file_name),
            "file_name" : file_info[0],
            "file_data" : file_data
        }