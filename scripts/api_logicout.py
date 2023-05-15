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

def calcul_couts(traj,vehicule='VUL_12',v_type='GF',frigo=True,tps_moy='00:10:00',tps_act='00:00:00'):
    '''
        traj: Coordinates Array
        
        Takes an array of coordinates and create the json request for the Logicout API, then sends it and display the characteristics of 
    '''
    #NB : The defaults values are chosen to match the worst case possible, so the script will give a pessimistic answer, but it cannot be worse in reality.
    #Parsing the coordinates array to build the json
    etapes = []
    for point in traj:
        etapes.append( {"latitude": point[1], "longitude": point[0], "duree_livraison": tps_moy})
    #Building the json used for the request
    json_logicout = {
        'key': logicout_key,
        'id_vehicule': vehicule,
        'type_vul': v_type,
        'frigorifique': frigo,
        'duree_autres_activites': tps_act,
        'service': 'mapbox',
        'retour': True,
        'etapes': etapes,
        'itineraire_key': mapbox_key,
        'heure_depart': '01/01/2000 00:00'
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
    
    return(json_response)