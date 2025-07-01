import cv2
import mediapipe as mp
import csv
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
import mediapipe.python.solutions.face_mesh_connections as face_mesh_connections

holistic = mp_holistic.Holistic(static_image_mode=False,
                                 min_detection_confidence=0.5,
                                 min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

csv_file = open('gesture_data.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)

print("Press '1', '2', or '3' to label gestures. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = holistic.process(image_rgb)

    landmarks = []

    # Save pose & hand landmarks only
    if results.pose_landmarks:
        for lm in results.pose_landmarks.landmark:
            landmarks.extend([lm.x, lm.y])
    if results.left_hand_landmarks:
        for lm in results.left_hand_landmarks.landmark:
            landmarks.extend([lm.x, lm.y])
    if results.right_hand_landmarks:
        for lm in results.right_hand_landmarks.landmark:
            landmarks.extend([lm.x, lm.y])

    # Draw face mesh
    if results.face_landmarks:
        mp_drawing.draw_landmarks(frame, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                                  mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                                  mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1))

    # Right hand
    mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2))

    # Left hand
    mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2))

    # Pose
    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

    cv2.imshow('Collecting Gesture Data', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('1') and landmarks:
        csv_writer.writerow(landmarks + ['gesture1'])
        print("Saved: gesture1")
    elif key == ord('2') and landmarks:
        csv_writer.writerow(landmarks + ['gesture2'])
        print("Saved: gesture2")
    elif key == ord('3') and landmarks:
        csv_writer.writerow(landmarks + ['gesture3'])
        print("Saved: gesture3")
    elif key == ord('q'):
        break

cap.release()
csv_file.close()
cv2.destroyAllWindows()
