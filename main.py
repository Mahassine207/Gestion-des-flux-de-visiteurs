import os
import pandas as pd
from meteo import get_weather_for_year
from jours_feries import get_jours_feries
from config import OPENWEATHER_API_KEY

VILLE = "Paris"
ANNEE = 2022
CSV_METEO = f"data/meteo_{VILLE.lower()}_{ANNEE}.csv"
CSV_JOURS_FERIES = "data/jours_feries.csv"

os.makedirs("data", exist_ok=True)

# Récupération et sauvegarde des données météo
try:
    success = get_weather_for_year(VILLE, ANNEE, OPENWEATHER_API_KEY, CSV_METEO)
    if success:
        print("✅ Données météo enregistrées.")
    else:
        print("❌ Échec de la récupération des données météo.")
except Exception as e:
    print(f"❌ Une erreur est survenue lors de la récupération des données météo : {e}")

# Vérification si le fichier météo a bien été créé
if os.path.exists(CSV_METEO):
    print(f"✅ Le fichier météo {CSV_METEO} existe.")
else:
    print(f"❌ Le fichier météo {CSV_METEO} n'a pas été créé.")

# Récupération et sauvegarde des jours fériés
try:
    jours_feries = get_jours_feries()
    if jours_feries:
        pd.DataFrame(jours_feries).to_csv(CSV_JOURS_FERIES, index=False)
        print("✅ Données des jours fériés enregistrées.")
    else:
        print("❌ Aucune donnée de jours fériés récupérée.")
except Exception as e:
    print(f"❌ Une erreur est survenue lors de la récupération des jours fériés : {e}")

# Vérification si le fichier des jours fériés a bien été créé
if os.path.exists(CSV_JOURS_FERIES):
    print(f"✅ Le fichier des jours fériés {CSV_JOURS_FERIES} existe.")
else:
    print(f"❌ Le fichier des jours fériés {CSV_JOURS_FERIES} n'a pas été créé.")

print("✅ Toutes les données ont été collectées et enregistrées.")
