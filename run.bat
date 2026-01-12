@echo off
REM Script de lancement rapide du projet (Windows)

echo ==========================================
echo  GPS Intelligent - Projet ProjetS5_maths
echo ==========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python n'est pas installé
    pause
    exit /b 1
)

echo [OK] Python détecté
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv" (
    echo [*] Création de l'environnement virtuel...
    python -m venv venv
    echo [OK] Environnement virtuel créé
)

REM Activer l'environnement virtuel
echo [*] Activation de l'environnement virtuel...
call venv\Scripts\activate

REM Installer les dépendances si nécessaire
if not exist "venv\installed" (
    echo [*] Installation des dépendances...
    pip install -r requirements.txt >nul 2>&1
    echo. > venv\installed
    echo [OK] Dépendances installées
)

echo.
echo Menu :
echo   1. Lancer la démonstration interactive
echo   2. Exécuter les expériences complètes
echo   3. Lancer les tests unitaires
echo   4. Voir la documentation
echo.

set /p choice="Votre choix (1-4) : "

if "%choice%"=="1" (
    echo.
    echo [*] Lancement de la démonstration...
    python demo.py
) else if "%choice%"=="2" (
    echo.
    echo [*] Exécution des expériences...
    python experiments\comparaison_algos.py
) else if "%choice%"=="3" (
    echo.
    echo [*] Exécution des tests...
    pytest tests\ -v
) else if "%choice%"=="4" (
    echo.
    echo [*] Documentation disponible dans docs\
    dir /B docs
) else (
    echo.
    echo [!] Choix invalide
)

echo.
echo [OK] Terminé
pause


