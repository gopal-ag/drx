import cv2
import numpy as np
from orange_detector import OrangeDetector
from kalmanfilter import KalmanFilter

input_video = "gopu.avi"
cap = cv2.VideoCapture(input_video)


od = OrangeDetector()
kf = KalmanFilter()


actual_positions = []
predicted_positions = []

while True:
  ret, frame = cap.read()
  if not ret:
    break


  orange_bbox = od.detect(frame)
  x, y, x2, y2 = orange_bbox
  cx = int((x + x2) / 2)
  cy = int((y + y2) / 2)


  actual_positions.append((cx, cy))


  predicted = kf.predict(cx, cy)
  predicted_positions.append(predicted)


  cv2.circle(frame, (cx, cy), 20, (0, 0, 255), 4)  # Detected position
  cv2.circle(frame, (predicted[0], predicted[1]), 20, (255, 0, 0), 4)  # Predicted position

  # Draw the actual path (blue line)
  for i in range(1, len(actual_positions)):
    cv2.line(frame, actual_positions[i - 1], actual_positions[i], (255, 0, 0), 2)

  # Draw the predicted path (red line)
  for i in range(1, len(predicted_positions)):
    cv2.line(frame, predicted_positions[i - 1], predicted_positions[i], (0, 0, 255), 2)

  # Show the frame with detections and paths
  cv2.imshow("Orange Detection", frame)

  # Exit on 'q' key press
  if cv2.waitKey(1) == ord('q'):
    break

# Release resources
cap.release()
cv2.destroyAllWindows()
