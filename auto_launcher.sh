#auto_launcher.sh

#!/bin/bash

# Variables d'environnement pour les chemins
SCRIPT_DIR="/home/brummel/Desktop/compteur"
ENV_DIR="${SCRIPT_DIR}/env"
SCRIPT_OVERTURE="${SCRIPT_DIR}/Compteur-intelligent/ouverture.py"
SCRIPT_MAIN="${SCRIPT_DIR}/Compteur-intelligent/main.py"

# Activer l'environnement virtuel
source "${ENV_DIR}/bin/activate"

# Fonction pour lancer un script et gérer les erreurs
function run_script() {
    local script="$1"
    echo "Lancer $script"
    python "$script" &> "${script}.log"
    if [ $? -ne 0 ]; then
        echo "Erreur lors de l'exécution de $script. Voir le log."
    fi
}

# Changer de répertoire
cd "${SCRIPT_DIR}"

# Lancer les scripts
run_script "${SCRIPT_OVERTURE}" &  # Lancer ouverture.py en arrière-plan
run_script "${SCRIPT_MAIN}"         # Lancer main.py