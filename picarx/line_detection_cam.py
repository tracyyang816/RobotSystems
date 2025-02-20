import numpy as np
import cv2
from picamera2 import Picamera2, Preview
import time
import picarx_improved
import math

def get_steering_angle(frame):
  
    # Convert frame to HSV and create a mask for lane colors
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    min_hue = np.array([60, 40, 40])
    max_hue = np.array([150, 255, 255])
    mask = cv2.inRange(hsv, min_hue, max_hue)

    # Apply edge detection
    edges = cv2.Canny(mask, 200, 400)

    # Detect line segments using Hough Transform
    segments = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, minLineLength=10, maxLineGap=50)

    # Lane detection parameters
    left_fit = []
    right_fit = []
    height, width, _ = frame.shape
    boundary = 1 / 3
    left_region_boundary = width * (1 - boundary)
    right_region_boundary = width * boundary

    # Filter detected lines into left and right lanes
    if segments is not None:
        for segment in segments:
            for x1, y1, x2, y2 in segment:
                if x1 == x2:
                    continue  # Ignore vertical lines
                slope, intercept = np.polyfit((x1, x2), (y1, y2), 1)
                
                if slope < 0 and x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
                elif slope > 0 and x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    # Compute average lane line
    lanes = []
    if left_fit:
        left_fit_avg = np.average(left_fit, axis=0)
        lanes.append(left_fit_avg)
    if right_fit:
        right_fit_avg = np.average(right_fit, axis=0)
        lanes.append(right_fit_avg)

    # Compute steering angle
    if not lanes:
        return 90  # Default to straight if no lanes detected

    slope, intercept = lanes[0]  # Use first detected lane for angle calculation
    y1, y2 = height, int(height / 2)
    x1, x2 = int((y1 - intercept) / slope), int((y2 - intercept) / slope)
    
    x_offset = x2 - x1
    y_offset = y2
    angle_to_mid_radian = math.atan(x_offset / y_offset)
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)

    return angle_to_mid_deg



picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()
time.sleep(2)  


px = picarx_improved.Picarx()



# cv2.startWindowThread()

while True:
    frame = picam2.capture_array()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)


    steering_angle = get_steering_angle(frame)
    print("streering angle", steering_angle)  # Send this to Picar motor control
        
    px.set_dir_servo_angle(steering_angle)
    px.forward(30)
    time.sleep(0.2)
    px.stop()


    # cv2.imshow("Edges", edges)
    
    # cv2.imshow("Camera", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# cv2.destroyAllWindows()
picam2.stop()
