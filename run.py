import requests
import pandas as pd
import json
import time

# Lire les codes postaux à partir du fichier CSV de laposte
df = pd.read_csv('source/019HexaSmal.csv', delimiter=';')
codes_postaux = df['Code_postal'].tolist()

donnees_par_code_postal = {}

# URL de base du site
base_url = 'http://coco.gg/cocoland/{}.js'

# Parcourir la liste des codes postaux
for code_postal in codes_postaux:
    if code_postal in donnees_par_code_postal:
        print(f'Données pour le code postal {code_postal} déjà enregistrées.')
        continue

    url = base_url.format(code_postal)

    # Faire une requête GET au site
    response = requests.get(url)

    # Attendre entre les requêtes
    time.sleep(0.2)

    if response.status_code == 200:
        # Si la requête a réussi, extraire la valeur de cityco de la réponse
        donnees = response.content.decode('latin-1')
        cityco = donnees.split("var cityco='", 1)[-1].split('*')

        # Formatter les données comme demandé
        data = {}
        for i in range(0, len(cityco), 2):
            if i + 1 < len(cityco):
                data[cityco[i]] = cityco[i+1]

        donnees_par_code_postal[code_postal] = data

        # Enregistrer les données au fur et à mesure
        with open('out/city-code.json', 'w', encoding='utf-8') as fichier_json:
            json.dump(donnees_par_code_postal, fichier_json, ensure_ascii=False, indent=4)

        print(f'Données pour le code postal {code_postal} récupérées')

    else:
        print(f'Échec de la requête pour le code postal {code_postal}')

print("Terminé")
