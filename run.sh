#!/bin/bash
# Script de lancement rapide du projet

echo "=========================================="
echo " GPS Intelligent - Projet ProjetS5_maths"
echo "=========================================="
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✓ Python détecté : $(python3 --version)"
echo ""

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    echo "✓ Environnement virtuel créé"
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances si nécessaire
if [ ! -f "venv/installed" ]; then
    echo "📥 Installation des dépendances..."
    pip install -r requirements.txt > /dev/null 2>&1
    touch venv/installed
    echo "✓ Dépendances installées"
fi

echo ""
echo "Menu :"
echo "  1. Lancer la démonstration interactive (console)"
echo "  2. Exécuter les expériences complètes"
echo "  3. Lancer les tests unitaires"
echo "  4. Lancer l'application web interactive"
echo "  5. Voir la documentation HTML"
echo ""

read -p "Votre choix (1-5) : " choice

case $choice in
    1)
        echo ""
        echo "🚀 Lancement de la démonstration..."
        python3 demo.py
        ;;
    2)
        echo ""
        echo "🧪 Exécution des expériences..."
        python3 experiments/comparaison_algos.py
        ;;
    3)
        echo ""
        echo "🧪 Exécution des tests..."
        pytest tests/ -v
        ;;
    4)
        echo ""
        echo "🌐 Lancement de l'application web..."
        echo "👉 Ouvrez votre navigateur sur http://localhost:8501"
        streamlit run webapp_demo.py
        ;;
    5)
        echo ""
        echo "📚 Ouverture de la documentation..."
        ./voir_documentation.sh
        ;;
    *)
        echo ""
        echo "⚠️  Choix invalide"
        ;;
esac

echo ""
echo "✓ Terminé"

