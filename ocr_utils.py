import cv2
import pytesseract
from google.cloud import vision
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this path

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray

def extract_text_tesseract(image):
    return pytesseract.image_to_string(image)

def extract_text_google_vision(image):
    client = vision.ImageAnnotatorClient()
    success, encoded_image = cv2.imencode('.jpg', image)
    content = encoded_image.tobytes()
    image_vision = vision.Image(content=content)
    response = client.text_detection(image=image_vision)
    texts = response.text_annotations
    return texts[0].description if texts else ""
