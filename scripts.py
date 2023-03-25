# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 17:23:54 2023

@author: fatou
"""
#pip install requests 
import requests

# Clé API JCDecaux
api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"

# URL de l'API JCDecaux pour les villes
url = f"https://api.jcdecaux.com/vls/v3/contracts?apiKey={api_key}"

# Récupération des données de l'API
response = requests.get(url)
contracts = response.json()

# Liste pour stocker les données des villes
cities_data = []

# Boucle sur les contrats pour récupérer les données de chaque ville
for contract in contracts:
    # URL de l'API JCDecaux pour les stations de la ville
    url = f"https://api.jcdecaux.com/vls/v3/stations?apiKey={api_key}&contract={contract['name']}"

    # Récupération des données de l'API
    response = requests.get(url)
    stations = response.json()

    # Initialisation des variables pour la ville en cours
    city_bikes = 0
    city_ebikes = 0

    # Boucle sur les stations de la ville pour calculer les pourcentages
    for station in stations:
        city_bikes += station['mainStands']['availabilities']['mechanicalBikes']
        city_ebikes += station['mainStands']['availabilities']['electricalBikes']

    # Calcul des pourcentages pour la ville en cours
    city_total = city_bikes + city_ebikes
    if city_total == 0:
        city_pct_bikes  = 0
        city_pct_ebikes  = 0
    else:
        city_pct_bikes = round((city_bikes / city_total) * 100, 2)
        city_pct_ebikes = round((city_ebikes / city_total) * 100, 2)

    # Ajout des données de la ville à la liste
    cities_data.append({'name': contract['name'], 'bikes': city_total, 'mechanical_pct': city_pct_bikes, 'electrical_pct': city_pct_ebikes})

# Tri de la liste par ordre décroissant du nombre total de vélos
cities_data.sort(key=lambda x: x['bikes'], reverse=True)

# Affichage des données des villes
for city in cities_data:
    print(f"{city['name']} a : {city['bikes']} vélos dont {city['mechanical_pct']}% de vélos mécaniques, {city['electrical_pct']}% de vélos électriques")
