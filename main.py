import flet as ft
from modules.ai_client import AI
from modules.speechtotext import recognize_speech
import threading

def main(page: ft.Page):
    page.title = "Live Speech-to-Text"

    col = ft.Column([])

    # Button to start recognition
    def start_listening(e):
        thread = threading.Thread(target=recognize_speech, args=(col,))
        thread.daemon = True  # Stops when the app closes
        thread.start()

    start_button = ft.ElevatedButton("Start Listening", on_click=start_listening)

    # Layout
    page.add(col, start_button)


ft.app(main)

##md davinki2025
##cd davinki2025
##python -m venv .venv
##.venv\Scripts\activate