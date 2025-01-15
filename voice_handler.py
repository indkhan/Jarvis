import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
microphone = sr.Microphone()
speaker = pyttsx3.init()

def listen():
    """Listen for voice input and convert to text"""
    with microphone as source:
        speak("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text.lower()
        except Exception as e:
            speak("Sorry, I didn't catch that. Could you repeat?")
            return ""

def speak(text):
    """Convert text to speech"""
    speaker.say(text)
    speaker.runAndWait()
