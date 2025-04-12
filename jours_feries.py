# jours_feries.py
import requests

def get_jours_feries(pays="FR", annee=2024):
    API_KEY = 'dOZQuLUGgh5FUPHbkvf5WUpeozQMwLZ8'
    URL = f"https://calendarific.com/api/v2/holidays"
    
    params = {
        'api_key': API_KEY,
        'country': pays,
        'year': annee
    }

    response = requests.get(URL, params=params)
    
    if response.status_code != 200:
        print(f"❌ Erreur lors de la requête. Code de statut: {response.status_code}")
        print(f"Réponse brute : {response.text}")
        return []

    data = response.json()
    
    # Extraire les jours fériés
    jours_feries_list = []
    for holiday in data['response']['holidays']:
        jours_feries_list.append({
            "Date": holiday["date"]["iso"],
            "Nom": holiday["name"]
        })

    return jours_feries_list
