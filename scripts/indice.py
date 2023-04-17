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
    aire = dist**2

    # Récupération de la liste des points de A
    pointsA = A['geometry']
    # pointsA = gpd.GeoDataFrame(geometry=gpd.points_from_xy(A[:,0], A[:,1]))
    
    # Récupération de la liste des points de B
    pointsB = B['geometry']
    # pointsB = gpd.GeoDataFrame(geometry=gpd.points_from_xy(B[:,0], B[:,1]))
    
    # Calcule la distance entre les points les plus éloignés entre les deux GeoDataFrames
    """
    Attention : à verifier si la distance est faite entre les points du coupleA et ceux du coupleB 2 à 2, ou alors 
    c'est le max entre tous les points du coupleA et tous les points du coupleB
    --> Réponse : ok, distance entre tous les points
    """
    max_distance = pointsA.distance(pointsB).max()
    # A récupérer : l'indice des points A et B pour savoir entre quels points la distance est max
    print(max_distance)
    ind = dist_start * max_distance / aire
    
    return ind


if __name__ == "__main__":

    gdf= use_data.create_gdf('simulations_reel_gdf.csv')

    # Changement de la géométrie vers start
    gdf = gpd.GeoDataFrame(gdf, geometry=gdf['start'].map(wkt.loads),crs = 'EPSG:2154')

    # Récupération de 2 éléments
    A = gdf.iloc[[0]]
    B = gdf.iloc[[1]]

    # Calcul de la distance entre les 2 points de départ
    dist_start = dist_start(A, B)

    # Changement de la géométrie vers itineraire
    gdf = gpd.GeoDataFrame(gdf, geometry=gdf['itineraire'].map(wkt.loads),crs = 'EPSG:2154')

    # Récupération de 2 éléments
    A = gdf.iloc[[0]]
    B = gdf.iloc[[1]]

    # Calcul de l'indice
    ind = indice(A,B,dist_start,100)

    print(ind)