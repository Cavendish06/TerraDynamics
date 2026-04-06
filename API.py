#Projet : TerraDynamics
#Auteurs : Baptiste Dieu, Macéo Mestrallet

"""
Ce module s'occupe d'effectuer les demandes API et le téléchargement de fichiers.
Il s'axe autour de deux librairies, Herbie, qui est un module python servant de client afin de télécharger des données météo mondiales, les données sont récupérées depuis des serveurs de stockage type AWS, et les fichiers sont au format GRIB2 (gridded binary), standard international pour les données météo, et openmeteo-API qui est une API open source dont le client est sous licence MIT.
Herbie est utilisé afin de récupérer les températures autour du globe, il a pour avantage de permettre de récupérer facilement un très grand ensemble de données (1 036 800 pts pour une résolution de 0,25°).
Open-meteo est utilisé afin de récupérer les coordonnées d'une ville ainsi que les données météo qui y sont liées.
"""
import herbie 
import numpy as np
import GUI_TerraDynamics
import requests
import openmeteo_requests
from requests_cache import CachedSession
from datetime import datetime, timezone


def conversion_lonHerbie(array): # Convertie le format longitude utilisé par grib2 qui est sur 160° en format classique de -180 à 180
    array = array.copy()
    array[array > 180] -= 360 #Applique un filtre ou "masque" à l'array (tableau) numpy
    return array


def dernier_run_disponible(heure): #Dû au temps de mise à)jour et la différence d'heure, il faut vérifier quand est le dernier log météo disponible
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    runs = [18, 12, 6, 0]
    
    for run in runs:
        heure=f"{run:02d}:00"
        try:
            H=herbie.Herbie( #Fonction intégré qui formule une requête à herbie pour un certain nombre de paramètre
                f"{date} {heure}",
                model="gfs",
                product="pgrb2.0p25",
                fxx=0,
                verbose=False
            )
            if H.grib is not None:
                return date, heure # Return :e dernier la date et l'heure du dernier log dispo; ol sont remis à jours tout les 6 heures
        except Exception: 
            continue
    raise ValueError("Aucun run GFS disponible aujourd'hui.")

def requete_monde(resolution, heure): #Effectue la requête afin de récupéré les températures autour du monde
    produit_map={ # Possibilité de résolution
        "0.25": "pgrb2.0p25",
        "0.5":  "pgrb2.0p50"
    }

    date_run, heure_run=dernier_run_disponible(heure)
    H=herbie.Herbie(f"{date_run} {heure_run}", model="gfs",product=produit_map[resolution], fxx=heure) #Requête monde 

    ds=H.xarray(r":TMP:2 m above") # Télécharge seulement les données intéressante du grib2 et les convertit stocke en dataset Xarray

    latsDs=ds["latitude"].values
    lonDs=ds["longitude"].values
    tempDs=ds["t2m"].values-273.15

    lats=np.copy(latsDs) #Effectue des copies numpy pouvoir modifier les tableaux
    lon=np.copy(lonDs)
    temp=np.copy(tempDs)

    lon=conversion_lonHerbie(lon)
    print(lats)
    lons_2d, lats_2d = np.meshgrid(lon, lats) #meshgrid prend deux tableaux 1D et crée deux grilles 2D. Chaque point de la grille a une latitude ET une longitude associée.

    lats_1d=lats_2d.ravel() #Déplie les tableaux en 1D
    lons_1d=lons_2d.ravel()

    grid_lat_lon=np.c_[lats_1d, lons_1d] #Créer un grlle 2D où chaque ligne à deux colonnes, une latitude et une longitude (total de 1 026 800 lignes pour 0.25° de reésolution). Numpy est donc la seuel option pour gérer une tel nombre d'éléments
    temp=temp.ravel()
    return grid_lat_lon, temp

def recherche_ville(ville): #Effectue une recherche des coordonnées d'une ville sur Terre via l'API geopoint d'open-meteo
    session=CachedSession(cache_name="cache/ville_specifique",expire_after=3600) #Mise en place d'une cached session les données récupéré sont donc stocké ici pendant 24 heures cela permet de ne pas utilisé de crédit API et d'obtenir les résultats bien plus ite si on refiat une requête.
    url="https://geocoding-api.open-meteo.com/v1/search"

    param1={"name": ville,
           "count": 1}

    reponse=session.get(url, params=param1)
    reponse_lisible=reponse.json()['results'] #Extraction json
    coordonne_ville=(reponse_lisible[0]["latitude"],reponse_lisible[0]["longitude"])

    return coordonne_ville

#Implémentation retry
def requete_ville(ville): #Effectue une requête afin d'obtenir les données météo relatifs à une ville
    coordonnee=recherche_ville(ville)
    session_cache=CachedSession(cache_name="cache/tempville",expire_after=1) #Lance une autre session aussi sous cache qui expire au bout d'une heure
    openmeteo=openmeteo_requests.Client(session=session_cache)

    url="https://api.open-meteo.com/v1/forecast"

    param={
        "latitude":coordonnee[0],
        "longitude":coordonnee[1],
        "current": ["temperature_2m","relative_humidity_2m","cloud_cover","wind_direction_10m","wind_speed_10m","precipitation","precipitation_probability","visibility"], # Récupère les données actuelles.
        "forecast_days": 1,
    }
    
    reponse=openmeteo.weather_api(url,params=param)
    current=reponse[0].Current()
    temperature=current.Variables(0).Value()
    donnees={
    "temperature":temperature,
    "humidite":current.Variables(1).Value(),
    "nuages":current.Variables(2).Value(),
    "vent_direction":current.Variables(3).Value(),
    "vent_vitesse":current.Variables(4).Value(),
    "precipitation":current.Variables(5).Value(),
    "proba_pluie":current.Variables(6).Value(),
    "visibilite":current.Variables(7).Value(),
    }
        
    grid_lat_lon= np.array([coordonnee[0],coordonnee[1]],ndmin=2)  # Convertie au bon format numpy pour effectuer des opérations dessus 

    return grid_lat_lon, temperature, donnees