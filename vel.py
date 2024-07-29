import cv2
import imutils
import time


greenLower = (29, 86, 6)
greenUpper = (64, 255, 250)


vs = cv2.VideoCapture(0)
time.sleep(2.0)


prev_center = None
prev_time = None
velocity_threshold = 5  
pixels_per_meter = 100

while True:

    ret, frame = vs.read()

    if not ret:
        break

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    velocity = 0


    if len(cnts) > 0:

        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)


            if prev_center is not None and prev_time is not None:
                dx = center[0] - prev_center[0]
                dy = center[1] - prev_center[1]
                dt = time.time() - prev_time
                distance_px = (dx**2 + dy**2)**0.5
                distance_m = distance_px / pixels_per_meter
                if distance_m > (velocity_threshold / pixels_per_meter):
                    velocity = distance_m / dt
                else:
                    velocity = 0


            prev_center = center
            prev_time = time.time()


    cv2.putText(frame, f"Velocity: {velocity:.2f} cm/s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


    cv2.imshow("Frame", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.release()
cv2.destroyAllWindows()
