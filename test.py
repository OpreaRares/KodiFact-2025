import flet as ft


def main(page: ft.Page):
    # Create a text box to show the transcribed text
    txt_output = ft.TextField(label="Voice Input", multiline=True, expand=True)

    # Add the button to start voice recognition
    def start_voice_recognition(e):
        page.add(ft.Html('''
            <script>
                const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                recognition.lang = 'en-US';
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.start();

                recognition.onresult = function(event) {
                    let final_transcript = '';
                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        if (event.results[i].isFinal) {
                            final_transcript += event.results[i][0].transcript;
                        }
                    }
                    document.getElementById("voice-text").value = final_transcript;
                }
            </script>
        ''', id="js_script"))

    # Create button to start voice input
    start_button = ft.ElevatedButton("Start Voice Recognition", on_click=start_voice_recognition)

    # Layout
    page.add(txt_output, start_button)


ft.app(main)