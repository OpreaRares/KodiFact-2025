from google import genai
##from modules.input import prompt
def AI(text: str):
    client = genai.Client(api_key="AIzaSyCGXHtTQpjIFpZy7hUQ0ig-YwysrT_RQ1E")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        ##contents = prompt
        contents = "Este corect asta " + text
    )

    return response.text