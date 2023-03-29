import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString, shape
import matplotlib
import folium

#import folium mapclassifypip 
#import ast //pour le trajet

root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory

def create_simulation_df(filename) :
    """
    Create geodataframes from the simulation files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """   
    
    df = pd.read_csv(root +"/data/raw/"+ filename,sep=';')

    return df

def create_trajet_df(filename) :
    """
    Create geodataframes from the trajet files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """   
    
    df = pd.read_csv(root +"/data/raw/"+ filename,sep=',')

    return df

def create_utilisateurs_df(filename) :
    """
    Create geodataframes from the utilisateurs files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """   

    df = pd.read_csv(root +"/data/raw/"+ filename,sep=';',encoding='cp1252')

    return df
    
def create_point_arret_df(filename) : 
    
    """
    Create geodataframes from the point_arret files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """   

    df = pd.read_csv(root + "/data/raw/"+ filename,sep=',')

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



df_communes = gpd.read_file(root + "/data/assets/COMMUNE.shp")  # Layer IGN
df_cheflieu = gpd.read_file(root + "/data/assets/CHFLIEU_COMMUNE.shp")  # Layer IGN


geo_df['start']= geo_df['geometry'].apply(lambda x: Point(x.coords[0])) # we take the first point of the simmulation to verify where it is
geo_df= gpd.GeoDataFrame(geo_df,geometry='start') #A Geodataframe can only have one geometry at a time. We change it to "Start" point to join it with the layer "communes"
geo_df_commune = geo_df.sjoin(df_communes,how='left')
geo_df_commune = geo_df_commune.drop(columns=['index_right']) #drop the column to do the jointure
geo_df_chef_lieu = geo_df_commune.merge(df_cheflieu,left_on='ID', right_on='ID_COM') # attributaire join with the id of the cheflieu
geo_df_chef_lieu = geo_df_chef_lieu.rename(columns ={'geometry_x':'intineraire','geometry_y':'cheflieu'})




# le dataframe geo_df_chef_lieu est à enregistrer sous format csv
# ajouter la condition de type_simulation (2 fichiers csv différents à créer)
# ajouter le filtre de la France

