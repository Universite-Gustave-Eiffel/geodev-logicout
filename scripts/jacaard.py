import geopandas as gpd
from shapely import wkt
import IsInclude



"""
This module has a function that, for a specific row of a Geopandas's dataframe, return an pandas dataframe with the id and the jacaard's index of the mutualisables itineraires

"""

def jacaard_index(row,geodataframe,dist,buffer_convex_hull,type):



    """
    Return a geodataframe containing all the intineraires mutualisables for an itineraire 
    We take 3 steps:
    1 - Take all itineraires from geodataframe are within a buffer of 100km from the row respective cheflieu .
    2 - Verify if we taking a differente user
    3 - Verify if the row are within a 100km each one of those itineraires filtered in the step 2


    Args:
        row {geopandas Geodataframe line}: a row of an geodataframe
        geodataframe {geopandas Geodataframe}: name of file in the directory ../data/raw
        dist {int}: buffer size in meters´
        buffer_enveloppe {int}: size of the buffer applied to the lines before generating the convex hull
        buffer_enveloppe {int}: size of the buffer applied to the lines before generating the convex hull
    """    
    #call the function to generate the talbe of itineraires that are mutualisables
    geo_df_envelop = IsInclude.IsIn_tournee_gdf(row,geodataframe,dist,type)



    row=gpd.GeoDataFrame(row, geometry=row['itineraire'].map(wkt.loads),crs = 'EPSG:2154')  # we change the geometry to itineraire
    row['buffer'] = row.geometry.buffer(buffer_convex_hull) # we calculate a buffer of 1km to avoid the empty envelopes
    row=gpd.GeoDataFrame(row['id_simulation'], geometry=row['buffer'].convex_hull,crs = 'EPSG:2154') #then we create the envelope and set it as the geometry of the gdf


    geo_df_envelop=gpd.GeoDataFrame(geo_df_envelop, geometry =geo_df_envelop['itineraire_right'].map(wkt.loads)) #we do the same for the mutualisable
    geo_df_envelop['buffer']=geo_df_envelop.geometry.buffer(buffer_convex_hull) 
    geo_df_envelop=gpd.GeoDataFrame(geo_df_envelop, geometry=geo_df_envelop['buffer'].convex_hull,crs = 'EPSG:2154')


    # we calculate the intersection and the union between the itineraire and their bles counterparts
    intersection = row.overlay(geo_df_envelop, how='intersection')
    row_area=row.area
    intersection['intersection_area'] = intersection.area # we calculate the area of the intersection
    geo_df_envelop['union_area'] = geo_df_envelop.area + row_area # and the area of the union. We must subtract the intersection area after the join
    geo_df_envelop = geo_df_envelop.join(intersection.set_index('id_simulation_right'), on='id_simulation_right',lsuffix='_caller', rsuffix='_other') 

    geo_df_envelop = gpd.GeoDataFrame(geo_df_envelop[['id_simulation','id_simulation_right','union_area','intersection_area']],geometry=geo_df_envelop['geometry_caller'])

    #we calculate  the Jacaard's index

    geo_df_envelop['intersection_area']=geo_df_envelop['intersection_area'].fillna(0)

    geo_df_envelop['union_area']=(geo_df_envelop['union_area']-geo_df_envelop['intersection_area'])
    geo_df_envelop['jaacard'] = geo_df_envelop['intersection_area']/geo_df_envelop['union_area']
    geo_df_envelop['intersection_area']=geo_df_envelop['intersection_area'].fillna(0)
    geo_df_envelop['id_simulation'] = row['id_simulation']


    return geo_df_envelop

