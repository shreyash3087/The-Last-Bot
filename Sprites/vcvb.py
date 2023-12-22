import cv2
import numpy as np

def detect_cracks(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Perform morphological operations (dilation and erosion)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(edges, kernel, iterations=3)
    eroded = cv2.erode(dilated, kernel, iterations=2)

    # Find contours in the eroded image
    contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and aspect ratio
    min_area = 100  # Minimum contour area to consider
    min_aspect_ratio = 0.2  # Minimum aspect ratio to consider
    detected_cracks = []
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)

        if area > min_area and aspect_ratio > min_aspect_ratio:
            detected_cracks.append(contour)

    # Draw contours on the original image
    cv2.drawContours(image, detected_cracks, -1, (0, 255, 0), 2)

    # Display the result
    cv2.imshow("Crack Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Path to the image file
image_path = "C:/Users/shrey/OneDrive/Desktop/Temp/Image.jpg"

# Call the crack detection function
detect_cracks(image_path)
