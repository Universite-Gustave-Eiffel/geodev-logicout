import os
import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point, LineString, shape
import matplotlib as plt
import numpy as np
import folium
from shapely import wkt



def create_df(filename) :
    """
    Create geodataframes from the simulation files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """
   
    root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory
    dirname = "/data/raw/" # relative path to the gitignore directory - the function on the file _dataframes_gpd.py is adapted to find the relative path of this directory
    df = pd.read_csv(root +dirname+ filename,sep=';')
    geometry = df['cheflieu'].map(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs = 'EPSG:2154')
    return gdf






# Fonction qui renvoie la distance euclidienne entre 2 couples de points, définis de cette manière : 
# coupleA = [Xa,Ya]
# coupleB = [Xb,Yb]
def distance(coupleA,coupleB):
    dist = np.sqrt((float(coupleA[0])-float(coupleB[0]))**2 + (float(coupleA[1])-float(coupleB[1]))**2)


# Fonction qui renvoie l'indice créé entre 2 tournée A et B, en fonction de la distance du buffer choisie
def indice(A, B, dist):

    aire = dist**2

    startA = pd.A['start']
    startB = pd.B['start']
    
    # startA = A['itineraire'].apply(lambda x: Point(x.coords[0]))
    # startB = B['itineraire'].apply(lambda x: Point(x.coords[0]))
    # startA = [A[0][0],A[0][1]]
    # startB = [B[0][0],B[0][1]]

    dist_start = distance(startA,startB)
    
    # Récupération de la liste des points de A
    pointsA = A['itineaire']
    # pointsA = gpd.GeoDataFrame(geometry=gpd.points_from_xy(A[:,0], A[:,1]))
    
    # Récupération de la liste des points de B
    pointsB = B['itineaire']
    # pointsB = gpd.GeoDataFrame(geometry=gpd.points_from_xy(B[:,0], B[:,1]))
    
    # Calcule la distance entre les points les plus éloignés entre les deux GeoDataFrames
    """
    Attention : à verifier si la distance est faite entre les points du coupleA et ceux du coupleB 2 à 2, ou alors 
    c'est le max entre tous les points du coupleA et tous les points du coupleB
    """
    max_distance = pointsA.distance(pointsB).max()
    # A récupérer : l'indice des points A et B pour savoir entre quels points la distance est max

    ind = dist_start * max_distance / aire

    return ind


if __name__ == "__main__":


    gdf= create_df('simulations_reel_gdf.csv')

    # print(geo_df_envelop.crs)
    
    A = gdf.iloc[0]
    B = gdf.iloc[1]
    ind = indice(A,B,100)
    print(ind)