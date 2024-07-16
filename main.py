import cv2
import numpy as np

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Allow the camera to warm up
import time
time.sleep(2)

# Capture a frame to get the size of the video
ret, frame = cap.read()
if not ret:
    print("Failed to capture initial frame")
    cap.release()
    exit()

# Load the background image
background = cv2.imread('background.jpg')

# Resize the background image to match the video frame size
background = cv2.resize(background, (frame.shape[1], frame.shape[0]))

# Define the color range for the cloak (e.g., green)
#lower_green = np.array([40, 100, 100])
#upper_green = np.array([80, 255, 255])
# Define the color range for the cloak (e.g., red)
# Red can span two ranges in the HSV color space
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the cloak
   # mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)


    # Invert the mask to get the non-cloak areas
    mask_inv = cv2.bitwise_not(mask)

    # Ensure the mask and images are in the same data type
    mask = mask.astype(np.uint8)
    mask_inv = mask_inv.astype(np.uint8)
    background = background.astype(np.uint8)
    frame = frame.astype(np.uint8)

    # Extract the cloak area from the frame
    cloak_area = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Extract the background area
    background_area = cv2.bitwise_and(background, background, mask=mask)

    # Combine the two images
    result = cv2.add(cloak_area, background_area)

    # Show the result
    cv2.imshow('Invisibility Cloak', result)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()