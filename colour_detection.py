
import cv2
import numpy as np

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam not found!")
    exit()

while True:
    # Read webcam frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Cannot read webcam!")
        break

    # Flip camera image
    frame = cv2.flip(frame, 1)

    # Convert BGR image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define colour ranges
    colors = {
        "Red": [
            ([0, 100, 100], [10, 255, 255]),
            ([160, 100, 100], [179, 255, 255])
        ],
        "Green": [
            ([35, 80, 80], [85, 255, 255])
        ],
        "Blue": [
            ([90, 80, 80], [130, 255, 255])
        ],
        "Yellow": [
            ([20, 100, 100], [35, 255, 255])
        ]
    }

    detected_color = "No Color Detected"

    # Detect colours
    for color_name, ranges in colors.items():
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

        for lower, upper in ranges:
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)

            mask |= cv2.inRange(hsv, lower, upper)

        if cv2.countNonZero(mask) > 1000:
            detected_color = color_name
            break

    # Display detected colour
    cv2.putText(
        frame,
        "Color: " + detected_color,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    # Show webcam window
    cv2.imshow("Live Webcam Colour Detection", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release webcam
cap.release()
cv2.destroyAllWindows()
