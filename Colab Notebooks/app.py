import os
import json
import joblib
import pandas as pd
from datetime import datetime
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# Initialisation FastAPI
app = FastAPI(
    title="API Détecteur de Fraude Bancaire",
    description="API de scoring en temps réel utilisant le modèle Random Forest entraîné sur Colab.",
    version="1.0.0"
)

# Configuration CORS pour autoriser l'accès depuis l'interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement des artefacts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "random_forest_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
META_PATH = os.path.join(BASE_DIR, "features.json")

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    with open(META_PATH, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    print("Modèle, Scaler et Métadonnées chargés avec succès !")
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement des artefacts : {e}")

FEATURE_COLUMNS = metadata["feature_columns"]
CATEGORIES = metadata["categories"]

# Modèle de données d'entrée pour la transaction
class TransactionInput(BaseModel):
    id_client: str = Field(..., description="ID unique du client")
    numero_compte: float = Field(..., alias="Numero de compte", description="Numéro de compte du client")
    type_transaction: Literal["ATM", "Paiement en ligne", "Paiement électronique"] = Field(..., alias="Type de transaction")
    status_operation: Literal["Validé", "Echoué"] = Field(..., alias="Status operation")
    localisation: str = Field(..., description="Ville de transaction")
    date: datetime = Field(..., description="Date et heure de transaction, format ISO (ex: 2025-02-10T22:20:00)")
    montant: float = Field(..., alias="Montant", description="Montant de la transaction en FCFA")

    class Config:
        populate_by_name = True

# Response Model
class PredictionResponse(BaseModel):
    classe_predite: str
    confiance: float
    probabilites: dict
    niveau_risque: str
    alerte: bool

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": "RandomForestClassifier",
        "train_accuracy": metadata.get("train_accuracy"),
        "test_accuracy": metadata.get("test_accuracy")
    }

@app.get("/metadata")
def get_metadata():
    return {
        "categories": CATEGORIES
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(tx: TransactionInput):
    try:
        # 1. Préparation des variables de base
        # Conversion de la date pour extraire DayOfWeek et Month
        day_of_week = tx.date.weekday() # Lundi=0, Dimanche=6
        month = tx.date.month

        # Dictionnaire initial des caractéristiques
        features = {
            "Numero de compte": tx.numero_compte,
            "Montant": tx.montant,
            "DayOfWeek": day_of_week,
            "Month": month
        }

        # 2. Encodage One-Hot manuel dynamique
        # Nous initialisons tous les colonnes one-hot à 0
        for col in FEATURE_COLUMNS:
            if col not in features:
                features[col] = 0

        # Mettre à 1 les colonnes correspondantes aux valeurs d'entrée
        # Type de transaction
        type_col = f"Type de transaction_{tx.type_transaction}"
        if type_col in features:
            features[type_col] = 1

        # Status operation
        status_col = f"Status operation_{tx.status_operation}"
        if status_col in features:
            features[status_col] = 1

        # Localisation
        loc_col = f"Localisation_{tx.localisation}"
        if loc_col in features:
            features[loc_col] = 1

        # Création du DataFrame dans le bon ordre de colonnes
        df_pred = pd.DataFrame([features])
        df_pred = df_pred[FEATURE_COLUMNS]

        # 3. Normalisation (Mise à l'échelle)
        X_scaled = scaler.transform(df_pred)

        # 4. Prédiction
        pred_code = int(model.predict(X_scaled)[0])
        pred_proba = model.predict_proba(X_scaled)[0]

        # Mapping des classes
        classes_map = {0: "Normal", 1: "Suspect"}
        classe_predite = classes_map.get(pred_code, "Inconnu")
        
        probabilites = {
            "Normal": float(pred_proba[0]),
            "Suspect": float(pred_proba[1])
        }

        confiance = float(pred_proba[pred_code])
        p_suspect = float(pred_proba[1])

        # Niveaux de risque
        if p_suspect >= 0.7:
            niveau_risque = "ÉLEVÉ"
            alerte = True
        elif p_suspect >= 0.3:
            niveau_risque = "MOYEN"
            alerte = True
        else:
            niveau_risque = "FAIBLE"
            alerte = False

        return PredictionResponse(
            classe_predite=classe_predite,
            confiance=confiance,
            probabilites=probabilites,
            niveau_risque=niveau_risque,
            alerte=alerte
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la prédiction : {e}")

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    dashboard_path = os.path.join(BASE_DIR, "dashboard.html")
    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    raise HTTPException(status_code=404, detail="dashboard.html non trouvé")
