@echo off

:: Virtuelle Umgebung erstellen
python -m venv venv

:: Virtuelle Umgebung aktivieren
call venv\Scripts\activate

:: Abhängigkeiten installieren
pip install -r requirements.txt

:: Datenbankmigrationen durchführen
python manage.py makemigrations
python manage.py migrate

:: Lokalen Server starten
python manage.py runserver