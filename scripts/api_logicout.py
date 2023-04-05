import json
import requests

with open('data/raw/keys.txt') as f:
    lines = f.readlines()

logicout_key = lines[3][9:]
mapbox_key = lines[0][7:]
google_key =lines[1][6:]

def calcul_couts(traj):
    '''
        traj: Coordinates Array
        
        Takes an array of coordinates and create the json request for the Logicout API, then sends it and display the characteristics of 
    '''
    etapes = []
    for point in traj:
        etapes.append( {"longitude": point[0], "latitude": point[1], "duree_livraison": "00:10:00"})
    print(etapes)
    json_logicout = {
        'key': logicout_key,
        'id_vehicule': 'VUL_12',
        'type_vul': 'GF',
        'frigorifique': True,
        'duree_conduite': '01:00:00',
        'duree_livraison': '00:30:00',
        'duree_autres_activites': '01:30:00',
        'heure_depart': '15/03/2025 15:48',
        'service': 'mapbox',
        'retour': False,
        'etapes': etapes,
        "itineraire_key": mapbox_key
    }

    data = json.dumps(json_logicout)

    r = requests.post(
        "https://www.logicout.fr/couts/api/calcul_parcours_detaille/",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    json_response = r.json()
    print(json_response)
    
        
test = ["48.8566,2.3522" , "51.5074,-0.1278" , "46.5468,1.6639"]
calcul_couts(test)