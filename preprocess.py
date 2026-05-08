import cv2
import numpy as np
import os

def preprocess_plate(image_path, debug_output=False):
    """
    Full preprocessing pipeline for license plate images before OCR.

    Steps:
        1. Upscale small images for better OCR accuracy
        2. Edge detection + contour finding to locate the plate
        3. Perspective correction (deskew) if a rectangular contour is found
        4. CLAHE - contrast enhancement for uneven lighting
        5. Gaussian blur - noise reduction
        6. Unsharp mask - sharpening character edges

    Args:
        image_path (str): Path to the input image
        debug_output (bool): If True, saves intermediate images to output/

    Returns:
        str: Path to the preprocessed image ready for OCR
    """

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")

    # --- Step 1: Upscale small images ---
    # OCR accuracy degrades on images narrower than ~600px
    h, w = img.shape[:2]
    if w < 600:
        scale = 600 / w
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

    # --- Step 2: Convert to grayscale + detect edges ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    if debug_output:
        os.makedirs("output", exist_ok=True)
        cv2.imwrite("output/edges.jpg", edges)

    # --- Step 3: Perspective correction (deskew) ---
    # Find the largest 4-sided contour, assume it's the plate rectangle
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    plate_contour = None
    for c in contours[:10]:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            plate_contour = approx
            break

    if plate_contour is not None:
        pts = plate_contour.reshape(4, 2).astype(np.float32)
        rect = order_points(pts)
        (tl, tr, br, bl) = rect

        maxW = max(int(np.linalg.norm(br - bl)), int(np.linalg.norm(tr - tl)))
        maxH = max(int(np.linalg.norm(tr - br)), int(np.linalg.norm(tl - bl)))

        if maxW > 0 and maxH > 0:
            dst = np.array([[0, 0], [maxW-1, 0], [maxW-1, maxH-1], [0, maxH-1]], dtype=np.float32)
            M = cv2.getPerspectiveTransform(rect, dst)
            img = cv2.warpPerspective(img, M, (maxW, maxH))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- Step 4: CLAHE (Contrast Limited Adaptive Histogram Equalization) ---
    # Enhances local contrast so characters are visible even in poor lighting
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    if debug_output:
        cv2.imwrite("output/gray.jpg", gray)

    # --- Step 5: Gaussian blur (denoise) ---
    # Smooths out grain/noise before sharpening
    denoised = cv2.GaussianBlur(gray, (3, 3), 0)

    if debug_output:
        cv2.imwrite("output/blur.jpg", denoised)

    # --- Step 6: Unsharp mask (sharpen) ---
    # Increases edge contrast so character boundaries are crisp for OCR
    sharp = cv2.addWeighted(gray, 1.5, denoised, -0.5, 0)

    # Save final preprocessed image for OCR
    os.makedirs("output", exist_ok=True)
    out_path = "output/ocr_input.jpg"
    cv2.imwrite(out_path, sharp)

    return out_path


def order_points(pts):
    """
    Order 4 corner points as: top-left, top-right, bottom-right, bottom-left.
    Used for perspective transform matrix calculation.
    """
    rect = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]    # top-left: smallest x+y sum
    rect[2] = pts[np.argmax(s)]    # bottom-right: largest x+y sum
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)] # top-right: smallest y-x diff
    rect[3] = pts[np.argmax(diff)] # bottom-left: largest y-x diff
    return rect