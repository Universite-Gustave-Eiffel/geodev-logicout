import numpy
import csv
from shapely import geometry



from geopy import distance



def geodesic_dist(l1,p1,l2,p2):
    return distance.distance((p1,l1),(p2,l2))



p1 = (3.0575,50.63194)
p2 = (-3.98583,48.72667)
print(geodesic_dist(p1[0],p1[1],p2[0],p2[1]))

rows = []
with open("data/raw/point_arret.csv", 'r') as file:
    csvreader = csv.reader(file, delimiter=',')
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)
print(header)

new_csv=[]
id_actuel=''
for row in rows:
    if row[1]!=id_actuel:
        new_csv.append([
            
            
            row[1],row[2],row[3],[(row[4],row[5])]
            
            
            ])
            
            
        id_actuel=row[1]
        
    else:
        new_csv[-1][3].append((row[4],row[5]))
        
print(new_csv[2])

