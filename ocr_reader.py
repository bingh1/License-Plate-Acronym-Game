import cv2
import easyocr
import re

reader = easyocr.Reader(['en'])


def read_plate_text(plate_image):
    gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)

    threshold = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    results = reader.readtext(threshold)

    if len(results) == 0:
        return ""

    text = results[0][1]

    cleaned = re.sub(r'[^A-Z0-9]', '', text.upper())

    return cleaned