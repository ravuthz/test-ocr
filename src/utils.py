import logging

def setup_logging():
    logging.basicConfig(
        filename='app.log',  # Log file name
        level=logging.DEBUG,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
    )

def logger():
    setup_logging()
    return logging.getLogger(__name__)

UPLOAD_FOLDER="public/uploads"

JSON_FOLDER="public/json"