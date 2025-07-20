import speech_recognition as sr
import pyttsx3
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

# Set the path to the credentials for Firebase Admin
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
# --- Firebase Setup ---
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pyfire-da0f6-default-rtdb.firebaseio.com/'  # Replace with your Firebase URL
})

# --- Speech Recognition and TTS Setup ---
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 160)

# --- Listen from Microphone ---
with sr.Microphone() as source:
    print("Please speak something...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print("You said:", text)

        # Speak it out loud
        tts_engine.say(f"You said: {text}")
        tts_engine.runAndWait()

        # --- Save last word/sentence to Firebase ---
        ref = db.reference('lastWord')  # This creates or updates the "lastWord" node
        ref.set(text)
        print("Saved to Firebase.")

    except sr.UnknownValueError:
        print("Sorry, could not understand your speech.")
        tts_engine.say("Sorry, I could not understand what you said.")
        tts_engine.runAndWait()
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        tts_engine.say("Sorry, I could not reach the speech service.")
        tts_engine.runAndWait()
