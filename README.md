# Détecteur de Fraude Bancaire 🏦🚨

Ce projet est une application web interactive de scoring et de détection de transactions bancaires suspectes en temps réel, basée sur un modèle de Machine Learning (**Random Forest**).

---

## 📋 Table des Matières
- [Description du Projet](#description-du-projet)
- [Architecture des Fichiers](#architecture-des-fichiers)
- [Fonctionnalités du Dashboard](#fonctionnalités-du-dashboard)
- [Prérequis et Installation Locale](#prérequis-et-installation-locale)
- [Déploiement en Ligne (Render)](#déploiement-en-ligne-render)
- [Entraînement du Modèle](#entraînement-du-modèle)

---

## 🔍 Description du Projet
L'application utilise un modèle **Random Forest** pré-entraîné avec scikit-learn pour analyser chaque transaction saisie et estimer sa probabilité d'être **Normale** ou **Suspecte**. Un tableau de bord moderne et réactif (avec mode sombre/clair) permet de simuler des transactions ou d'appliquer des scénarios types de fraude pour observer le comportement du modèle de scoring.

---

## 📁 Architecture des Fichiers

Le dépôt est structuré comme suit :
*   **`render.yaml`** : Fichier Blueprint Render situé à la racine pour automatiser le déploiement du service.
*   **`Colab Notebooks/`** : Dossier contenant le code source et les fichiers de l'application :
    *   **`app.py`** : Serveur backend développé avec FastAPI. Il expose les points de terminaison d'API pour les prédictions et sert l'interface web (dashboard).
    *   **`dashboard.html`** : Interface web interactive construite avec du HTML/CSS moderne (Zinc design) et du JavaScript natif (Vanilla JS). Utilise **Chart.js** pour la visualisation des données.
    *   **`Dockerfile`** : Fichier de build Docker pour conteneuriser l'application avec démarrage dynamique sur le port réseau de Render.
    *   **`train_and_save_model.py`** : Script Python pour nettoyer les données, entraîner le modèle Random Forest et exporter les fichiers requis.
    *   **`model.ipynb`** : Notebook Jupyter de recherche et d'exploration contenant le processus complet de conception et de test du modèle.
    *   **`features.json`** : Métadonnées sur les caractéristiques (features) et les variables catégorielles encodées pour assurer l'alignement de l'API.
    *   **`random_forest_model.pkl`** : Le modèle Random Forest entraîné et sauvegardé au format pickle.
    *   **`scaler.pkl`** : L'objet `StandardScaler` utilisé pour normaliser les données avant la prédiction.
    *   **`Bank_transaction_scenario1.csv`** : Jeu de données brutes contenant l'historique des transactions d'entraînement.
    *   **`requirements.txt`** : Liste des dépendances Python nécessaires au projet.

---

## 📊 Fonctionnalités du Dashboard

*   **Simulateur de Transaction** : Saisissez manuellement les caractéristiques d'une transaction pour l'analyser.
*   **Gestion Détaillée des Échecs** : L'ancien champ de statut simple a été remplacé par un sélecteur **Résultat de la Transaction** permettant d'indiquer précisément la cause d'un échec (soit sur le **montant**, le **lieu**, ou le **mode de transaction**).
*   **Cas de Test & Scénarios Types** : Remplissage automatique avec des cas d'utilisation courants (transactions standard, retraits modérés, montants très élevés ou opérations suspectes de nuit).
*   **Générateur Aléatoire** : Permet de générer instantanément des données de transaction cohérentes (incluant des échecs aléatoires avec causes) pour tester la réactivité.
*   **Niveaux de Risque Visuels** : Risque **Faible** (vert), **Moyen** (orange) et **Élevé** (rouge) affichés sous forme de badges avec des recommandations de sécurité.
*   **Graphiques Interactifs** :
    *   *Répartition du Risque* : Graphique en anneau montrant le pourcentage de transactions analysées par niveau de risque.
    *   *Flux des Montants* : Courbe de tendance montrant l'évolution des volumes financiers scannés.
*   **Historique Local Enrichi** : Une table garde la trace des transactions scannées au cours de la session (sauvegardée localement dans le navigateur avec `localStorage`), affichant désormais le statut de validation ou la cause spécifique de l'échec.

---

## 🛠️ Prérequis et Installation Locale

### 1. Activer/Créer l'environnement virtuel (Optionnel mais recommandé)
Si vous n'avez pas encore d'environnement virtuel configuré, créez-en un dans le dossier racine :
```powershell
python -m venv .venv
```

### 2. Installer les dépendances
Installez l'ensemble des bibliothèques nécessaires à l'aide de `pip` :
```powershell
.venv\Scripts\pip install -r "Colab Notebooks/requirements.txt"
```

### 3. Lancer l'Application Localement
1. Démarrez le serveur Uvicorn avec rechargement automatique :
   ```powershell
   cd "Colab Notebooks"
   ..\.venv\Scripts\python -m uvicorn app:app --reload
   ```
2. Ouvrez l'interface dans votre navigateur à l'adresse suivante :
   👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🚀 Déploiement en Ligne (Render)

Le projet est configuré pour être déployé en quelques clics sur la plateforme **Render.com**.

### Préparer le dépôt
Assurez-vous que tous les fichiers récents ont été envoyés sur votre dépôt GitHub :
```bash
git add render.yaml "Colab Notebooks/"
git commit -m "Mise à jour du projet pour déploiement Render et gestion des causes d'échec"
git push origin main
```

### Méthode A : Déploiement via le Blueprint (Recommandé)
1. Connectez-vous sur votre compte **Render**.
2. Allez dans la section **Blueprints** et cliquez sur **New Blueprint Instance**.
3. Associez votre dépôt GitHub.
4. Render lira automatiquement le fichier `render.yaml` situé à la racine et se chargera d'orchestrer le build du conteneur en utilisant le dossier de contexte `Colab Notebooks`.
5. Cliquez sur **Apply**. Une fois le service *Live* (vert), cliquez sur l'URL fournie pour accéder à l'application.

### Méthode B : Déploiement Manuel
1. Cliquez sur **New** -> **Web Service**.
2. Connectez votre dépôt GitHub.
3. Donnez un nom au projet et configurez :
   - **Root Directory** : `Colab Notebooks`
   - **Runtime** : `Docker`
4. Cliquez sur **Deploy**.

---

## 🧠 Entraînement du Modèle

Si vous modifiez le jeu de données `Bank_transaction_scenario1.csv` ou si vous souhaitez réentraîner le modèle, lancez le script d'entraînement :
```powershell
cd "Colab Notebooks"
..\.venv\Scripts\python train_and_save_model.py
```
Cela mettra à jour automatiquement les fichiers `random_forest_model.pkl`, `scaler.pkl` et `features.json` pour qu'ils soient directement pris en compte par l'API de scoring au prochain démarrage.
