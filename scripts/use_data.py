import os
import geopandas as gpd
import pandas as pd
from shapely import wkt

from shapely.geometry import Point, LineString, shape

def create_gdf(filename, ColumnsGeometry) :
    """
    Create geodataframes from the real simulation files

    Args:
        filename (string): name of file in the directory ../data/raw
        ColumnsGeometry (string): name of the column to be defined as the geometry of the Geodataframe 
    """
    root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory
    dirname = "/data/raw/" # relative path to the gitignore directory - the function on the file _dataframes_gpd.py is adapted to find the relative path of this directory
    df = pd.read_csv(root + dirname+ filename,sep=';')
    geometry = df[ColumnsGeometry].map(wkt.loads)
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
             

def coord_lister(geom):
    """
    Return a list of coordenate of a given geometry

    Args:
        id {int}: a row of an geodataframe

    """    
    coords = list(geom.coords)
    return (coords)


def get_itineraire(id,geodataframe):
    
    """
    Return a geodataframe containing  the intineraire of the given id

    Args:
        id {int}: a row of an geodataframe

    """    
    sample = geodataframe[geodataframe['id_simulation']==id]
    return sample

if __name__ == "__main__":

    filename = "simulations_reel_gdf.csv"
    gdf = create_gdf(filename, 'itineraire') # dataframe du fichier csv choisi
    print(gdf)
    print(gdf.geometry.to_crs(4326))
    # Test
    # gdf = gpd.GeoDataFrame(gdf, geometry=gdf['itineraire'].map(wkt.loads),crs = 'EPSG:2154')
    A = gdf.iloc[[0]]
    linestring = A['geometry']
    print(line_to_coord(linestring))



