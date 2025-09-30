from functools import wraps
from flask import request, jsonify

ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'ico', 'svg'}
ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg', 'image/svg+xml', 'image/x-icon'}

def allowed_file(filename: str) -> bool:
    """
    Check if the filename has an allowed extension.

    Args:
        filename (str): Name of the file.

    Returns:
        bool: True if file has allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image_file(file_key: str = 'file', required: bool = False):
    """
    Decorator to validate uploaded image files in Flask requests.

    Args:
        file_key (str): Key of the file in request.files.
        required (bool): If True, the file must be provided.

    Returns:
        function: Wrapped function that validates the file before execution.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            file = request.files.get(file_key)

            if not file:
                if required:
                    return jsonify({'error': f'File "{file_key}" is required!'}), 400
                return func(*args, **kwargs)

            if file.filename == '':
                return jsonify({'error': 'File not chosen!'}), 400

            if not allowed_file(file.filename):
                return jsonify({'error': 'Unsupported file type! Allowed: png, jpeg, jpg, ico, svg'}), 400

            if file.mimetype not in ALLOWED_MIME_TYPES:
                return jsonify({'error': f'Unsupported MIME-type: {file.mimetype}'}), 400

            return func(*args, **kwargs)
        return wrapper
    return decorator