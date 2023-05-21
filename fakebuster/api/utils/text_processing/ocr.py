import pytesseract
from PIL import Image


def get_text_from_img(img : str) -> str | None:
    try:
        image = Image.open(img)
    except AttributeError as err:
        return None
    else:
        text = pytesseract.image_to_string(image, lang="pol")
        return text