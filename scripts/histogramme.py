import os
import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point, LineString, shape
import matplotlib as plt
import numpy as np
import folium

#import folium mapclassify
#import ast //pour le trajet

dirname = "data/raw/" # relative path to the gitignore directory - the function on the file _dataframes_gpd.py is adapted to find the relative path of this directory


def create_simulation_df(filename) :
    """
    Create geodataframes from the simulation files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """   
    
    df = pd.read_csv(dirname+filename,sep=';')

    return df

def create_trajet_df(filename) :
    """
    Create geodataframes from the trajet files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """   
    
    df = pd.read_csv(dirname+filename,sep=',')

    return df

def create_utilisateurs_df(filename) :
    """
    Create geodataframes from the utilisateurs files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """   

    df = pd.read_csv(dirname+filename,sep=';',encoding='cp1252')

    return df
    
def create_point_arret_df(filename) : 
    
    """
    Create geodataframes from the point_arret files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """   

    df = pd.read_csv(dirname+filename,sep=',')

    return df

#creation and filtering of utilisateurs dataframe
df_utilisateurs = create_utilisateurs_df('utilisateurs.csv')
df_utilisateurs_oui= df_utilisateurs[df_utilisateurs['prise en compte O/N ENSG']=='oui']

#creation of simulation dataframe and join with utilisateurs df
df_simulation = create_simulation_df('simulation.csv')
df_utilisateurs_simulations =pd.merge(df_simulation,df_utilisateurs_oui, left_on='id_utilisateur', right_on='id',how='inner')

#creation of point_arret dataframe and join with utilisateurs_simulations
df_point_arret = create_point_arret_df('point_arret.csv')
df_simulations_arrets = pd.merge(df_point_arret,df_utilisateurs_simulations, left_on='id_simulation', right_on='id_x',how='inner')

gdf_simulation_arrets= gpd.GeoDataFrame(df_simulations_arrets[['id_simulation','id_utilisateur']], geometry=gpd.points_from_xy(df_simulations_arrets.longitude, df_simulations_arrets.latitude))


#join segment of lines
geo_df = gdf_simulation_arrets.groupby(['id_simulation', 'id_utilisateur'],as_index=False)['geometry'].apply(lambda x: LineString(x.tolist()) if x.size > 1 else None)


#set CRS and change to Lambert 2193
geo_df = gpd.GeoDataFrame(geo_df, geometry='geometry',crs="EPSG:4326")
geo_df= geo_df.to_crs("EPSG:2154")

#Remove invalid geometries- "lines" made of two identical points
geo_df = geo_df[geo_df['geometry'].is_valid==True]


#to save a shapefile
#geo_df.to_file('dataframe.shp')  

df_communes = gpd.read_file("data/assets/COMMUNE.shp") # Layer IGN
df_cheflieu = gpd.read_file("data/assets/CHFLIEU_COMMUNE.shp") # Layer IGN


geo_df['start']= geo_df['geometry'].apply(lambda x: Point(x.coords[0])) # we take the first point of the simmulation to verify where it is
geo_df= gpd.GeoDataFrame(geo_df,geometry='start') #A Geodataframe can only have one geometry at a time. We change it to "Start" point to join it with the layer "communes"
geo_df_commune = geo_df.sjoin(df_communes,how='left')
geo_df_commune = geo_df_commune.drop(columns=['index_right']) #drop the column to do the jointure

geo_df_chef_lieu = geo_df_commune.merge(df_cheflieu,left_on='ID', right_on='ID_COM') # attributaire join with the id of the cheflieu
geo_df_chef_lieu = geo_df_chef_lieu.rename(columns ={'geometry_x':'intineraire','geometry_y':'cheflieu'})



# Début détection des livraisons dans les 100km 

A = []
def detect(geo_df_chef_lieu):

    
    # A : tableau de valeur avec juste le nombre de trajet mutualisable dans le rayon choisi 

    n = len(geo_df_chef_lieu) # A modifier pour trouver la bonne façon d'avoir le nombre de ligne
    for i in range(n):


        row= geo_df_chef_lieu.iloc[[i]] # test with one delivery
        row_itineraire = row # we store to plot the initial delivery
        row_itineraire= gpd.GeoDataFrame(row_itineraire,geometry='intineraire') # we transform it to a line
        row= gpd.GeoDataFrame(row,geometry='cheflieu') # we get the center of the cheflieu as a geometry 

        row['buffer'] = row.geometry.buffer(100000) # create the buffer based on the cheflieu point
        row = row.drop(columns=['ID_COM','ID']) #drop the column to do the jointure
        row = gpd.GeoDataFrame(row,geometry='buffer') # we set the buffer as the gdf geometry

        geo_df_commune['linestring'] = geo_df_commune['geometry']# backup of linestring to preserve for the jointure
        geo_df_commune = gpd.GeoDataFrame(geo_df_commune,geometry='geometry')#we set the line as a geometry

        count = 0
        if(row.sjoin(geo_df_commune,predicate='contains', how='inner')): # we join with lines from the simulations from before the manipulation
            # à regarder ici, renvoie un dataframe puis compter dedans le nombre d'éléments
            
            count +=1

        row = row[row['id_utilisateur_right']!=row['id_utilisateur_left']] # filter the users with the same ID
        row_lines = gpd.GeoDataFrame(row,geometry='linestring')

        # On regarde tous les trajets dans le rayon de 100 km

        # Regarder géopanda pour regrouper 
        # included_points = [geo_df_chef_lieu['start'] in row.sjoin(row['buffer'], predicate='contains')]



plt.hist(A,bins=20,range=(0,4),color="y",edgecolor="gray",label="histogramme")
plt.title('Histogramme de mutualisation des producteurs sur la France, dans un rayon de 100km autour des exploitations')
plt.xlabel('Nombre de producteur dans le rayon de 100 km')
plt.ylabel('Count')
plt.show()

