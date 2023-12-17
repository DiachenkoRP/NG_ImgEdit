import os
from PIL import Image, ImageOps

UPLOAD_FOLDER = "/home/diachenkorp/Desktop/Git/NG_ImgEdit/frontend/static/uploaded_images"
EDITED_FOLDER = "/home/diachenkorp/Desktop/Git/NG_ImgEdit/frontend/static/edited_images"
image_name = os.listdir(UPLOAD_FOLDER)[0]