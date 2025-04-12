import subprocess
import time

# Définir l'intervalle d'exécution en secondes (par exemple, toutes les 24 heures)
interval = 86400  # 86400 secondes = 24 heures

def run_scraper():
    # Exécuter le script evenements.py
    subprocess.run(['python', 'evenements.py'], check=True)

if __name__ == "__main__":
    while True:
        run_scraper()
        print(f"Script exécuté à {time.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(interval)  # Attendre 24 heures avant d'exécuter à nouveau
