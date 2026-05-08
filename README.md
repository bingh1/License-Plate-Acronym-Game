# Plating Acronyms

A Colorado-themed license plate acronym generator for the console. Take a photo of any Colorado license plate, and the program will read the letters using OCR and generate 5 creative acronyms using Colorado-flavored words — mountains, ski resorts, craft beer, wildlife, and more.

Built as a final project for Image Processing and Computing.

---

## Features

- Reads license plate letters directly from a photo using EasyOCR
- Accepts manual letter input if you don't have an image
- Generates 5 unique Colorado-themed acronyms per run
- Filters out plate text like "COLORFUL COLORADO" so only the actual plate letters are used
- Works fully offline — no API key required

---

## Requirements

- Python 3.7+
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)

Install the dependency:

```bash
pip install easyocr
```

---

## Usage

**From an image:**
```bash
python plate.py images/test1.jpg
```

**From letters directly:**
```bash
python plate.py BABY
```

**Example output:**
```
Reading plate from image...
Detected letters: RVP

 Colorado Plate: R-V-P

  1. Roaring Vista Powder
  2. Rockies Vail Peak
  3. Rugged Vibrant Pristine
  4. Ridge Vertical Ponderosa
  5. Ripping Vail Powder
```

---

## How it works

1. EasyOCR scans the image and detects all text regions
2. Common plate labels like "COLORADO" and "COLORFUL" are filtered out
3. The remaining characters are stripped down to letters only
4. For each letter, the program picks a Colorado-themed word from a curated word list, falling back to a general English dictionary if needed
5. Five unique acronyms are generated and printed with the key letters highlighted in green

---

## Notes

- The first time you run it with an image, EasyOCR will download its English model (~100MB). This only happens once.
- Works best with clear, straight-on photos of the plate
- If OCR struggles with a photo, you can always type the letters manually as a fallback
