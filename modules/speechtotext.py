import flet as ft
import speech_recognition as sr
import threading
import time
from modules.ai_client import AI

MIC_INDEX = 2  # se schimba nr bazat pe nr de la microfon. foloseste test.py pt lista
INTERVAL = 30  # dupa cate secunde trimite inputul la ai


def recognize_speech(column: ft.Column):
    recognizer = sr.Recognizer()
    speech_buffer = []  # lista de propozitii
    stop_listening = False  # bool control

    # UI Elements
    txt_output = ft.TextField(label="Recognized Speech", multiline=True, expand=True, value="")
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

                    # append pt buffer
                    speech_buffer.append(text)

                    # update cu prop noua
                    txt_output.value = " ".join(speech_buffer)
                    column.update()

            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError:
                print("Could not connect to the Speech API.")

    def process_buffer():
        """ Sends the collected speech to AI every INTERVAL seconds. """
        nonlocal stop_listening
        while not stop_listening:
            time.sleep(INTERVAL)  # buffer efectiv
            if speech_buffer:
                full_text = " ".join(speech_buffer)  # join tot textul si buffer text
                speech_buffer.clear()  # reset buffer

                # trimite prompt la AI
                ai_response = AI(full_text)
                column.controls.append(ft.Markdown(
                    value=ai_response,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                ))
                column.update()

    # start speech to text si procesare in 2 threaduri
    listen_thread = threading.Thread(target=listen, daemon=True)
    buffer_thread = threading.Thread(target=process_buffer, daemon=True)

    listen_thread.start()
    buffer_thread.start()

#  :)