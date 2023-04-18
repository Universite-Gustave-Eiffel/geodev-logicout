import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString, shape


# Script to create the CSV of the filtered and joined dataframes
# Execute once to generate the csv files inside the folder "data/raw"


root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory


# we charge the shapes
df_communes = gpd.read_file(root + "/data/assets/COMMUNE.shp")  # Layer IGN
df_cheflieu = gpd.read_file(root + "/data/assets/CHFLIEU_COMMUNE.shp")  # Layer IGN
df_france = gpd.read_file(root + "/data/assets/FRANCE.shp")  # Layer cree a partir du shape REGION de lIGN
df_france = gpd.GeoDataFrame(df_france, geometry='geometry',crs="EPSG:2154")

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



#Creation and filtering of utilisateurs dataframe
df_utilisateurs = create_utilisateurs_df('utilisateurs.csv')
df_utilisateurs= df_utilisateurs[df_utilisateurs['prise en compte O/N ENSG']=='oui']

#Creation of simulation dataframe and join with utilisateurs df
df_simulation = create_simulation_df('simulation.csv')
df_simulation_reel = df_simulation[df_simulation['type_simulation']=='reel']

#Creation of point_arret dataframe and join with utilisateurs_simulations
df_point_arret = create_point_arret_df('point_arret.csv')


def create_geodataframe(simulation,utilisateur,point_arret):

    """
    Create geodataframe with all the necessary fields to run the algorithm to find the mutualisations

    Args:
        simulation, utilisateur, point_arret  (string): name of files in the directory ../data/raw



    """   


    print('start')
    # we make the first dataframes    
    df_utilisateurs_simulations =pd.merge(simulation,utilisateur, left_on='id_utilisateur', right_on='id',how='inner')
    df_simulations_arrets = pd.merge(point_arret,df_utilisateurs_simulations, left_on='id_simulation', right_on='id_x',how='inner')
    gdf_simulation_arrets= gpd.GeoDataFrame(df_simulations_arrets[['id_simulation','id_utilisateur']], geometry=gpd.points_from_xy(df_simulations_arrets.longitude, df_simulations_arrets.latitude))

    #join segments of lines
    geo_df = gdf_simulation_arrets.groupby(['id_simulation', 'id_utilisateur'],as_index=False)['geometry'].apply(lambda x: LineString(x.tolist()) if x.size > 1 else None)

    #Setting the CRS and setting the projection to Lambert 2193
    geo_df = gpd.GeoDataFrame(geo_df, geometry='geometry',crs="EPSG:4326")
    geo_df= geo_df.to_crs("EPSG:2154")

    #Removing invalid geometries- "lines" made of two identical points
    geo_df = geo_df[geo_df['geometry'].is_valid==True]
      

    geo_df['start']= geo_df['geometry'].apply(lambda x: Point(x.coords[0])) # Taking the first point of the simmulation to verify its position
    geo_df= gpd.GeoDataFrame(geo_df,geometry='start') #A Geodataframe can only have one geometry at a time. We change it to "Start" point to join it with the layer "communes"
  
    geo_df_commune = geo_df.sjoin(df_communes,how='left')
    geo_df_commune = geo_df_commune.drop(columns=['index_right']) #Dropping the column to join effectively

    
    geo_df_chef_lieu = geo_df_commune.merge(df_cheflieu,left_on='ID', right_on='ID_COM') # proerty based join with the id of the 'cheflieu'
    geo_df_chef_lieu = geo_df_chef_lieu.rename(columns ={'geometry_x':'itineraire','geometry_y':'cheflieu'})

    
    geo_df_chef_lieu = gpd.GeoDataFrame(geo_df_chef_lieu,geometry='itineraire')

    # Joining the chef_lieu dataframe onto the france dataframe
    geo_df_chef_lieu = geo_df_chef_lieu.sjoin(df_france,how='left')
    geo_df_chef_lieu = gpd.GeoDataFrame(geo_df_chef_lieu,geometry='start')
    
    #Cleaning the dataframe
    geo_df_chef_lieu = geo_df_chef_lieu.drop(columns=['index_right','ID_right','ID_left','NOM_M','NOM','INSEE_REG'])        
    print(geo_df_chef_lieu.head())
    print(geo_df_chef_lieu.geometry)
    #Returning the final dataframe
    return geo_df_chef_lieu



simulations_to_csv = create_geodataframe(df_simulation,df_utilisateurs,df_point_arret)
simulations_reels_to_csv = create_geodataframe(df_simulation_reel,df_utilisateurs,df_point_arret)
simulations_to_csv.to_csv(root + "/data/raw/" + "simulations_gdf.csv",sep=';', index=False)
simulations_reels_to_csv.to_csv(root + "/data/raw/" + "simulations_reel_gdf.csv",sep=';', index=False)
