# Utiliser une image de base Python légère
FROM python:3.11-slim

# Définir des variables d'environnement pour optimiser Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le dossier de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système minimales nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source de l'application et les artefacts du modèle
COPY app.py .
COPY dashboard.html .
COPY features.json .
COPY random_forest_model.pkl .
COPY scaler.pkl .

# Commande pour démarrer le serveur de production Uvicorn en écoutant sur le port de Render ($PORT)
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
