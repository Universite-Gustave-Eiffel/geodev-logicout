# Imports

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString, shape
import matplotlib as plt
import numpy as np
from shapely import wkt
import csv

# File imports

import use_data
import indice
import jacaard
import IsInclude

##################################### Start #####################################

def algo_une_tournee(tournee, gdf, inclusion, filename, radius, buffer_convex_hull, file_output):

    gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, radius, inclusion)
    print(gdf_IsInclude.columns.values.tolist())
    gdf1_IsInclude = gpd.GeoDataFrame(gdf_IsInclude, geometry=gdf_IsInclude['start'].map(wkt.loads), crs = 'EPSG:2154')
    gdf2_IsInclude = gpd.GeoDataFrame(gdf_IsInclude, geometry=gdf_IsInclude['itineraire'].map(wkt.loads), crs = 'EPSG:2154')
    
    gdf_base = use_data.create_gdf(filename, 'cheflieu')

    gdf_enveloppe = jacaard.jacaard_index(tournee,gdf_IsInclude,radius,buffer_convex_hull,inclusion)

    nb_lines = gdf_IsInclude.count()[0]

    result = []
    
    # result.append(tournee['id_simulation'].values[0])

    for i in range(nb_lines):

        # Indice de distance 
        dist_start = indice.dist_start(tournee,gdf1_IsInclude.iloc[[i]])
        
        ind_dist = indice.indice(tournee,gdf2_IsInclude.iloc[[i]],dist_start,radius)
        
        # Indice d'enveloppe convexe
        ind_env = gdf_enveloppe.iloc[[i]]['jaacard'].values[0]

        # Indice final 
        de = ind_dist*(1-ind_env)

        result.append([tournee['id_simulation'].values[0],gdf2_IsInclude.iloc[[i]]['id_simulation_right'].values[0],ind_dist,ind_env,de])
        # print([tournee['id_simulation'].values[0],gdf2_IsInclude.iloc[[i]]['id_simulation_right'].values[0],ind_dist,ind_env,de])
    
    headerList = ['id_A','id_B','ind distance','ind enveloppe','ind regroupé']

    # Sauvegarde dans un csv
    # np.savetxt(file_output, result , delimiter=' ') 
    with open('_final.csv','w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        # csvwriter.writeheader()
        csvwriter.writerows(result)

        
        # A regarder :  changer la boucle et le gdf sur lequel on extrait les données, pour mettre celui de l'enveloppe convexe.
        # Regarder aussi pour mettre un header sur le fichier csv

        
    

if __name__ == "__main__": 

    filename = 'simulations_reel_gdf.csv'
    gdf = use_data.create_gdf(filename,'cheflieu')
    tournee = gdf.iloc[[0]]
    radius = 100000
    buffer_convex_hull = 1000
    inclusion = 2
    file_output = 'ind.txt'

    algo_une_tournee(tournee, gdf, inclusion, filename, radius, buffer_convex_hull, file_output)