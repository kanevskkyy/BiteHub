import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from flask import Flask, g, request
from flask_jwt_extended import get_jwt_identity

class Logger:
    """Logging configuration"""

    @staticmethod
    def setup_logger(app: Flask):
        log_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')
        os.makedirs(log_folder, exist_ok=True)
        log_file = os.path.join(log_folder, 'backend.log')

        logger = logging.getLogger('backend_logger')
        logger.setLevel(logging.INFO)

        file_handler = RotatingFileHandler(
            log_file, maxBytes=5*1024*1024, backupCount=5
        )
        file_formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        @app.before_request
        def log_request_info():
            g.start_time = datetime.utcnow()
            user = 'Anonymous'
            try:
                jwt_user = get_jwt_identity()
                if jwt_user:
                    user = jwt_user
            except Exception:
                pass

            logger.info(f'User: {user} | Request: {request.method} {request.path} | IP: {request.remote_addr}')

            if request.files:
                for file_name, file in request.files.items():
                    file.seek(0, 2)
                    size = file.tell()
                    file.seek(0)
                    logger.info(f'File uploaded: {file_name} | Filename: {file.filename} | Size: {size} bytes')

        @app.after_request
        def log_response_info(response):
            duration = (datetime.utcnow() - g.start_time).total_seconds()
            logger.info(f'Response: {request.method} {request.path} | Status: {response.status_code} | Duration: {duration:.3f}s')
            return response

        @app.errorhandler(Exception)
        def handle_exception(e):
            try:
                user = get_jwt_identity() or 'Anonymous'
            except Exception:
                user = 'Anonymous'

            logger.exception(f'Exception at {request.path} | User: {user} | Type: {type(e).__name__} | {str(e)}')
            return {'message': 'Internal server error'}, 500

        return logger