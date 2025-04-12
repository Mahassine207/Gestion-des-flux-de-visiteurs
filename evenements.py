from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Configuration améliorée du navigateur
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
# options.add_argument("--headless")  # Décommentez après test

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Masquer l'automation
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """
})

# Accès à la page
driver.get("https://www.eventbrite.com/d/france--paris/all-events/")

# Gestion des cookies
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept') or contains(., 'Accepter')]"))
    ).click()
except:
    pass

# Scroll pour charger les événements
last_height = driver.execute_script("return document.body.scrollHeight")
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Nouvelle approche d'extraction
events = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'event-card')]"))
)

event_data = []

for event in events:
    try:
        title = event.find_element(By.XPATH, ".//h2 | .//h3").text.strip()
        date = event.find_element(By.XPATH, ".//p[contains(., '•') or contains(@class, 'date')]").text.strip()
        link = event.find_element(By.XPATH, ".//a[contains(@href, '/e/')]").get_attribute("href").split('?')[0]
        
        if title and date and link:
            event_data.append({
                "Nom": title,
                "Date": date,
                "Lien": link
            })
    except:
        continue

# Nettoyage des données
if event_data:
    df = pd.DataFrame(event_data).drop_duplicates(subset=['Lien'])
    df.to_csv("data/events_paris.csv", index=False, encoding='utf-8-sig')
    
    # Affichage amélioré
    print(f"\n{' ÉVÉNEMENTS PARISIENS ':=^80}")
    for idx, row in df.iterrows():
        print(f"\n▶ {row['Nom']}")
        print(f"⏰ {row['Date']}")
        print(f"🔗 {row['Lien']}")
        print("-"*80)
    print(f"\n{len(df)} événements trouvés et sauvegardés.")
else:
    print("Aucun événement trouvé - Vérifiez les sélecteurs ou le chargement de la page.")
    driver.save_screenshot("debug.png")
    print("Capture d'écran sauvegardée (debug.png)")

driver.quit()