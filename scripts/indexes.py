import geopandas as gpd
from shapely import wkt, hausdorff_distance
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString, shape, mapping
import numpy as np
from shapely import wkt
import use_data 
from scipy.spatial.distance import cdist
"""
This module contains the function to generate the different kinds of indexes that we use for our algorithm to find the mutualisables itineraires

"""

def jacaard_index(row,geodataframe,buffer_hull):
    """
    Calculate the Jaacard's index for all mutualisations of a given itinerary from a dataframe
    
    Args:
        row {geopandas Geodataframe line}: a row of an geodataframe
        geodataframe {geopandas Geodataframe}: a geodataframe of the mutualisables itineraires for the given row
        buffer_hull {int}: size of the buffer applied to the lines before generating the convex hull

    Returns:

        geo_df_envelop {geopandas Geodataframe}: Geodataframe containing the above index
    """    
    
    # we change the geometries to 'itineraire'
    geo_df_envelop=gpd.GeoDataFrame(geodataframe, geometry =geodataframe['itineraire_right'].map(wkt.loads))
    row=gpd.GeoDataFrame(row, geometry=row['itineraire'].map(wkt.loads),crs = 'EPSG:2154') 

    # we calculate a buffer of 1km to avoid the empty envelopes
    row['buffer'] = row.geometry.buffer(buffer_hull) 

    #then we create the envelope and set it as the geometry of the gdf
    row=gpd.GeoDataFrame(row['id_simulation'], geometry=row['buffer'].convex_hull,crs = 'EPSG:2154') 
    geo_df_envelop['buffer']=geo_df_envelop.geometry.buffer(buffer_hull) 
    geo_df_envelop=gpd.GeoDataFrame(geo_df_envelop, geometry=geo_df_envelop['buffer'].convex_hull,crs = 'EPSG:2154')

    #we backup those geometries before the joins
    geo_df_iti_right = geo_df_envelop['itineraire_right']
    geo_df_start_right =  geo_df_envelop['start_right']
    
    
    # we calculate the intersection and the union between the itineraire and their bles counterparts
    intersection = row.overlay(geo_df_envelop, how='intersection')
    row_area=row.area

    
    # we calculate the area of the intersection
    intersection['intersection_area'] = intersection.area 

    # and the area of the union. We must subtract the intersection area after the join
    geo_df_envelop['union_area'] = geo_df_envelop.area + row_area 
    geo_df_envelop = geo_df_envelop.join(intersection.set_index('id_simulation_right'), on='id_simulation_right',lsuffix='_caller', rsuffix='_other') 


    geo_df_envelop = gpd.GeoDataFrame(geo_df_envelop[['id_simulation','id_simulation_right','union_area','intersection_area']],geometry=geo_df_envelop['geometry_caller'])


    #we calculate  the Jacaard's index and save the usefull geometries

    geo_df_envelop['intersection_area']=geo_df_envelop['intersection_area'].fillna(0)
    geo_df_envelop['itineraire_right'] =  geo_df_iti_right
    geo_df_envelop['start_right'] =  geo_df_start_right
    geo_df_envelop['union_area']=(geo_df_envelop['union_area']-geo_df_envelop['intersection_area'])
    geo_df_envelop['jaacard'] = geo_df_envelop['intersection_area']/geo_df_envelop['union_area']
    geo_df_envelop['intersection_area']=geo_df_envelop['intersection_area'].fillna(0)
    geo_df_envelop['id_simulation'] = row['id_simulation']


    return geo_df_envelop



def dist_start(itinerary,geodataframe):

    """
    Return one geodataframe with an additional column containing the distance between the starting point of each element
    and the starting point of a given itinerary 
    
    Args:
        itinerary {geopandas Geodataframe line}: a row of an geodataframe
        geodataframe {geopandas Geodataframe}: a geodataframe of the mutualisables itineraries for the given row
        buffer_hull {int}: size of the buffer applied to the lines before generating the convex hull
    
    Returns:
        geo_df_envelop {geopandas Geodataframe}: Geodataframe containing the above index

    """    


    #we change the geometry of the dataframes to their starting point


    itinerary = gpd.GeoDataFrame(itinerary, geometry = itinerary['start'].map(wkt.loads)) 
    geodataframe = gpd.GeoDataFrame(geodataframe, geometry = geodataframe['start_right'].map(wkt.loads)) 

    #and use the geopanda's function to calculate the distance between the starting point
    geodataframe['start_distance'] = geodataframe.distance(itinerary)
    
    return geodataframe



def max_distance(itineraire,geodataframe):

    """
    Return one geodataframe with an additional column containing the max distance between the itineraire of each element
    and the a given itineraire 
    
    Args:
        itineraire {geopandas Geodataframe line}: a row of an geodataframe
        geodataframe {geopandas Geodataframe}: a geodataframe of the mutualisables itineraires for the given row

    """            

    # we change the geometry of the dataframes to their itineraires
    itineraire = gpd.GeoDataFrame(itineraire, geometry = itineraire['itineraire'].map(wkt.loads)) 
    geodataframe = gpd.GeoDataFrame(geodataframe, geometry = geodataframe['itineraire_right'].map(wkt.loads))  


    #As there's a lot of points to compare we will vectorialize this calcul   
    row_points = itineraire.geometry.map(use_data.coord_lister).tolist()
    row_points = np.array(row_points[0])
    gdf_points = geodataframe.geometry.map(use_data.coord_lister).tolist()
    
    #we make the vectorized calcul for each the gdf row cause they have different sizes and can't be treated 
    #all at the same time
    max_distances = [ np.amax((cdist(row_points, np.array(x), 'euclidean'))) for x in gdf_points]
    geodataframe['max_distance'] = max_distances
       
    
    #If we decide to add another distance, for example, the hausdorff distance, we can simply ad the code here
    #EX:
    #gdf['hausdorff'] = gdf.apply(lambda x : hausdorff_distance(itineraire.geometry,geodataframe.geometry), axis=1)
       
    return geodataframe

def index(geodataframe,area):

    """
    Return one geodataframe with two added indexes:
    
    Args:
        area{float}: parameter for normalization of the index -usually pi*radius for mutualisation**2
        geodataframe {geopandas Geodataframe}: a geodataframe of the mutualisables itineraires for the given row

    """            

    geodataframe['index']= geodataframe['start_distance'] * geodataframe['max_distance'] / area
    geodataframe['index_with_jaacard'] = geodataframe['index'] * (1-geodataframe['jaacard'])
    return geodataframe