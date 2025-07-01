import mediapipe as mp
import cv2
import numpy as np
import joblib
import threading
import time
import pyttsx3
import firebase_admin
from firebase_admin import credentials, db

# Firebase setup
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pyfire-da0f6-default-rtdb.firebaseio.com/'
})

# TTS setup
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 130)
last_spoken = ""

# Load model
classifier = joblib.load('gesture_classifier.pkl')

# Mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
import mediapipe.python.solutions.face_mesh_connections as face_mesh_connections

# Webcam
cap = cv2.VideoCapture(0)

gesture_timer = None
gesture_candidate = None

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = holistic.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Face mesh (tessellation + contours)
        if results.face_landmarks:
            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                                      mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                                      mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1))

        # Right Hand
        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2))

        # Left Hand
        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2))

        # Pose
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        # Extract landmarks
        landmarks = []
        if results.pose_landmarks:
            for lm in results.pose_landmarks.landmark:
                landmarks.extend([lm.x, lm.y])
        if results.left_hand_landmarks:
            for lm in results.left_hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y])
        if results.right_hand_landmarks:
            for lm in results.right_hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y])

        if landmarks:
            landmarks = np.array(landmarks).flatten()
            try:
                prediction = classifier.predict([landmarks])[0]
                proba = classifier.predict_proba([landmarks])[0]
                confidence = np.max(proba) * 100
            except:
                prediction = "Unknown"
                confidence = 0

            cv2.putText(image, f'Gesture: {prediction} ({confidence:.2f}%)', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if prediction != last_spoken and confidence > 80:
                def speak_text(text):
                    tts_engine.say(text)
                    tts_engine.runAndWait()

                threading.Thread(target=speak_text, args=(prediction,), daemon=True).start()
                last_spoken = prediction

            current_time = time.time()
            if prediction != gesture_candidate:
                gesture_candidate = prediction
                gesture_timer = current_time
            elif prediction == gesture_candidate and (current_time - gesture_timer) >= 5:
                ref = db.reference('lastGesture')
                ref.set(prediction)
                print("Gesture Saved to Firebase.")
                gesture_timer = current_time + 1000
        else:
            cv2.putText(image, 'No pose or hands detected', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Gesture Recognition with Mesh', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
