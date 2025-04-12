import requests
import pandas as pd

def get_weather_for_year(city, year, api_key, output_csv):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{year}-01-01/{year}-12-31?key={api_key}&include=days"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        all_data = []
        for day_data in data['days']:
            precipitations = day_data.get('precip', 0)
            precip_status = "Oui" if precipitations > 0 else "Non"

            weather_info = {
                'Date': day_data['datetime'],
                'Température (°C)': day_data['temp'],
                'Précipitations (mm)': precipitations,
                'Humidité (%)': day_data['humidity'],
                'Vitesse du vent (km/h)': day_data['windspeed'],
                'Précipitation (Oui/Non)': precip_status
            }
            all_data.append(weather_info)

        df = pd.DataFrame(all_data)
        df.to_csv(output_csv, index=False)
        print(f"✅ Données météo pour {city} en {year} enregistrées.")
        return True
    else:
        print(f"❌ Erreur avec l'API pour {city} en {year}: {response.status_code}")
        return False
