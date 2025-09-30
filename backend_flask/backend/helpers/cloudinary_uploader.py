from werkzeug.datastructures import FileStorage

from flask import Flask

import cloudinary
import cloudinary.uploader

class CloudinaryUploader:
    """
    Configuring the external Cloudinary service for uploading images
    """

    @staticmethod
    def upload_file(file: FileStorage, folder: str) -> str:
        result = cloudinary.uploader.upload(file, folder=folder, resource_type='image')
        return result.get('secure_url')

    @staticmethod
    def init_cloudinary(app: Flask) -> None:
        cloudinary.config(
            cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=app.config['CLOUDINARY_API_KEY'],
            api_secret=app.config['CLOUDINARY_API_SECRET'],
        )

    @staticmethod
    def delete_file(file_url: str) -> None:
        public_id = file_url.split('/')[-1].split('.')[0]
        cloudinary.uploader.destroy(public_id)