import cloudinary
import cloudinary.uploader
from flask import Flask


class CloudinaryUploader:
    @staticmethod
    def upload_file(file, folder: str) -> str:
        result = cloudinary.uploader.upload(file, folder=folder, resource_type='image')
        return result.get('secure_url')

    @staticmethod
    def init_cloudinary(app: Flask):
        cloudinary.config(
            cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=app.config['CLOUDINARY_API_KEY'],
            api_secret=app.config['CLOUDINARY_API_SECRET'],
        )