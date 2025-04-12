# weather_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd

# Votre clé API Visual Crossing (remplacez par la vôtre)
API_KEY = "RDG2YTGFUCWZRC72JNDU37D8L"

def get_weather_for_year(city, year):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{year}-01-01/{year}-12-31?key={API_KEY}&include=days"
    
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
        df.to_csv(f"meteo_{city}_{year}.csv", index=False)
        print(f"✅ Données météo pour {city} en {year} enregistrées.")
    else:
        print(f"❌ Erreur avec l'API pour {city} en {year}: {response.status_code}")

# Définir les arguments par défaut pour le DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Créer le DAG
with DAG(
    'weather_dag',
    default_args=default_args,
    description='Récupérer les données météo pour une année donnée',
    schedule=timedelta(days=1),  # Exécution quotidienne
    start_date=datetime(2022, 1, 1),
    catchup=False,
) as dag:

    # Définir la tâche dans le DAG
    get_weather_task = PythonOperator(
        task_id='get_weather_for_year_task',
        python_callable=get_weather_for_year,
        op_args=["Paris", 2022],  # Arguments pour la fonction : ville et année
    )

    # Exécution de la tâche
    get_weather_task
