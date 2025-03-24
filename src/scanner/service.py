import cv2
import pytesseract
import os
import re
import json
from utils import logger, JSON_FOLDER
from datetime import datetime
from flask import jsonify

log = logger()

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

class IDCardScanner:
        
    def preprocess_image(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        # _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        # _, threshold = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        threshold = cv2.medianBlur(threshold, 3)

        # Noise removal
        denoised = cv2.fastNlMeansDenoising(threshold)
        
        return denoised

    def extract_text(self, image, lang):
        # Extract text using tesseract
        text = pytesseract.image_to_string(image, lang)
        return text

    def parse_kh_info(self, text):
        # Find all text with colons and split into key-value pairs
        matches = re.findall(r'([^:\n]+):\s*([^\n]+)', text)

        # Convert to a structured list
        structured_data = [{"key": key.strip(), "value": value.strip()} for key, value in matches]

        # Convert to JSON format
        # return json.dumps(structured_data, indent=4, ensure_ascii=False)
        return structured_data

    def write_to_json(self, json_content, json_filename):
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(json_content, json_file, indent=4, ensure_ascii=False)


    def parse_id_info(self, text):
        print(text)
        info = {
            'dob': None,
            'name': None,
            'address': None,
            'id_number': None
        }

        # Extract ID number (assuming format: 9 digits)
        id_match = re.search(r'\b\d{9}\b', text)
        if id_match:
            info['id_number'] = id_match.group()
            
        # Extract name (assuming format: uppercase letters)
        name_match = re.search(r'([A-Z]+\s+[A-Z]+)', text)
        if name_match:
            info['name'] = name_match.group()
            
        # Extract date of birth (assuming format: DD/MM/YYYY)
        dob_match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', text)
        if dob_match:
            info['dob'] = dob_match.group()
            
        # Extract address (assuming it's after "Address:" or similar)
        addr_match = re.search(r'(?:Address|ADD)[:]\s*(.*?)(?:\n|$)', text, re.IGNORECASE)
        if addr_match:
            info['address'] = addr_match.group(1).strip()
            
        return info

    def scan_id_card(self, image_path):
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise Exception("Could not read image")
            
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Extract text
            # text_en = self.extract_text(processed_image, "eng")
            # text_kh = self.extract_text(processed_image, "khm")
            text = self.extract_text(processed_image, "khm+eng")
            
            # Parse information
            result_en = self.parse_id_info(text)
            self.write_to_json(text, os.path.join(JSON_FOLDER, "id_card_en.json"))

            result_kh = self.parse_kh_info(text)
            self.write_to_json(text, os.path.join(JSON_FOLDER, "id_card_kh.json"))

            return {
                "result_en": result_en, 
                "result_kh": result_kh,
                "text": text
            }
        except Exception as e:
            print(f"Error scanning ID card: {str(e)}")
            return None


# oe 34323458(7)
# SAIRMUSASIV: [fu iot
# 
# SREY POV
# Igfogifontin: OM.og.98ée s58:5f5 Ann: obs HIE
# Saighionin: eMNATANSS eANgnoMnA qin
# IRS: GMM Rime 89.
# 
# | suINtiianngs anngnimn & aing
# 
# AIAITSNN: 0G.06.V09E Nig OM.od.N0WE
# $8518: (DIANE. 0,cni.6 thoiuaigh
# 
# IDKHM343234587 <<<<<<<<<ccceec<<§<
# 9008032M2601250KHM<<<<<<<<<<<6
# SREY <<POV<<<<KcKKceceedccc§eccc<
# 


# គិរី 34323458 (7)
# គោត្តគាមនឹងនាម: ស្រ ពៅ
# 
# ព 00ម
# 
# ថ្ងៃខែឆ្នាំកំណើត: ០៣.០៨.១៩៩៩ ទេទៈស្រី កំពស់: ១៦៩ ស.ម
# ទីកន្លែងកំណើត: សង្កាត់បឹងកត់ទី១ ខណ្ឌទួលគោក ភ្នំពេញ
# អាសឃដ្ឋូនៈ ផ្ទូះ៣៣ ផ្លូវ៣៥៥ ភូមិ១
# 
# សង្កាត់បឹងកក់ទី១ ខណ្ឌទួលគោក ភ្នំ ភ្នំពេញ
# 
# សុពលទាពៈ ០៤.០៨.២០១៥ ដល់ថ្ងៃ ០៣.០៩.២០២៥
# តឺនតាគ: ប្រជ្រុយចំ. 0,៥ស.ម លើចិញ្ចើមខាងឆ្វេង
# 
# 0|៧ស3432 34587<<<<<<<<<<<<<<<<
# ទ១008032|2601 2១0«៥២<<<<<<<<<<<4«
# $ក៣៩"<<00,<<<<<<<<<<<<<<<<<<<<<