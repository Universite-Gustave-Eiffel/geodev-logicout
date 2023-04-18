import os
import geopandas as gpd
import pandas as pd
from shapely import wkt

from shapely.geometry import Point, LineString, shape


def create_gdf(filename, ColumnGeometry) :
    """
    Create geodataframes from the real simulation files

    Args:
        path_trajet (string): name of file in the directory ../data/raw

    """
    root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory
    dirname = "/data/raw/" # relative path to the gitignore directory - the function on the file _dataframes_gpd.py is adapted to find the relative path of this directory

    df = pd.read_csv(root +dirname+ filename,sep=';')
    geometry = df[ColumnGeometry].map(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs = 'EPSG:2154')
    return gdf



def line_to_points(line):
    """
    Découpe de la linestring en liste de points
    """
    return [Point(xy) for xy in line.coords]


def line_to_coord(linestring):
    """
    Récupère les coordonnées des points de la linestring, et les ajoutent dans un array qu'il retourne en sortie
    """
    C = []
    list_points = linestring.apply(line_to_points).explode()
    for point in list_points:
        x = point.x
        y = point.y
        C.append([point.x,point.y])

    return C    
             
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

if __name__ == "__main__":

    filename = "simulations_reel_gdf.csv"
    gdf = create_gdf(filename, 'cheflieu') # dataframe du fichier csv choisi
    print(gdf)
    
    # Test
    gdf = gpd.GeoDataFrame(gdf, geometry=gdf['itineraire'].map(wkt.loads),crs = 'EPSG:2154')
    A = gdf.iloc[[0]]
    linestring = A['geometry']
    print(line_to_coord(linestring))

