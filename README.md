# todo_api
Todo API

REST API w Pythonie do zarządzania zadaniami z autentykacją użytkowników.
Każdy użytkownik widzi i zarządza tylko swoimi zadaniami.

Funkcje:
- Rejestracja i logowanie (JWT / OAuth2)
- Dodawanie, edytowanie, usuwanie i przeglądanie zadań
- Każdy użytkownik ma dostęp tylko do swoich danych

Tech stack: Python, FastAPI, SQLite, Pydantic, JWT


## Uruchomienie

1. Zainstaluj zależności:
pip install fastapi uvicorn python-jose pwdlib pydantic

2. Uruchom serwer:
uvicorn main:app --reload

3. Otwórz dokumentację API w przeglądarce:
http://127.0.0.1:8000/docs

