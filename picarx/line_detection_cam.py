import numpy as np
import cv2
from picamera2 import Picamera2, Preview
import time
import picarx_improved

def get_steering_angle(lines, img_width):
    
    # calculate the steering angle based on lines detected 

    if lines is None:
        return 0  # Go straight for now

    left_lines = []
    right_lines = []

    for line in lines:
        for rho, theta in line:
            angle = np.degrees(theta)
            if 30 < angle < 60:  # Right lane lines
                right_lines.append((rho, theta))
            elif 120 < angle < 150:  # Left lane lines
                left_lines.append((rho, theta))

    if not left_lines and not right_lines:
        return 0  # No strong lane markings detected

    avg_left_angle = np.mean([np.degrees(theta) for _, theta in left_lines]) if left_lines else None
    avg_right_angle = np.mean([np.degrees(theta) for _, theta in right_lines]) if right_lines else None

    if avg_left_angle and avg_right_angle:
        avg_steering_angle = (avg_left_angle + avg_right_angle) / 2 - 90
    elif avg_left_angle:
        avg_steering_angle = avg_left_angle - 90
    elif avg_right_angle:
        avg_steering_angle = avg_right_angle - 90
    else:
        avg_steering_angle = 0

    return int(avg_steering_angle)



picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()
time.sleep(2)  


px = picarx_improved.Picarx()



cv2.startWindowThread()

while True:
    frame = picam2.capture_array()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)


    steering_angle = get_steering_angle(lines, img_width=640)
    print("streering angle", steering_angle)  # Send this to Picar motor control
        
    px.set_dir_servo_angle(steering_angle)
    px.forward(30)
    time.sleep(0.2)
    px.stop()


    cv2.imshow("Edges", edges)
    cv2.imshow("Camera", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
