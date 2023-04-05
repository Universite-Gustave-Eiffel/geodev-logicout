import numpy as np
import matplotlib.pyplot as plt
import os
import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point, LineString, shape
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


def IsIn(gdf, dist):
    n = gdf.count()[0] # number of total rounds
    A = []
    for i in range(n):
        tournee = gdf.iloc[[i]]

        geometry = tournee['cheflieu'].map(wkt.loads)
        cheflieu = gpd.GeoDataFrame(tournee, geometry=geometry, crs = 'EPSG:2154') # we get the center of the cheflieu as a geometry
        cheflieu['buffer'] = cheflieu.geometry.buffer(dist) # create the buffer based on the cheflieu point

        cheflieu = cheflieu.drop(columns=['ID_COM']) # drop the column to do the jointure
        cheflieu = gpd.GeoDataFrame(cheflieu, geometry='buffer') # we set the buffer as the gdf geometry

        gdf['linestring'] = gdf['geometry'] # backup of linestring to preserve for the jointure
        gdf = gpd.GeoDataFrame(gdf, geometry='geometry') #we set the line as a geometry

        IsMutu = cheflieu.sjoin(gdf, predicate='contains', how='inner') # we join with lines from the simulations from before the manipulation
        IsMutu = IsMutu[IsMutu['id_utilisateur_right']!=IsMutu['id_utilisateur_left']] # filter the users with the same ID

        nbrMutu = IsMutu.count()[0]

        A.append(nbrMutu)
    
    return A


def histo(data, filename, dist):
    plt.hist(data,bins=10,color="blue",edgecolor="gray",label="histogramme") # 10 class histogram
    plt.title('Histogramme du nombre de mutualisations possibles :'+filename)
    plt.xlabel('Nombre de producteurs dans un rayon de '+str(dist*1e-3)+' km')
    plt.ylabel('Fréquence')
    plt.show()



if __name__ == "__main__":
    # filename = "simulations_gdf.csv"
    filename = "simulations_reel_gdf.csv"

    gdf = create_df(filename) # dataframe du fichier csv choisi
    dist = 100000
    data = IsIn(gdf, dist)

    histo(data, filename, dist)

