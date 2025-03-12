import flet as ft
import sqlite3
import sys


# Setup database
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


# Setup register
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


# Setup authenticate
def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None


# Main
def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 500
    mode = sys.argv[1] if len(sys.argv) > 1 else "signin"

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

    if mode == "signup":
        page.title = "Sign Up"
        page.add(
            ft.ResponsiveRow([
            ft.Column([
                ft.Row([],height=150),
                ft.Text("Sign Up", size=24, weight=ft.FontWeight.BOLD),
                username_field,
                password_field,
                ft.ElevatedButton("Sign Up", on_click=sign_up),
                message
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER)
        )
    else:
        page.title = "Sign In"
        page.add(
            ft.ResponsiveRow([
            ft.Column([
                ft.Row([],height=150),
                ft.Text("Sign In", size=24, weight=ft.FontWeight.BOLD),
                username_field,
                password_field,
                ft.ElevatedButton("Sign In", on_click=sign_in),
                message
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER)
        )


if __name__ == "__main__":
    init_db()
    ft.app(main)

#ma doare capul