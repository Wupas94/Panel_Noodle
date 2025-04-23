# Panel Noodle

System zarządzania czasem pracy dla zespołów, napisany w Django.

## Funkcjonalności

- ✅ Rejestracja czasu pracy
- ✅ Role użytkowników (Admin, Manager, Pracownik)
- ✅ Panel administracyjny
- ✅ Zarządzanie zespołem
- ✅ Zatwierdzanie wpisów czasu pracy
- ✅ Nowoczesny interfejs użytkownika

## Wymagania

- Python 3.8+
- Django 5.0.2
- Pozostałe zależności w `requirements.txt`

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/TWÓJ_USERNAME/Panel_Noodle.git
cd Panel_Noodle
```

2. Stwórz wirtualne środowisko i aktywuj je:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Skopiuj plik `.env.example` do `.env` i uzupełnij zmienne środowiskowe:
```bash
cp .env.example .env
```

5. Wykonaj migracje:
```bash
python manage.py migrate
```

6. Stwórz superużytkownika:
```bash
python manage.py createsuperuser
```

7. Uruchom serwer deweloperski:
```bash
python manage.py runserver
```

## Struktura projektu

```
Panel_Noodle/
├── core/               # Główna aplikacja z modelami
├── dashboard/          # Aplikacja panelu użytkownika
├── templates/          # Szablony HTML
├── panel_noodle/       # Główny moduł projektu
├── manage.py
├── requirements.txt
└── README.md
```

## Licencja

MIT

## Autorzy

- Twórca projektu 