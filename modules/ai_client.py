from google import genai
##from modules.input import prompt
def AI(text: str, system_prompt: str = None):
    client = genai.Client(api_key="AIzaSyCGXHtTQpjIFpZy7hUQ0ig-YwysrT_RQ1E")

    base_prompt = ""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=text
    )

    return response.text