#tests de libraries et export de shapefile

import numpy
import csv
from geopy import distance



def geodesic_dist(l1,p1,l2,p2):
    return distance.distance((p1,l1),(p2,l2))



p1 = (3.0575,50.63194)
p2 = (-3.98583,48.72667)
print(geodesic_dist(p1[0],p1[1],p2[0],p2[1]))

rows = []
with open("data/raw/point_arret.csv", 'r') as file:
    lines = file.readlines()[1:]
    csvreader = csv.reader(lines, delimiter=',',quoting=csv.QUOTE_NONNUMERIC)
    for row in csvreader:
        
        rows.append(row)

new_csv=[]
id_actuel=''
for row in rows:
    if row[1]!=id_actuel:
        new_csv.append([
            
            
            row[1],row[2],row[3],[[row[4],row[5]]]
            
            
            ])
            
            
        id_actuel=row[1]
        
    else:
        new_csv[-1][3].append([row[4],row[5]])
        
print(new_csv[2])



print(new_csv[0])


import shapefile

def polyligne_file(nom_fichier, rows):
    path = nom_fichier
    with shapefile.Writer(path, shapefile.POLYLINE) as shp:
        shp.field('id_simulation','C','40') 
      
        print(new_csv[0][3])
        
        
        for row in rows:
            shp.line([
                row[3]
                ])


            shp.record(row[0])

  
  
    
polyligne_file("data/raw/shp/test3.shp",new_csv)