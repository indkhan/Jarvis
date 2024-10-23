import keyboard
import speech_recognition as sr
import pyttsx3
import threading
from queue import Queue
from time import sleep

# Global variables for state management
recording = False
speaking = False
should_run = True
speech_queue = Queue()
recognizer = sr.Recognizer()
engine = pyttsx3.init()


def listen_for_phrase():
    """Listen for audio without stopping automatically"""
    with sr.Microphone() as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        # Set dynamic energy threshold
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 4000  # Adjust this value based on your microphone

        # Use longer phrase_time_limit to prevent premature stopping
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
            return audio
        except sr.WaitTimeoutError:
            return None


def start_listening():
    """Start recording audio"""
    global recording, speaking

    if not recording and not speaking:
        recording = True
        print("\nListening... (Press SPACE to stop)")

        while recording and should_run:
            try:
                audio = listen_for_phrase()
                if (
                    audio and recording
                ):  # Only process if we're still supposed to be recording
                    text = recognizer.recognize_google(audio)
                    print(f"You said: {text}")
                    speech_queue.put(text)

                    # Don't start speaking yet - wait for space key
                    if not speaking and not recording:
                        start_speaking()
            except sr.UnknownValueError:
                pass  # Ignore unrecognized audio and continue listening
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                sleep(1)  # Add delay before retrying
            except Exception as e:
                print(f"Error during recording: {e}")
                sleep(1)  # Add delay before retrying


def speak_text():
    """Function to handle the text-to-speech"""
    global speaking
    try:
        while not speech_queue.empty() and should_run:
            text = speech_queue.get()
            engine.say(text)
            engine.runAndWait()
    except Exception as e:
        print(f"Error during speech: {e}")
    finally:
        speaking = False
        if should_run:  # Only start listening if program should continue
            start_listening()


def start_speaking():
    """Start speaking the recorded text"""
    global speaking

    if not speaking and not speech_queue.empty():
        speaking = True
        # Run speech in a separate thread
        threading.Thread(target=speak_text, daemon=True).start()


def handle_space():
    """Handle space key press"""
    global recording, speaking

    if recording:
        recording = False
        if not speaking and not speech_queue.empty():
            start_speaking()
    elif speaking:
        engine.stop()
        speaking = False
        # Clear the speech queue when interrupting
        while not speech_queue.empty():
            speech_queue.get()
        start_listening()


def main():
    """Main program function"""
    global should_run

    try:
        # Set up hotkey combinations
        keyboard.add_hotkey(
            "ctrl+shift+space",
            lambda: threading.Thread(target=start_listening, daemon=True).start(),
        )
        keyboard.add_hotkey("space", handle_space)

        print("Program started!")
        print("Press Ctrl+Shift+Space to start recording")
        print("Press Space to stop recording/interrupt playback")
        print("Press ESC to exit")

        # Keep running until ESC is pressed
        keyboard.wait("esc")

        # Cleanup
        should_run = False
        recording = False
        speaking = False
        engine.stop()
        print("\nProgram terminated.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Program ended.")


if __name__ == "__main__":
    main()
