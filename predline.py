import cv2
import numpy as np
from green_detector import OrangeDetector
from kalmanfilter import KalmanFilter


cap = cv2.VideoCapture(0)

od = OrangeDetector()
kf = KalmanFilter()

actual_positions = []
predicted_positions = []
timestamps = []  
deletion_threshold = 2

while True:
  ret, frame = cap.read()
  if not ret:
    break


  current_time = cv2.getTickCount() / cv2.getTickFrequency()


  orange_bbox = od.detect(frame)
  if orange_bbox is not None: 
      x, y, x2, y2 = orange_bbox
      cx = int((x + x2) / 2)
      cy = int((y + y2) / 2)
      actual_positions.append((cx, cy))
      predicted = kf.predict(cx, cy)
      predicted_positions.append(predicted)
      timestamps.append(current_time)
  else:
      actual_positions = []
      predicted_positions = []
      timestamps = []


  for i in range(len(timestamps) - 1, -1, -1): 
      if current_time - timestamps[i] > deletion_threshold:
          del actual_positions[i]
          del predicted_positions[i]
          del timestamps[i]


  for i in range(len(actual_positions)):
      cv2.circle(frame, (actual_positions[i][0], actual_positions[i][1]), 20, (0, 0, 255), 4)  # Detected position
      cv2.circle(frame, (predicted_positions[i][0], predicted_positions[i][1]), 20, (255, 0, 0), 4)  # Predicted position
      if i > 0:  
          cv2.line(frame, actual_positions[i - 1], actual_positions[i], (255, 0, 0), 2)
          cv2.line(frame, predicted_positions[i - 1], predicted_positions[i], (0, 0, 255), 2)

  cv2.imshow("Orange Detection", frame)


  if cv2.waitKey(1) == ord('q'):
    break


cap.release()
cv2.destroyAllWindows()
