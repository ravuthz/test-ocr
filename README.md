# Test OCR

Configure path of "tesseract" in "src/scanner/service.py"

```bash

pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
```

Make sure you have python

```bash
python -V
pip list
```

Install dependecies

```bash
pip install poetry
poetry install
```

Start app with port 9000

```bash
python -m flask --app src/main run -p 9000 --debug
```

http://localhost:9000
