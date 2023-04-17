import os
import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point, LineString, shape
import matplotlib as plt
import numpy as np
import folium
from shapely import wkt
import use_data 


# Fonction qui renvoie l'indice créé entre 2 tournée A et B, en fonction de la distance du buffer choisie
def dist_start(A, B):
    
    startA = [A['geometry'].x.values[0],A['geometry'].y.values[0]]
    startB = [B['geometry'].x.values[0],B['geometry'].y.values[0]]

    dist_start = np.sqrt((startA[0] - startB[0])**2 + (startA[1] - startB[1])**2)

    return dist_start


def indice(A,B,dist_start,dist):

    # Calcul de la distance (100km) au carré
    aire = np.pi*dist**2

    # Récupération de la liste des points de A
    linestringA = A['geometry']
    # pointsA = gpd.GeoDataFrame(geometry=gpd.points_from_xy(A[:,0], A[:,1]))
    
    # Récupération de la liste des points de B
    linestringB = B['geometry']
    # pointsB = gpd.GeoDataFrame(geometry=gpd.points_from_xy(B[:,0], B[:,1]))
    
    # Calcule la distance entre les points les plus éloignés entre les deux GeoDataFrames
    """
    Attention : à verifier si la distance est faite entre les points du coupleA et ceux du coupleB 2 à 2, ou alors 
    c'est le max entre tous les points du coupleA et tous les points du coupleB
    --> Réponse : ok, distance entre tous les points
    """
    print('--------------------')
    print('Points de A : ')
    print(linestringA)
    print('--------------------')
    print('Points de B : ')
    print(linestringB)
    print('--------------------')
    
    # Découpe de la linestring en liste de points
    def line_to_points(line):
        return [Point(xy) for xy in line.coords]

    # Appliquer la fonction à chaque ligne de la GeoSeries
    pointsA = linestringA.apply(line_to_points).explode()
    pointsB = linestringB.apply(line_to_points).explode()
    
    max_distance = 0
    for p1 in pointsA:
        for p2 in pointsB:
            dist = p1.distance(p2)
            if(dist>max_distance):
                max_distance = dist

    print('--------------------')
    print("Dist_start : ")
    print(dist_start)
    print("max_distance : ")
    print(max_distance)
    print("aire : ")
    print(aire)
    print('--------------------')
    
   
    # Récupération du maximum des distances
    
    # max_distance = distance_entre_points.max()

    # Indice calculé
    ind = dist_start * max_distance / aire
    
    return ind


if __name__ == "__main__":

    # gdf= use_data.create_gdf('simulations_reel_gdf.csv')

    pos1 = 821
    pos2 = 57

    # Changement de la géométrie vers start
    gdf1 = use_data.create_gdf('simulations_reel_gdf.csv', 'start')

    # Récupération de 2 éléments
    A = gdf1.iloc[[pos1]]
    B = gdf1.iloc[[pos2]]

    # Calcul de la distance entre les 2 points de départ
    dist_start = dist_start(A, B)

    # Changement de la géométrie vers itineraire
    gdf2 = use_data.create_gdf('simulations_reel_gdf.csv', 'itineraire')

    # Récupération de 2 éléments
    A = gdf2.iloc[[pos1]]
    B = gdf2.iloc[[pos2]]

    # Calcul de l'indice
    ind = indice(A,B,dist_start,100000)
    print(ind)