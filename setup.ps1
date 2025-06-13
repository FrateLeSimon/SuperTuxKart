# Supprime l'ancien venv s'il existe
if (Test-Path -Path ".\venv") {
    Remove-Item -Recurse -Force ".\venv"
    Write-Output "Ancien venv supprimé."
} else {
    Write-Output "Aucun venv trouvé, création du nouveau."
}

# Crée un nouveau venv
python -m venv venv
Write-Output "Nouveau venv créé."

# Active le venv
& .\venv\Scripts\Activate.ps1

# Installe les dépendances depuis requirements.txt
if (Test-Path -Path ".\requirements.txt") {
    pip install --upgrade pip
    pip install -r requirements.txt
    Write-Output "Dépendances installées depuis requirements.txt"
} else {
    Write-Output "Fichier requirements.txt introuvable, installe pyautogui et pygetwindow manuellement."
}