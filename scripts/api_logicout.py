import json
import requests
from dotenv import load_dotenv
import os
import logging
from datetime import date

#Setting up the logfile to keep track of the requests
logging.basicConfig(filename='log.txt', level=logging.INFO)
#Retrieving the keys from the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)
logicout_key = os.getenv('LOGICOUT_KEY')
gmaps_key = os.getenv('GMAPS_KEY')
mapbox_key = os.getenv('MAPBOX_SECRET_KEY')

def calcul_couts(traj):
    '''
        traj: Coordinates Array
        
        Takes an array of coordinates and create the json request for the Logicout API, then sends it and display the characteristics of 
    '''
    #Parsing the coordinates array to build the json
    etapes = []
    for point in traj:
        etapes.append( {"latitude": point[0], "longitude": point[1], "duree_livraison": "00:10:00"})
    print(etapes)
    #Building the json used for the request
    json_logicout = {
        'key': logicout_key,
        'id_vehicule': 'VUL_12',
        'type_vul': 'GF',
        'frigorifique': True,
        'duree_autres_activites': '01:30:00',
        'heure_depart': '15/03/2025 15:48',
        'service': 'mapbox',
        'retour': False,
        'etapes': etapes,
        "itineraire_key": mapbox_key
    }

    data = json.dumps(json_logicout)
    #Sending the json to the API
    r = requests.post(
        "https://www.logicout.fr/couts/api/calcul_parcours_detaille/",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    json_response = r.json()
    #Printing
    #print(json_response)
    logging.info(str(date.today())+str(json_response))
    
        
test = [(48.8566,2.3522), (46.5468,1.6639)]
calcul_couts(test)