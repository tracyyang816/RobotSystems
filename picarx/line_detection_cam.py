import numpy as np
import cv2
from picamera2 import Picamera2, Preview
import time
import picarx_improved
import math
import random

def get_steering_angle(segments, frame):
    left_fit = []
    right_fit = []

    height, width, _ = frame.shape
    boundary = 1 / 3
    left_region_boundary = width * (1 - boundary)
    right_region_boundary = width * boundary

    if segments:
        for x1, y1, x2, y2 in segments:
            if x1 == x2:
                continue  # Ignore vertical lines
            slope, intercept = np.polyfit((x1, x2), (y1, y2), 1)

            if x1 < left_region_boundary and x2 < left_region_boundary: # slope < 0 and 
                left_fit.append((slope, intercept))
            elif x1 > right_region_boundary and x2 > right_region_boundary: # slope > 0 and
                right_fit.append((slope, intercept))

    lanes = []
    if left_fit:
        lanes.append(np.average(left_fit, axis=0))
    if right_fit:
        lanes.append(np.average(right_fit, axis=0))

    if not lanes:
        return False

    slope, intercept = lanes[0]
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
px.set_cam_tilt_angle(-50)
last_angle = 0

no_line_count = 0

while True:
    frame = picam2.capture_array()

    height, width, _ = frame.shape

    # Crop only the lower 1/3 of the frame
    lower_third = frame[int(height * (2/3)):, :]

    gray = cv2.cvtColor(lower_third, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=10, maxLineGap=50)

    segments = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            segments.append([x1, y1, x2, y2])

    if segments:
        for (x1, y1, x2, y2) in segments:
            cv2.line(lower_third, (x1, y1), (x2, y2), (0, 0, 255), 2)

    steering_angle = get_steering_angle(segments, lower_third)
    print("Steering Angle:", steering_angle)


    #cv2.imshow("Edges", edges)  # Edge detection view
    # cv2.imshow("Lines", lines)
    cv2.imshow("Lane Detection", frame)  # Camera view with detected lanes
    
    

    if no_line_count > 5:
        no_line_count = 0
        px.set_dir_servo_angle(last_angle)
        px.forward(30)
        time.sleep(0.1)
        px.stop()

    if steering_angle == False:
        no_line_count += 1
    else: 
        last_angle = steering_angle
        px.set_dir_servo_angle(steering_angle)
        px.forward(30)
        time.sleep(0.1)
        px.stop()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
