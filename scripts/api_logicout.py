import json
import requests


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
        'key': 'fb885e9a-50a6-4bc3-9a67-0c1560eb2927',
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
        "itineraire_key": "sk.eyJ1IjoiY2xvdmlzLWJlcmdlcmV0IiwiYSI6ImNsZnRlMGUyOTAwMDIzZm9hcWs2ZHdraTQifQ.F1gVE8c5d8Xn_47QYgQ2QA"
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