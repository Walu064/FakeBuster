import pytesseract
from PIL import Image


def get_text_from_img(img : str) -> str:
    image = Image.open(img)
    text = pytesseract.image_to_string(image, lang="pol")
    return text