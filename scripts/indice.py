import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString, shape
import matplotlib as plt
import numpy as np
from shapely import wkt
import use_data 


def dist_start(A, B):
    """ 
    Cette fonction permet de calculer la distance entre les points de départ des tournées A et B
    Input : A, B (geodataframe) : geodataframe des 2 tournées A et B
    Output : dist_start (numpy.float64) : distance entre les 2 points de départ des tournées A et B.
    """

    startA = [A['geometry'].x.values[0],A['geometry'].y.values[0]]
    startB = [B['geometry'].x.values[0],B['geometry'].y.values[0]]

    dist_start = np.sqrt((startA[0] - startB[0])**2 + (startA[1] - startB[1])**2)

    return dist_start


def indice(A,B,dist_start,buffer):
    """ 
    Cette fonction permet de calculer l'indice des distances pour l'algorithme de mutualisation
    Input : A, B (geodataframe) : geodataframe des 2 tournées A et B
            dist_start (numpy.float64) : distance entre les 2 points de départs des 2 tournées A et B en mètres
            buffer (float) : distance en mètres du rayon du buffer
    Output : indice (numpy.float64) : l'indice des distances
    """

    # Calcul de la distance (100km) au carré
    aire = np.pi*buffer**2

    # Récupération de la liste des points de A
    linestringA = A['geometry']
    
    # Récupération de la liste des points de B
    linestringB = B['geometry']
    
    # On découpe le linestring en plusieurs points
    
    pointsA = linestringA.apply(use_data.line_to_points).explode()
    pointsB = linestringB.apply(use_data.line_to_points).explode()
    print(type(pointsA))
    """
    print('--------------------')
    print('Points de A : ')
    print(pointsA)
    print('--------------------')
    print('Points de B : ')
    print(pointsB)
    """
    # Calcule la distance entre les points les plus éloignés entre les deux GeoDataFrames
    """
    Attention : à verifier si la distance est faite entre les points du coupleA et ceux du coupleB 2 à 2, ou alors 
    c'est le max entre tous les points du coupleA et tous les points du coupleB
    --> Réponse : ok, distance entre tous les points
    """
    C = []
    for p1 in pointsA:
        for p2 in pointsB:
            dist = p1.distance(p2)
            C.append(dist)

    # On récupère la distance la plus grande dans le tableau
    max_distance = max(C)
    """
    print('--------------------')
    print("dist_start : ",dist_start)
    print("max_distance : ",max_distance)
    print("aire : ",aire)
    print('--------------------')
    """
    # On calcule l'indice avec la formule suivante :
    ind = dist_start * max_distance / aire

    return ind

def ind_calc(A,gdf,buffer):

    # Récupération du nombre de ligne dans le gdf
    nb_lines = gdf.count()[0]

    # Création des 2 géométries
    # geometry = gdf['start'].map(wkt.loads)
    gdf1 = gpd.GeoDataFrame(gdf, geometry=gdf['start'].map(wkt.loads), crs = 'EPSG:2154')
    # geometry = gdf['itineraire'].map(wkt.loads)
    gdf2 = gpd.GeoDataFrame(gdf, geometry=gdf['itineraire'].map(wkt.loads), crs = 'EPSG:2154')
    All_ind = []
    for i in range(nb_lines):
        dist = dist_start(A,gdf1.iloc[[i]])
        ind = indice(A,gdf2.iloc[[i]],dist,buffer)
        print('dist_start : ', dist)
        print('indice : ', ind)
        All_ind.append(ind)

    return All_ind


    

if __name__ == "__main__":

    
    # gdf= use_data.create_gdf('simulations_reel_gdf.csv')

    # Numéro des lignes des 2 tournées choisies dans le geodataframe
    pos1 = 0
    pos2 = 58
    
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
    
    print(A['id_simulation'].values[0])
    # Application de la fonction ind_calc sur toutes les données
    # All_ind = ind_calc(A,gdf1,100000)
    # print(All_ind)