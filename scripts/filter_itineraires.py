# Filtre les trajets selon un id utilisateur validé
import csv
import os

import numpy as np

def filterItineraire(simulations,users,trajets,arret):
    '''
    
    Filters the itineraires from the file "itineraire" based on the list of
    concerned users from the file users

    Args: 
        simulation (csv) : simulation's base
        users (csv) : user's base
        trajets (csv) : itineraire's base
        
        
    Return a list of valid itineraires
    
    '''
    path_users =  os.getcwd() + "/data/raw/" + users 
    path_simulation = os.getcwd() + "/data/raw/" + simulations 
    path_trajet = os.getcwd() + "/data/raw/" + trajets 
    path_arret=os.getcwd() + "/data/raw/" + arret 
    
    print(os.getcwd())

  
    users_valides = []
    simulations =[]
    out_simulations=[]
    arrets_filtres=[]
    
    with open(path_users, 'r') as file:
        lines = file.readlines()[1:]
        csvreader = csv.reader(lines, delimiter=',')
        for row in csvreader:
            if row[7]=='oui':
                users_valides.append(row[0])
    
    
        
    with open(path_simulation, 'r') as file: # create a list with the simulation id and the user id
            lines = file.readlines()[1:]
            csvreader = csv.reader(lines, delimiter=';')
            for row in csvreader:
                if row[2] in users_valides:
                    simulations.append(int(row[0]))

    print(len(users_valides))
    print(len(simulations))
    print('--------')
    print(type(simulations[0]))
    
    with open(path_trajet, 'r') as file:
        lines = file.readlines()[1:]
        csvreader = csv.reader(lines)
  
        for row in csvreader:
            if row[4]!="":
                if int(row[1]) in simulations:
                    if int(row[1]) not in out_simulations:
                        out_simulations.append(int(row[1]))


    with open(path_arret, 'r') as file:
        lines = file.readlines()[1:]
        csvreader = csv.reader(lines, delimiter=',',quoting=csv.QUOTE_NONNUMERIC)
        id_actuel=''   


        for row in csvreader:
            if int(row[1]) in out_simulations:
                if row[1]!=id_actuel:
                    arrets_filtres.append([
                        
                        
                        row[1],[[row[4],row[5]]]
                        
                        
                        ])
                        
                        
                    id_actuel=row[1]
                    
                else:
                    arrets_filtres[-1][-1].append([row[4],row[5]])
                    

    print('2222222222222')
    print(len(out_simulations))                 
    return arrets_filtres


itineraire = filterItineraire("simulation.csv","utilisateur_nettoye.csv","trajet.csv","point_arret.csv")

def record_itineraires(filename):
    """
    function to record the valid itineraires into an CSV file
    
    
    Args:
        fiename
    """
    path='data/raw/'+filename
    with open(path,mode='w') as output:
        writer = csv.writer(output,delimiter=';')
        for i in range(len(itineraire)):
            writer.writerow(itineraire[i])
        

print(itineraire[0])
