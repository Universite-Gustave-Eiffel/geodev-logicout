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



# Fonction qui renvoie la distance euclidienne entre 2 couples de points, définis de cette manière : 
# coupleA = [Xa,Ya]
# coupleB = [Xb,Yb]
def distance(coupleA,coupleB):
    dist = np.sqrt((float(coupleA[0])-float(coupleB[0]))**2 + (float(coupleA[1])-float(coupleB[1]))**2)


# Fonction qui renvoie l'indice créé entre 2 tournée A et B, en fonction de la distance du buffer choisie
def indice(A, B, dist):

    aire = dist**2
 
    A_df = gpd.GeoDataFrame(A, geometry=A['geometry'], crs = 'EPSG:2154')
    B_df = gpd.GeoDataFrame(B, geometry=B['geometry'].map(wkt.loads), crs = 'EPSG:2154')

    startA = [A_df['start'],A_df['start']]
    startB = [B_df['start'],B_df['start']]

    dist_start = distance(startA,startB)
    
    # Récupération de la liste des points de A
    pointsA = A_df['itineaire']
    # pointsA = gpd.GeoDataFrame(geometry=gpd.points_from_xy(A[:,0], A[:,1]))
    
    # Récupération de la liste des points de B
    pointsB = B_df['itineaire']
    # pointsB = gpd.GeoDataFrame(geometry=gpd.points_from_xy(B[:,0], B[:,1]))
    
    # Calcule la distance entre les points les plus éloignés entre les deux GeoDataFrames
    """
    Attention : à verifier si la distance est faite entre les points du coupleA et ceux du coupleB 2 à 2, ou alors 
    c'est le max entre tous les points du coupleA et tous les points du coupleB
    --> Réponse : ok, distance entre tous les points
    """
    max_distance = pointsA.distance(pointsB).max()
    # A récupérer : l'indice des points A et B pour savoir entre quels points la distance est max

    ind = dist_start * max_distance / aire

    return ind


if __name__ == "__main__":

    gdf= use_data.create_gdf('simulations_reel_gdf.csv')
    # gdf = gpd.GeoDataFrame(gdf, geometry=gdf['start'].map(wkt.loads),crs = 'EPSG:2154')

    A = gdf.iloc[0]
    geometryA = A['cheflieu'].map(wkt.loads)
    A = gpd.GeoDataFrame(A, geometry=geometryA, crs = 'EPSG:2154')
    B = gdf.iloc[1]

    print(type(A['start']))
    print('---------------------')
    print(A)
    print('---------------------')

    

    ind = indice(A,B,100)
    print(ind)