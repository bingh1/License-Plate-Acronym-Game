import cv2

from preprocess import preprocess_image
from detect_plate import detect_plate
from ocr_reader import read_plate_text
from acronym_generator import generate_acronym


IMAGE_PATH = 'images/test1.jpg'


# Preprocess image
image, gray, blur, edges = preprocess_image(IMAGE_PATH)


# Detect plate
plate = detect_plate(image, edges)


if plate is None:
    print('No plate detected.')
    exit()


# Draw contour
cv2.drawContours(image, [plate], -1, (0, 255, 0), 3)


# Crop plate
x, y, w, h = cv2.boundingRect(plate)
plate_image = image[y:y+h, x:x+w]


# Save cropped plate
cv2.imwrite('output/detected_plate.jpg', plate_image)


# OCR
plate_text = read_plate_text(plate_image)


# Extract letters only
letters = ''.join(filter(str.isalpha, plate_text))


# Generate acronym
acronym = generate_acronym(letters)


# Print results
print('\n===== RESULTS =====')
print('Detected Plate:', plate_text)
print('Letters:', letters)
print('Generated Acronym:', acronym)


# Display images
cv2.imshow('Original', image)
cv2.imshow('Edges', edges)
cv2.imshow('Detected Plate', plate_image)

cv2.waitKey(0)
cv2.destroyAllWindows()