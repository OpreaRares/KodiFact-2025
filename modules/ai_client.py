from google import genai
##from modules.input import prompt
# ai_client.py
conversation_history = []

def AI(text: str):
    global conversation_history

    # Append the new user message to the history
    conversation_history.append(f"Utilizator: {text}")

    # Join all messages so far
    context = "\n".join(conversation_history)

    # Add a base instruction at the top
    full_prompt = (
        "Numele tau este KodiFact. Esti un program care primeste un text si il verifica si il corecteaza daca informatiile prezentate sunt false; daca sunt, le prezinti in forma corecta. Adauga informatii suplimentare despre ceea ce s-a zis si aprofundeaza ce ai zis. Vei primi text incontinuu si trebuie sa legi textele pe care le primesti cu cele precedente ca sa poti prezenta informatii corecte in general la tot ce s-a spus tinand cont de context. Vei prezenta DOAR informatiile cerute si sa nu incepi cu KodiFact: Aici este conversatia ta cu utilizatorul pana in acest moment: . Vei detecta greseli logice in discurs, adica daca apar contradictii, le vei mentiona si corecta. Pentru orice eroare din punct de vedere logic sau factual vei mentiona propriu zis greseala si partea corectata. \n\n"

        + context
    )

    client = genai.Client(api_key="AIzaSyCGXHtTQpjIFpZy7hUQ0ig-YwysrT_RQ1E")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=full_prompt
    )

    ai_response = response.text
    conversation_history.append(f"KodiFact: {ai_response}")

    return ai_response