import flet as ft
import subprocess


def open_account(mode):
    subprocess.Popen(["python", "account.py", mode])


# Main Flet App
def main(page: ft.Page):
    page.title = "KodiFact"
    page.window_width = 400
    page.window_height = 300

    welcome_text = ft.Text("KodiFact", size=44, weight=ft.FontWeight.BOLD)
    sign_up_button = ft.ElevatedButton("Sign Up", on_click=lambda e: open_account("signup"))
    sign_in_button = ft.ElevatedButton("Sign In", on_click=lambda e: open_account("signin"))

    page.add(
        ft.Column([
            welcome_text,
            ft.Row([
                sign_up_button,
                sign_in_button
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )


ft.app(main)

