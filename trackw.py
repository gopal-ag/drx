import cv2
import imutils
import time

# Define the lower and upper boundaries of the "green" ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# Start video capture
vs = cv2.VideoCapture(0)
time.sleep(2.0)

while True:
    # Grab the current frame
    ret, frame = vs.read()

    if not ret:
        break

    # Resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Create a mask for the green color, then perform a series of dilations and erosions
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask and initialize the current (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # Only proceed if at least one contour was found
    if len(cnts) > 0:
        # Find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Only proceed if the radius meets a minimum size
        if radius > 10:
            # Draw the circle and centroid on the frame
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # Show the frame to our screen
    cv2.imshow("Frame", frame)

    # If the 'q' key is pressed, break from the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close any open windows
vs.release()
cv2.destroyAllWindows()
