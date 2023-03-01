import numpy as np
import csv


# Fichier point_arret.csv sous forme d'Array (en retirant l'entête)
link = './data/raw/point_arret.csv'
data = np.genfromtxt(link, delimiter=',')[1:,:]

# Enregistrer, dans un csv, toutes les coordonnées des points d'arrêts par trajet (i.e. par id_simulation) 
id_simulation = np.unique(data[:,1])

# Création et ouverture du fichier en mode écriture
with open('data/steps.csv', mode='w') as csvFile:
    # Créer un objet writer
    writer = csv.writer(csvFile, delimiter=',')

    for id in id_simulation :
        i = 0
        for step in data:
            if step[1] == id :
                if i==0 :
                    trip = np.array([[step[-2], step[-1]]])
                    i += 1
                else:
                    trip = np.append(trip, [np.array([step[-2], step[-1]])], axis=0)
        writer.writerow([id, trip])

csvFile.close()

