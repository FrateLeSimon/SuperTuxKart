#!/bin/bash
# Script d'installation tout-en-un pour Linux/Mac
# Crée le venv, installe les dépendances, active le venv, relance le setup

python3.9 setup_project.py
source venv/bin/activate
python setup_project.py 