import requests

def get_jours_feries():
    response = requests.get(f"https://date.nager.at/Api/v2/PublicHolidays/{2024}/{'FR'}")
    print(f"Code statut HTTP : {response.status_code}")  # Vérifiez le code de statut HTTP
    print(f"Contenu de la réponse : {response.text}")  # Affichez le contenu brut de la réponse
    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except ValueError as e:
            print(f"Erreur lors de l'analyse JSON: {e}")
    else:
        print(f"Erreur HTTP : {response.status_code}")
    return None
