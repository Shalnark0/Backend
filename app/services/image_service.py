import os
from app.utils.error_handler import Error, NotFoundError

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')

class ImageService:
    @staticmethod
    def get_image_by_id(image_id):
        image_path = os.path.join(UPLOAD_FOLDER, f"{image_id}.jpg")
        if not os.path.exists(image_path):
            raise NotFoundError("Image not found")
        return image_path