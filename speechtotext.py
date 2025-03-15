import flet as ft
import speech_recognition as sr
import threading

MIC_INDEX = 2


def recognize_speech(txt_output):
    """ Continuously listen for speech and update the text field. """
    recognizer = sr.Recognizer()

    with sr.Microphone(device_index=MIC_INDEX) as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise

    while True:
        try:
            with sr.Microphone(device_index=MIC_INDEX) as source:
                print("Listening...")
                audio = recognizer.listen(source)

                # Convert speech to text
                text = recognizer.recognize_google(audio, language="ro-RO")
                print(f"Recognized: {text}")

                # Update the text field
                txt_output.value = text
                txt_output.update()

        except sr.UnknownValueError:
            txt_output.value = "Could not understand the audio."
            txt_output.update()
        except sr.RequestError:
            txt_output.value = "Could not connect to the Speech API."
            txt_output.update()


def main(page: ft.Page):
    """ Main Flet UI """
    page.title = "Live Speech-to-Text"

    # Create text box for output
    txt_output = ft.TextField(label="Recognized Speech", multiline=True, expand=True)

    # Button to start recognition
    def start_listening(e):
        thread = threading.Thread(target=recognize_speech, args=(txt_output,))
        thread.daemon = True  # Stops when the app closes
        thread.start()

    start_button = ft.ElevatedButton("Start Listening", on_click=start_listening)

    # Layout
    page.add(txt_output, start_button)


ft.app(target=main)