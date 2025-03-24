from google.cloud import vision
from google.cloud.vision import types
import io

def detect_text_from_image(image_path):
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    # Load the image into memory
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Create an image instance for the Vision API
    image = types.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Check if any text was detected
    if texts:
        print("Text found in image:")
        print(texts[0].description)  # The first entry contains the full text
    else:
        print("No text found in the image.")

# Replace this with the path to your ID card image
# image_path = 'path_to_your_id_card_image.jpg'
# detect_text_from_image(image_path)
