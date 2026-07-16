import pandas as pd
import numpy as np
import joblib
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Chemins des fichiers
base_dir = r"c:\Users\PC\Downloads\Colab Notebooks-20260714T164202Z-1-001\Colab Notebooks"
csv_path = os.path.join(base_dir, "Bank_transaction_scenario1.csv")

print("Chargement des données...")
df = pd.read_csv(csv_path)

# Division de la colonne combinée (séparée par des point-virgules)
print("Prétraitement et nettoyage...")
df_split = df['ID Clients;Numero de compte;Identifiant operation;Type de transaction;Status operation;Localisation;Date;Montant;Target'].str.split(';', expand=True)
df_split.columns = ['ID Clients', 'Numero de compte', 'Identifiant operation', 'Type de transaction', 'Status operation', 'Localisation', 'Date', 'Montant', 'Target']
df = df_split.copy()

# Conversion des types
df['Numero de compte'] = pd.to_numeric(df['Numero de compte'], errors='coerce')
df['Montant'] = pd.to_numeric(df['Montant'], errors='coerce')

# Encodage de la cible : Normal=0, Suspect=1, le reste (Fraude) devient NaN et sera supprimé
df['Target'] = df['Target'].map({'Normal': 0, 'Suspect': 1})

# Extraction des caractéristiques temporelles de la Date
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['DayOfWeek'] = df['Date'].dt.dayofweek
df['Month'] = df['Date'].dt.month

# Suppression des colonnes inutiles
df = df.drop(columns=['Date', 'ID Clients', 'Identifiant operation'])

# Suppression des lignes avec des valeurs manquantes (notamment la cible 'Fraude' devenue NaN)
df = df.dropna()

print(f"Nombre de lignes pour l'entraînement : {len(df)}")
print(f"Distribution des classes cibles :\n{df['Target'].value_counts()}")

# Encodage One-Hot des caractéristiques catégorielles
categorical_cols = ['Type de transaction', 'Status operation', 'Localisation']

# On extrait les catégories uniques avant l'encodage pour les sauvegarder dans les métadonnées
metadata_categories = {col: sorted(df[col].astype(str).unique().tolist()) for col in categorical_cols}

df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Séparation des caractéristiques et de la cible
X = df_encoded.drop('Target', axis=1)
y = df_encoded['Target']

# Sauvegarder l'ordre et le nom exact des colonnes attendues par le modèle
feature_columns = X.columns.tolist()

# Séparation train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Mise à l'échelle des caractéristiques...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Entraînement du modèle Random Forest...")
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train_scaled, y_train)

# Évaluation rapide
train_acc = rf_model.score(X_train_scaled, y_train)
test_acc = rf_model.score(X_test_scaled, y_test)
print(f"Exactitude sur le Train : {train_acc:.4f}")
print(f"Exactitude sur le Test : {test_acc:.4f}")

# Sauvegarde des objets
model_path = os.path.join(base_dir, "random_forest_model.pkl")
scaler_path = os.path.join(base_dir, "scaler.pkl")
meta_path = os.path.join(base_dir, "features.json")

print(f"Sauvegarde du modèle dans {model_path}...")
joblib.dump(rf_model, model_path)

print(f"Sauvegarde du scaler dans {scaler_path}...")
joblib.dump(scaler, scaler_path)

# Enregistrement des métadonnées des colonnes pour aligner l'API lors de l'inférence
metadata = {
    "feature_columns": feature_columns,
    "categories": metadata_categories,
    "train_accuracy": float(train_acc),
    "test_accuracy": float(test_acc)
}
print(f"Sauvegarde des métadonnées dans {meta_path}...")
with open(meta_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("Entraînement et sauvegarde terminés avec succès !")
