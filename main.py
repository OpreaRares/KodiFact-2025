import flet as ft
from modules.ai_client import AI

def main(page: ft.Page):
    page.add(ft.Text(value=AI()))



ft.app(main)

##md davinki2025
##cd davinki2025
##python -m venv .venv
##.venv\Scripts\activate