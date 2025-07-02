@echo off
REM Script d'installation tout-en-un pour Windows
REM Crée le venv, installe les dépendances, active le venv, relance le setup

py -3.11 setup_project.py
call venv\Scripts\activate
python setup_project.py
pause 