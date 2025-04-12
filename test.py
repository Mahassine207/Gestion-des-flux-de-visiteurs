import requests

city = "Paris"
api_key = "f2c6dd296b431f62373fef3a49eddbb9"  # Remplacez par votre clé API valide

url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)

if response.status_code == 200:
    print("✅ Réponse de l'API :", response.json())
else:
    print(f"❌ Erreur {response.status_code}: Clé API non valide ou problème d'authentification.")