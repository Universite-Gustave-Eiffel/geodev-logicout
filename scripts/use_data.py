import os
import geopandas as gpd
import pandas as pd
from shapely import wkt
pd.options.mode.chained_assignment = None  # to avoid warnings

def create_gdf(filename) :
    """
    Create geodataframes from the real simulation files
    Args:
        path_trajet (string): name of file in the directory ../data/raw
    """
    root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory
    dirname = "/data/raw/" # relative path to the gitignore directory - the function on the file _dataframes_gpd.py is adapted to find the relative path of this directory
    df = pd.read_csv(root + dirname+ filename,sep=';')
    geometry = df['cheflieu'].map(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs = 'EPSG:2154')
    return gdf


# def affichage():
#     # Affichage graphique pour certaines valeurs
#     if i % 500 == 0:
#         root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory
#         row_itineraire = gpd.GeoDataFrame(tournee, geometry=geometry_iti, crs = 'EPSG:2154')
#         m = row_itineraire.explore(name = 'livraison',style_kwds=dict(fill=False, stroke=True,weight=5,color='black'))
        
#         m = cheflieu.explore(m=m, name="Buffer", style_kwds=dict(fill=False, stroke=True,color='black'))
        
#         row_lines = gpd.GeoDataFrame(IsMutu, geometry=geometry_iti, crs = 'EPSG:2154')
#         m = row_lines.explore(m=m, cmap = 'Paired', column='id_simulation_right', categorical=True)

#         output = root+"/data/raw/"+str(i)+"_simulation.html"
#         m.save(output)


def mutualisables(row,geodataframe):
    """
    Return a geodataframe containing all the intineraires mutualisables for an itineraire 
    We take 3 steps:
    1 - Take all itineraires from geodataframe are within a buffer of 100km from the row respective cheflieu .
    2 - Verify if we taking a differente user
    3 - Verify if the row are within a 100km each one of those itineraires filtered in the step 2


    Args:
        row {geopandas Geodataframe line}: a row of an geodataframe
        geodataframe {geopandas Geodataframe}: name of file in the directory ../data/raw
    """


    #Step 1

    gdf = gpd.GeoDataFrame(geodataframe, geometry=geodataframe['itineraire'].map(wkt.loads))
    tournee = row # we select a single row to apply the algorithm
    geometry = tournee['cheflieu'].map(wkt.loads)
    cheflieu = gpd.GeoDataFrame(tournee, geometry=geometry, crs = 'EPSG:2154') # we get the center of the cheflieu as a geometry
    cheflieu['buffer'] = cheflieu.geometry.buffer(100000) # create the buffer based on the cheflieu point
    cheflieu = cheflieu.drop(columns=['ID_COM']) # drop the column to do the jointure
    cheflieu = gpd.GeoDataFrame(cheflieu, geometry='buffer') # we set the buffer as the gdf geometry
    IsMutu = cheflieu.sjoin(gdf, predicate='contains', how='inner') # we join with lines from the simulations from before the manipulation
    
    
    #Step 2
    
    IsMutu = IsMutu[IsMutu['id_utilisateur_right']!=IsMutu['id_utilisateur_left']] # filter the users with the same ID

    #Step 3

    IsMutu['buffer'] = IsMutu.geometry.buffer(100000)
    IsMutu = gpd.GeoDataFrame(IsMutu, geometry='buffer')
    tournee.set_geometry(tournee['cheflieu'].map(wkt.loads))
    tournee['buffer'] = tournee.geometry.buffer(100000)
    tournee = gpd.GeoDataFrame(tournee, geometry='buffer')
 

    
    #we prepare the data to return
    IsMutu = IsMutu.drop(columns=['index_right'])
    IsMutu = gpd.sjoin(IsMutu,tournee.to_crs('EPSG:2154'),how='left')
    

    return IsMutu  



if __name__ == "__main__":

    filename = "simulations_reel_gdf.csv"
    gdf = create_gdf(filename) # dataframe du fichier csv choisi
    print(gdf)