import requests
import pandas as pd

# Votre clé API Visual Crossing (remplacez par la vôtre)
API_KEY = "CEML76NFE3T5CQBRQLEL5SCK3"

def get_weather_for_day(city, date):
    # Construire l'URL de l'API de Visual Crossing pour obtenir les données météo
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{date}?key={API_KEY}&include=days"
    
    # Effectuer la requête
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Extraire les informations météorologiques pour la journée donnée
        day_data = data.get('days', [])[0]  # Il y a une seule entrée par jour dans la réponse
        
        weather_info = {
            'Date': date,
            'Température (°C)': day_data['temp'],
            'Précipitations (mm)': day_data.get('precip', 0),  # Précipitations pour la journée
            'Humidité (%)': day_data['humidity'],
            'Vitesse du vent (km/h)': day_data['windspeed']
        }
        
        return weather_info
    else:
        print(f"❌ Erreur avec l'API pour {city} le {date}: {response.status_code}")
        return None

# Exemple d'appel de la fonction avec une ville et une date
city = "Paris"
date = "2022-01-01"

weather_data = get_weather_for_day(city, date)

if weather_data:
    # Sauvegarder dans un fichier CSV
    df = pd.DataFrame([weather_data])
    df.to_csv(f"meteo_{city}_{date}.csv", index=False)
    print(f"✅ Données météo pour {city} le {date} enregistrées.")
