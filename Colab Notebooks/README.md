# Détecteur de Fraude Bancaire 🏦🚨

Ce projet est une application web interactive de scoring et de détection de transactions bancaires suspectes en temps réel, basée sur un modèle de Machine Learning (**Random Forest**).

## 📋 Table des Matières
- [Description du Projet](#description-du-projet)
- [Architecture des Fichiers](#architecture-des-fichiers)
- [Prérequis et Installation](#prérequis-et-installation)
- [Lancement de l'Application](#lancement-de-lapplication)
- [Fonctionnalités du Dashboard](#fonctionnalités-du-dashboard)
- [Entraînement du Modèle](#entraînement-du-modèle)

---

## 🔍 Description du Projet
L'application utilise un modèle **Random Forest** pré-entraîné avec scikit-learn pour analyser chaque transaction saisie et estimer sa probabilité d'être **Normale** ou **Suspecte**. Un tableau de bord moderne et réactif (avec mode sombre/clair) permet de simuler des transactions ou d'appliquer des scénarios types de fraude pour observer le comportement du modèle de scoring.

---

## 📁 Architecture des Fichiers

*   **`app.py`** : Serveur backend développé avec FastAPI. Il expose les points de terminaison d'API pour les prédictions et sert l'interface web (dashboard).
*   **`dashboard.html`** : Interface web interactive construite avec du HTML/CSS moderne (Zinc design) et du JavaScript natif (Vanilla JS). Utilise **Chart.js** pour la visualisation des données.
*   **`train_and_save_model.py`** : Script Python pour nettoyer les données, entraîner le modèle Random Forest et exporter les fichiers requis.
*   **`model.ipynb`** : Notebook Jupyter de recherche et d'exploration contenant le processus complet de conception et de test du modèle.
*   **`features.json`** : Métadonnées sur les colonnes de caractéristiques (features) et les variables catégorielles encodées pour assurer l'alignement de l'API.
*   **`random_forest_model.pkl`** : Le modèle Random Forest entraîné et sauvegardé au format pickle.
*   **`scaler.pkl`** : L'objet `StandardScaler` utilisé pour normaliser les données avant la prédiction.
*   **`Bank_transaction_scenario1.csv`** : Jeu de données brutes contenant l'historique des transactions d'entraînement.
*   **`requirements.txt`** : Liste des dépendances Python nécessaires au projet.

---

## 🛠️ Prérequis et Installation

### 1. Activer/Créer l'environnement virtuel (Optionnel mais recommandé)
Si vous n'avez pas encore d'environnement virtuel configuré, créez-en un dans le dossier racine :
```powershell
python -m venv .venv
```

### 2. Installer les dépendances
Installez l'ensemble des bibliothèques nécessaires à l'aide de `pip` :
```powershell
.venv\Scripts\pip install -r requirements.txt
```

---

## 🚀 Lancement de l'Application

### Étape 1 : Démarrer le serveur API FastAPI
Lancez le serveur Uvicorn avec rechargement automatique :
```powershell
.venv\Scripts\python -m uvicorn app:app --reload
```

### Étape 2 : Ouvrir l'interface dans votre navigateur
Accédez à l'URL suivante pour ouvrir le tableau de bord :
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📊 Fonctionnalités du Dashboard

*   **Simulateur de Transaction** : Saisissez manuellement les caractéristiques d'une transaction (montant, type, statut, localisation, date) pour l'analyser.
*   **Cas de Test & Scénarios Types** : Remplissage automatique avec des cas d'utilisation courants (transactions standard, retraits modérés, montants très élevés ou opérations suspectes de nuit).
*   **Générateur Aléatoire** : Permet de générer instantanément de fausses données de transaction cohérentes pour tester la réactivité.
*   **Niveaux de Risque Visuels** : Risque **Faible** (vert), **Moyen** (orange) et **Élevé** (rouge) affichés sous forme de badges avec recommandations associées.
*   **Graphiques Interactifs** :
    *   *Répartition du Risque* : Graphique en anneau montrant le pourcentage de transactions analysées par niveau de risque.
    *   *Flux des Montants* : Courbe de tendance montrant l'évolution des volumes financiers scannés.
*   **Historique Local** : Une table garde la trace des transactions scannées au cours de la session (sauvegardé localement dans le navigateur avec `localStorage`).

---

## 🧠 Entraînement du Modèle

Si vous modifiez le jeu de données `Bank_transaction_scenario1.csv` ou si vous souhaitez réentraîner le modèle, vous pouvez lancer le script suivant :
```powershell
.venv\Scripts\python train_and_save_model.py
```
Cela mettra à jour automatiquement les fichiers `random_forest_model.pkl`, `scaler.pkl` et `features.json` pour qu'ils soient directement pris en compte par l'API de scoring au prochain appel.
