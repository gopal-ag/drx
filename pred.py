import cv2
import imutils
import numpy as np
import time
from collections import deque

# Define the lower and upper boundaries of the "green" ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# Video input and output
input_video_path = 'ball_throw.mp4'  # Path to the uploaded video file
output_video_path = 'output_video.mp4'  # Path for the output video file

# Start video capture
vs = cv2.VideoCapture(input_video_path)

# Get video properties
fps = int(vs.get(cv2.CAP_PROP_FPS))
width = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Initialize previous center and time
prev_center = None
prev_time = None
velocity_threshold = 5  # Threshold for significant movement
positions = deque(maxlen=10)  # Store the last 10 positions of the ball

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
    velocity = 0

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

            # Calculate the velocity
            if prev_center is not None and prev_time is not None:
                dx = center[0] - prev_center[0]
                dy = center[1] - prev_center[1]
                dt = time.time() - prev_time
                distance = (dx**2 + dy**2)**0.5
                if distance > velocity_threshold:
                    velocity = distance / dt
                else:
                    velocity = 0

            # Update the previous center and time
            prev_center = center
            prev_time = time.time()

            # Append the current center to the positions deque
            positions.appendleft(center)

    # Display the velocity on the frame
    cv2.putText(frame, f"Velocity: {velocity:.2f} px/s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Predict the trajectory using linear regression if there are enough points
    if len(positions) >= 2:
        # Prepare data for linear regression
        x_positions = np.array([p[0] for p in positions]).reshape(-1, 1)
        y_positions = np.array([p[1] for p in positions]).reshape(-1, 1)

        # Fit linear model for x and y positions
        if len(x_positions) > 1:
            x_model = np.polyfit(range(len(x_positions)), x_positions.flatten(), 1)
            y_model = np.polyfit(range(len(y_positions)), y_positions.flatten(), 1)

            # Predict future positions
            future_steps = 30  # Number of future steps to predict
            for i in range(1, future_steps):
                future_x = np.polyval(x_model, len(x_positions) + i)
                future_y = np.polyval(y_model, len(y_positions) + i)
                cv2.circle(frame, (int(future_x), int(future_y)), 2, (255, 0, 255), -1)

    # Write the frame to the output video
    out.write(frame)

# Release the camera and close any open windows
vs.release()
out.release()
cv2.destroyAllWindows()

output_video_path
