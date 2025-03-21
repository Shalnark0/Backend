from app.services.image_service import ImageService
from flask import send_file, jsonify
from app.utils.error_handler import NotFoundError

class ImageController:
    @staticmethod
    def get_image(image_id):
        try:
            image_path = ImageService.get_image_by_id(image_id)
            return send_file(image_path, mimetype='image/jpeg')
        except NotFoundError as e:
            return jsonify({"message": str(e)}), 404