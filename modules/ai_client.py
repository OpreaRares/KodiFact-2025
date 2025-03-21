from google import genai
##from modules.input import prompt
def AI(text: str):
    client = genai.Client(api_key="AIzaSyCGXHtTQpjIFpZy7hUQ0ig-YwysrT_RQ1E")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        ##contents = prompt
        contents = "Propozitia care urmeaza poate fi o afirmatie sau intrebare. In cazul unei afirmatii, verifica daca este corect. Daca da, spune Nimic eronat. . Daca nu, explica eroarea. In cazul unei intrebari, prezinta raspunsul. Spune DOAR ce este cerut. Acesta este textul: " + text
        #dc e asa de sassy gemini incerc sa ii dau un prompt si imi da ca de ce nu am intrebat adecvat
    )

    return response.text