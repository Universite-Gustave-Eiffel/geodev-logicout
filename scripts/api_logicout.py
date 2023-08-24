import json
import requests
from dotenv import load_dotenv
from dotenv import dotenv_values
import os
import logging
from datetime import date

#Setting up the logfile to keep track of the requests
logging.basicConfig(filename='log.txt', level=logging.INFO)

#Retrieving the keys from the .env file
#dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
keys = dotenv_values(".env")

def calcul_couts(traj,vehicule='VUL_12',v_type='GF',frigo=True,tps_moy='00:10:00',tps_act='00:00:00'):
    '''
        traj: Coordinates Array
        
        Takes an array of coordinates and create the json request for the Logicout API, then sends it and display the characteristics of 
    '''

    if keys: # check if API keys are available

        #NB : The defaults values are chosen to match the worst case possible, so the script will give a pessimistic answer, but it cannot be worse in reality.
        #Parsing the coordinates array to build the json
        etapes = []
        for point in traj:
            etapes.append( {"latitude": point[1], 
                            "longitude": point[0], 
                            "duree_livraison": tps_moy})
        #Building the json used for the request
        json_logicout = {
            'key': keys['LOGICOUT_KEY'],
            'id_vehicule': vehicule,
            'type_vul': v_type,
            'frigorifique': frigo,
            'duree_autres_activites': tps_act,
            'service': 'mapbox',
            'retour': True,
            'etapes': etapes,
            'itineraire_key': keys['MAPBOX_SECRET_KEY'],
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

    else:
        print("API keys not available")
        logging.info(str(date.today())+ ' API keys not available')
        return()

   
    return(json_response)