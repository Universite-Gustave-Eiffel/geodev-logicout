import os
import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point, LineString, shape
import matplotlib.pyplot as plt
import numpy as np
import use_data
import IsInclude




def histo(gdf, typefile, dist, typeCheck):
    """
        typeCheck = 1 si une seule implication 
                  = 2 si double implication

        typefile = tournées quelconques ou réelles
    """
    n = gdf.count()[0] # number of total rounds
    A = []
    for i in range(n):
        tournee = gdf.iloc[[i]]
        if typeCheck == 1:
            gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, dist)
        else :
            gdf_IsInclude = IsInclude.double_check(tournee, gdf, dist)
        
        nbrMutu = gdf_IsInclude.count()[0]
        A.append(nbrMutu)

    # affichage de l'histogramme
    plt.hist(A,bins=20,color="blue",edgecolor="gray",label="histogramme")
    plt.title('Histogramme du nombre de mutualisations possibles : tournées '+typefile)
    plt.xlabel('Nombre de tournées dans un rayon de '+str(dist*1e-3)+' km pour des utilisateurs différents')
    plt.ylabel('Fréquence')
    plt.show()




if __name__ == "__main__":
    # filename = "simulations_gdf.csv"
    filename = "simulations_reel_gdf.csv"

    gdf = use_data.create_gdf(filename) # dataframe du fichier csv choisi
    dist = 100000
    typeCheck = 2 # 1 ou 2
    typefile = 'réelles' # 'quelconques' ou 'réelles'
    print(histo(gdf, typefile, dist, typeCheck))


