import flet as ft
import speech_recognition as sr
from modules.ai_client import AI

MIC_INDEX = 2


def recognize_speech(column: ft.Column):
    # Create text box for output
    txt_output = ft.TextField(label="Recognized Speech", multiline=True, expand=True, value="")

    column.controls.clear()
    column.controls.extend([txt_output,ft.ProgressRing()])
    column.update()

    """ Continuously listen for speech and update the text field. """
    recognizer = sr.Recognizer()

    with sr.Microphone(device_index=MIC_INDEX) as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise

    try:
        while txt_output.value == "":
            with sr.Microphone(device_index=MIC_INDEX) as source:
                print("Listening...")
                audio = recognizer.listen(source)

                # Convert speech to text
                text = recognizer.recognize_google(audio, language="ro-RO")
                print(f"Recognized: {text}")

                # Update the text field
                txt_output.value = text
                column.update()

        column.controls.pop()
        column.update()

        column.controls.append(ft.Markdown(
                value=AI(txt_output.value),
                selectable=True,
                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            )
        )
        column.update()

    except sr.UnknownValueError:
        txt_output.value = "Could not understand the audio."
        column.update()
    except sr.RequestError:
        txt_output.value = "Could not connect to the Speech API."
        column.update()