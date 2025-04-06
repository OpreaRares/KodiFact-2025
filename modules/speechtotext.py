import flet as ft
import speech_recognition as sr
import threading
from modules.ai_client import AI

MIC_INDEX = 1  # Change this based on your microphone index

def recognize_speech(column: ft.Column):
    recognizer = sr.Recognizer()
    stop_listening = False

    # UI Elements
    txt_output = ft.TextField(label="Vorbire Recunoscută", multiline=True, expand=True, value="")
    column.controls.clear()
    column.controls.extend([txt_output, ft.ProgressRing()])
    column.update()

    def listen():
        nonlocal stop_listening
        with sr.Microphone(device_index=MIC_INDEX) as source:
            recognizer.adjust_for_ambient_noise(source)  # Reduce background noise

        while not stop_listening:
            try:
                with sr.Microphone(device_index=MIC_INDEX) as source:
                    print("Listening...")
                    audio = recognizer.listen(source)

                    # Convert speech to text
                    text = recognizer.recognize_google(audio, language="ro-RO")
                    print(f"Recognized: {text}")

                    # Update recognized text
                    txt_output.value += text + "\n"
                    column.update()

                    # Send to AI immediately
                    def ask_ai():
                        ai_response = AI(text)
                        column.controls.append(ft.Markdown(
                            value=ai_response,
                            selectable=True,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        ))
                        column.update()

                    # Run AI call in separate thread so UI doesn't freeze
                    threading.Thread(target=ask_ai, daemon=True).start()

            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError:
                print("Could not connect to the Speech API.")

    # Start listening thread
    listen_thread = threading.Thread(target=listen, daemon=True)
    listen_thread.start()
