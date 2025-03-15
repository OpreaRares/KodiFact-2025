from google import genai
from modules.input import prompt

def AI():
    client = genai.Client(api_key="AIzaSyCGXHtTQpjIFpZy7hUQ0ig-YwysrT_RQ1E")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents = prompt
    )

    return(response.text)