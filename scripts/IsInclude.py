import os
import geopandas as gpd
import pandas as pd
from shapely import wkt
from shapely.geometry import Point, LineString, shape
import matplotlib as plt
import numpy as np
import use_data



def IsIn_tournee_gdf(tournee, gdf, dist):
    """
        Retourne un d
    """

    geometry = tournee['cheflieu'].map(wkt.loads)
    cheflieu = gpd.GeoDataFrame(tournee, geometry=geometry, crs = 'EPSG:2154') # we get the center of the cheflieu as a geometry
    cheflieu['buffer'] = cheflieu.geometry.buffer(dist) # create the buffer based on the cheflieu point

    cheflieu = cheflieu.drop(columns=['ID_COM']) # drop the column to do the jointure
    cheflieu = gpd.GeoDataFrame(cheflieu, geometry='buffer') # we set the buffer as the gdf geometry

    geometry_iti = gdf['itineraire'].map(wkt.loads)
    gdf2 = gpd.GeoDataFrame(gdf, geometry=geometry_iti, crs = 'EPSG:2154') #we set the line as a geometry

    gdf_IsInclude = cheflieu.sjoin(gdf2, predicate='contains', how='inner') # we join with lines from the simulations from before the manipulation
    gdf_IsInclude = gdf_IsInclude[gdf_IsInclude['id_utilisateur_right']!=gdf_IsInclude['id_utilisateur_left']] # filter the users with the same ID
    gdf_IsInclude = gdf_IsInclude.drop(columns=['index_right']) # drop the column to do the jointure

    return gdf_IsInclude


# permet de faire la validation du rayon inverse mais ne fonctionne pas pour l'instant

def IsIn_tournee_tournee(tourneeA, tourneeB, dist):
    """
    Returns true if tour A is in the distribution radius buffer meter of tour B
    else return false

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """
    # definition of the tour geometry A : 'itineraire'
    geometryA = tourneeA['itineraire'].map(wkt.loads)
    tourneeA = gpd.GeoDataFrame(tourneeA, geometry=geometryA, crs = 'EPSG:2154')

    # definition of the tour geometry B : 'chef-lieu'
    geometryB = tourneeB['cheflieu_right'].map(wkt.loads)
    tourneeB = gpd.GeoDataFrame(tourneeB, geometry=geometryB, crs = 'EPSG:2154')
    tourneeB['buffer'] = tourneeB.geometry.buffer(dist)
    tourneeB = gpd.GeoDataFrame(tourneeB, geometry='buffer', crs = 'EPSG:2154')

    gdf_IsInclude = tourneeB.sjoin(tourneeA, predicate='contains', how='inner')

    return gdf_IsInclude.count()[0]


    

if __name__ == "__main__":

    filename = "simulations_reel_gdf.csv"
    gdf = use_data.create_gdf(filename) # dataframe du fichier csv choisi
    tournee = gdf.iloc[[290]]
    dist = 100000
    test = IsIn_tournee_gdf(tournee, gdf, dist)

    tourneeB = test[test['id_utilisateur_right']==194]

    print(IsIn_tournee_tournee(tournee, tourneeB, dist))
    # n = test.count()[0]
    # for i in range(n):
    #     tourneeB = test.iloc[[i]]
    #     print(IsIn_tournee_tournee(tournee, tourneeB, dist))





