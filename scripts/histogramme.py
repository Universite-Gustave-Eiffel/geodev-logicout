import numpy as np
import matplotlib as plt
import os
import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point, LineString, shape
import folium




def create_df(filename) :
    """
    Create geodataframes from the simulation files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """
    dirname = "data/raw/" # relative path to the gitignore directory - the function on the file _dataframes_gpd.py is adapted to find the relative path of this directory
    df = pd.read_csv(dirname+filename,sep=';')

    return df





# Import CSV 

link = ''
data = np.genfromtxt(link, delimiter=',')

# Appel algo rayon 100km

A = []

plt.hist(A,bins=20,range=(0,4),color="y",edgecolor="gray",label="histogramme")
plt.title('Histogramme de mutualisation des producteurs sur la France, dans un rayon de 100km autour des exploitations')
plt.xlabel('Nombre de producteur dans le rayon de 100 km')
plt.ylabel('Count')
plt.show()

