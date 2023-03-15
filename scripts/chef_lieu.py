import numpy as np
import csv

file = './data/raw/CHFLIEU_COMMUNE.csv'
data = []
with open(file,newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data.append(row)

chef_lieu = []
# On récupère lat lon de chaque chef_lieu
for i in range(len(data)):
    chef_lieu.append([data[i][3],data[i][4]])
print(chef_lieu)


def isin(ferme,chef_lieu,commune):
    coord_chef_lieu = []
    # On parcout toutes les communes
    for i in range(len(commune)):
        # Condition pour savoir si la ferme est dans la commune
        if(np.isin(ferme,commune[i])):
            # Récupérer les coordonnées du chef_lieu de la commune
            coord_chef_lieu.append(chef_lieu[i][0],chef_lieu[i][1])
    
    return coord_chef_lieu
