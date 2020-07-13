import cv2
import numpy as np
import dlib
from math import hypot
import time
from playsound import playsound
import _thread
import time

cap = cv2.VideoCapture(0)#camera port 0


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def print_time(threadName, delay):
    playsound('jasonderulo.mp3')

def midpoint(p1,p2):
    return int((p1.x + p2.x)/2),int((p1.y + p2.y)/2)

font = cv2.FONT_HERSHEY_SIMPLEX

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    hor_line = cv2.line(frame, left_point, right_point,(0,255,0), 1)

    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    ver_line = cv2.line(frame, center_top, center_bottom,(0,255,0), 1)

    #length of the line
    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    ratio = hor_line_length/ ver_line_length, ver_line_length
    return ratio

blink = 1
TOTAL = 0
thres = 5.1
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#for gray images(lightweight)
    faces = detector(gray)
    for face in faces:
        #x, y = face.left(), face.top()
        #x1, y1 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x,y), (x1,y1), (0,255,0), 3 )# green box, thickness of box
        landmarks = predictor(gray, face)
        left_eye_ratio,_ = get_blinking_ratio([36,37,38,39,40,41], landmarks)
        right_eye_ratio, myVerti = get_blinking_ratio([42,43,44,45,46,47], landmarks)
        blinking_ratio = (left_eye_ratio+right_eye_ratio)/2
        personal_threshold = 0.67 * myVerti #0.67 is just the best constant I found with experimentation
        cv2.putText(frame, "left ratio: {:.2f}".format(left_eye_ratio), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "right ratio: {:.2f}".format(right_eye_ratio), (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if (left_eye_ratio>personal_threshold or right_eye_ratio>personal_threshold) and blink == 1:
            TOTAL += 1
            time.sleep(0.1)#average persons blinking time
            _thread.start_new_thread( print_time , ("Thread-1", 0, )) 
        if (left_eye_ratio>personal_threshold or right_eye_ratio>personal_threshold):
            blink = 0
        else:
            blink = 1

        cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(5)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindow()