import os
import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point, LineString, shape
import matplotlib as plt
import numpy as np




def histo(data, filename, dist):
    n = gdf.count()[0] # number of total rounds
    A = []
    for i in range(n):
        tournee = gdf.iloc[[i]]



    plt.hist(data,bins=20,color="blue",edgecolor="gray",label="histogramme") # 10 class histogram
    plt.title('Histogramme du nombre de mutualisations possibles :'+filename)
    plt.xlabel('Nombre de producteurs dans un rayon de '+str(dist*1e-3)+' km')
    plt.ylabel('Fréquence')
    plt.show()



if __name__ == "__main__":
    # filename = "simulations_gdf.csv"
    filename = "simulations_reel_gdf.csv"

    gdf = create_df(filename) # dataframe du fichier csv choisi
    dist = 50000
    data = IsIn(gdf, dist)
    print(gdf)
    # histo(data, filename, dist)

