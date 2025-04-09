import flet as ft
import sqlite3
import threading
from modules.ai_client import AI
from modules.speechtotext import recognize_speech

systemPrompt = "Numele tau este KodiFact. Esti un program care primeste un text si il verifica si il corecteaza daca informatiile sunt false; daca sunt, le prezinti in forma corecta. Vei primi text incontinuu si trebuie sa legi textele pe care le primesti cu cele precedente ca sa poti prezenta informatii corecte in general la tot ce s-a spus tinand cont de context. Vei prezenta informatiile in scurt. Raspunde la acest mesaj DOAR cu Bun venit la KodiFact."
def reset_history():
    global conversation_history
    conversation_history = []
# Initialize database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Register user
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True, "Utilizatorul s-a înregistrat cu succes!"
    except sqlite3.IntegrityError:
        return False, "Numele de utilizator există deja!"
    finally:
        conn.close()

# Authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Main Flet App
def main(page: ft.Page):
    page.title = "KodiFact"
    page.window_width = 400
    page.window_height = 500

    def go_to(route):
        page.views.clear()
        if route == "main":
            page.views.append(main_view())
        elif route == "signup":
            page.views.append(signup_view())
        elif route == "signin":
            page.views.append(signin_view())
        elif route == "app":
            page.views.append(app_view())
        page.update()

    def main_view():
        return ft.View(
            "/",
            controls=[
                ft.Text("KodiFact", size=44, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Inregistrare", on_click=lambda e: go_to("signup")),
                ft.ElevatedButton("Conectare", on_click=lambda e: go_to("signin"))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    def signup_view():
        username_field = ft.TextField(label="Nume utilizator", width=300)
        password_field = ft.TextField(label="Parola", password=True, width=300)
        message = ft.Text()

        def sign_up(e):
            username = username_field.value.strip()
            password = password_field.value.strip()
            if not username or not password:
                message.value = "Completeaza ambele campuri!"
            else:
                success, msg = register_user(username, password)
                message.value = msg
            message.update()

        return ft.View(
            "/signup",
            controls=[
                ft.Text("Inregistrare", size=24, weight=ft.FontWeight.BOLD),
                username_field,
                password_field,
                ft.ElevatedButton("Inregistrare", on_click=sign_up),
                ft.ElevatedButton("Inapoi la Pagina Principala", on_click=lambda e: go_to("main")),
                message
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    def signin_view():
        username_field = ft.TextField(label="Nume utilizator", width=300)
        password_field = ft.TextField(label="Parola", password=True, width=300)
        message = ft.Text()

        def sign_in(e):
            username = username_field.value.strip()
            password = password_field.value.strip()
            if not username or not password:
                message.value = "Completeaza ambele campuri!"
            else:
                if authenticate_user(username, password):
                    go_to("app")
                else:
                    message.value = "Nume ulilizator sau parola este incorecta!"
            page.update()

        return ft.View(
            "/signin",
            controls=[
                ft.Text("Conectare", size=24, weight=ft.FontWeight.BOLD),
                username_field,
                password_field,
                ft.ElevatedButton("Conectare", on_click=sign_in),
                ft.ElevatedButton("Inapoi la Pagina Principala", on_click=lambda e: go_to("main")),
                message
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    def app_view():
        col = ft.Column([])

        # Initial message placeholder
        ai_intro = ft.Text(value="", selectable=True)
        col.controls.append(ai_intro)

        # Function to call AI with the system prompt when the app opens
        def load_intro():
            intro_response = AI(systemPrompt)  # Call with initial greeting
            ai_intro.value = intro_response  # Update the text with response
            page.update()

        # Run the above function in a thread
        threading.Thread(target=load_intro, daemon=True).start()

        # Listening button
        def start_listening(e):
            thread = threading.Thread(target=recognize_speech, args=(col,))
            thread.daemon = True
            thread.start()

        start_button = ft.ElevatedButton("Ascultă", on_click=start_listening)
        return ft.View("/app", controls=[col, start_button])

    page.on_route_change = lambda e: go_to(e.route.strip("/"))
    page.views.append(main_view())
    page.update()

if __name__ == "__main__":
    init_db()
    ft.app(main)
