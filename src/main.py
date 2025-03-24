import os
import logging

from flask import Flask, send_file, jsonify, make_response
from scanner.controller import get_scan_id, post_scan_id
# from google.service import detect_text_from_image
from utils import setup_logging, UPLOAD_FOLDER, JSON_FOLDER

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

setup_logging()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(JSON_FOLDER):
    os.makedirs(JSON_FOLDER)

@app.route("/")
def index():
    app.logger.info("Home route accessed")
    return send_file('index.html')

@app.route("/test")
def test_id():
    data = get_scan_id()
    response = make_response(jsonify(data))
    response.headers['Accept'] = 'application/json;charset=utf-8'
    response.headers['Content-Type'] = 'application/json;charset=utf-8'
    return response

@app.route("/scan-id", methods=['POST'])
def scan_id():
    data = post_scan_id()
    response = make_response(jsonify(data))
    response.headers['Accept'] = 'application/json;charset=utf-8'
    response.headers['Content-Type'] = 'application/json;charset=utf-8'
    return response

# @app.route("/test")
# def test():
#     return detect_text_from_image(os.path.join(UPLOAD_FOLDER, "img_KHidcard.png"))

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
