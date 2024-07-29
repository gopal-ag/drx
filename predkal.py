import cv2
from green_detector import OrangeDetector
from kalmanfilter import KalmanFilter


cap = cv2.VideoCapture(0)  


od = OrangeDetector()
kf = KalmanFilter()

while True:
    ret, frame = cap.read()
    if not ret:
        break


    orange_bbox = od.detect(frame)  
    x, y, x2, y2 = orange_bbox
    cx = int((x + x2) / 2)
    cy = int((y + y2) / 2)


    predicted = kf.predict(cx, cy)
    

    cv2.circle(frame, (cx, cy), 20, (0, 0, 255), 4)  # Detected position
    cv2.circle(frame, (predicted[0], predicted[1]), 20, (255, 0, 0), 4)  # Predicted position


    cv2.imshow("Frame", frame)
    

    key = cv2.waitKey(1)
    if key == 27:
        break 

cap.release()
cv2.destroyAllWindows()
