import os
from flask import request, jsonify
from utils import UPLOAD_FOLDER
from scanner.service import IDCardScanner

def get_scan_id():
    # filepath = '/home/user/id-scanner/public/uploads/ith-sobeourn.png'
    # filepath = '/home/user/id-scanner/public/uploads/phay-thavirak.jpg'
    filepath = '/home/user/id-scanner/public/uploads/sith-traly.png'
    scanner = IDCardScanner()
    return scanner.scan_id_card(filepath)

def post_scan_id():
    print("scan_id")
    
    if 'id_card' not in request.files or request.files['id_card'].filename == '':
        return "No file part"

    file = request.files['id_card']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    if (filepath):
        scanner = IDCardScanner()
        return scanner.scan_id_card(filepath)

    return f"File uploaded successfully: {file.filename}"

