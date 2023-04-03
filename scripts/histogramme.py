import numpy as np
import matplotlib as plt
import os
import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point, LineString, shape
import folium


filename = "_simulations_gdf.csv"
# filename = "_simulations_reel_gdf.csv"

def create_df(filename) :
    """
    Create geodataframes from the simulation files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """
    dirname = "data/raw/" # relative path to the gitignore directory - the function on the file _dataframes_gpd.py is adapted to find the relative path of this directory
    df = pd.read_csv(dirname+filename,sep=';')

    return df

df = create_df(filename) # dataframe du fichier csv choisi

dist = 100000

tournee = df.iloc[[1]]


def IsIn(tournee, df, dist):


    cheflieu = gpd.GeoDataFrame(tournee, geometry='cheflieu') # we get the center of the cheflieu as a geometry
    cheflieu['buffer'] = cheflieu.geometry.buffer(dist) # create the buffer based on the cheflieu point
    cheflieu = cheflieu.drop(columns=['ID_COM','ID']) # drop the column to do the jointure
    cheflieu = gpd.GeoDataFrame(cheflieu, geometry='buffer') # we set the buffer as the gdf geometry

    df['linestring'] = df['geometry'] # backup of linestring to preserve for the jointure
    df = gpd.GeoDataFrame(df, geometry='geometry') #we set the line as a geometry

    IsMutu = cheflieu.sjoin(df, predicate='contains', how='inner') # we join with lines from the simulations from before the manipulation
    IsMutu = IsMutu[IsMutu['id_utilisateur_right']!=IsMutu['id_utilisateur_left']] # filter the users with the same ID

    return IsMutu


print(IsIn(tournee, df, dist))



A = []


# utiliser seaborn plutôt que matplotlib

# plt.hist(A,bins=20,range=(0,4),color="y",edgecolor="gray",label="histogramme")
# plt.title('Histogramme de mutualisation des producteurs sur la France, dans un rayon de 100km autour des exploitations')
# plt.xlabel('Nombre de producteur dans le rayon de 100 km')
# plt.ylabel('Count')
# plt.show()

