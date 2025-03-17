import flet as ft
import sqlite3


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
        return True, "User registered successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists!"
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
        page.update()

    def main_view():
        return ft.View(
            "/",
            controls=[
                ft.Text("KodiFact", size=44, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Sign Up", on_click=lambda e: go_to("signup")),
                ft.ElevatedButton("Sign In", on_click=lambda e: go_to("signin"))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    def signup_view():
        username_field = ft.TextField(label="Username", width=300)
        password_field = ft.TextField(label="Password", password=True, width=300)
        message = ft.Text()

        def sign_up(e):
            username = username_field.value.strip()
            password = password_field.value.strip()
            if not username or not password:
                message.value = "Both fields are required!"
            else:
                success, msg = register_user(username, password)
                message.value = msg
            message.update()

        return ft.View(
            "/signup",
            controls=[
                ft.Text("Sign Up", size=24, weight=ft.FontWeight.BOLD),
                username_field,
                password_field,
                ft.ElevatedButton("Sign Up", on_click=sign_up),
                ft.ElevatedButton("Back to Main", on_click=lambda e: go_to("main")),
                message
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    def signin_view():
        username_field = ft.TextField(label="Username", width=300)
        password_field = ft.TextField(label="Password", password=True, width=300)
        message = ft.Text()

        def sign_in(e):
            username = username_field.value.strip()
            password = password_field.value.strip()
            if not username or not password:
                message.value = "Both fields are required!"
            else:
                if authenticate_user(username, password):
                    message.value = "Login successful!"
                else:
                    message.value = "Invalid username or password!"
            message.update()

        return ft.View(
            "/signin",
            controls=[
                ft.Text("Sign In", size=24, weight=ft.FontWeight.BOLD),
                username_field,
                password_field,
                ft.ElevatedButton("Sign In", on_click=sign_in),
                ft.ElevatedButton("Back to Main", on_click=lambda e: go_to("main")),
                message
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    page.on_route_change = lambda e: go_to(e.route.strip("/"))
    page.views.append(main_view())
    page.update()


if __name__ == "__main__":
    init_db()
    ft.app(main,view=ft.AppView.WEB_BROWSER)
