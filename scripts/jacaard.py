import geopandas as gpd
import pandas as pd
from shapely import wkt
from shapely.geometry import Point, LineString, shape
import use_data
import IsInclude



"""
This module has a function that, for a specific row of a Geopandas's dataframe, return an pandas dataframe with the id and the jacaard's index of the mutualisables itineraires

"""



#we take the database and a row as example
geo_df= use_data.create_gdf('_simulations_reel_gdf.csv')
row_sample = geo_df.iloc[[3]]




def jacaard_index(row,geodataframe):
    #call the function to generate the talbe of itineraires that are mutualisables
    geo_df_envelop = IsInclude.IsIn_tournee_gdf(row,geodataframe,100000)



    row=gpd.GeoDataFrame(row, geometry=row['itineraire'].map(wkt.loads),crs = 'EPSG:2154')  # we change the geometry to itineraire
    row['buffer'] = row.geometry.buffer(1000) # we calculate a buffer of 1km to avoid the empty envelopes
    row=gpd.GeoDataFrame(row['id_simulation'], geometry=row['buffer'].convex_hull,crs = 'EPSG:2154') #then we create the envelope and set it as the geometry of the gdf


    geo_df_envelop=gpd.GeoDataFrame(geo_df_envelop, geometry =geo_df_envelop['itineraire_right'].map(wkt.loads)) #we do the same for the mutualisable
    geo_df_envelop['buffer']=geo_df_envelop.geometry.buffer(1000) 
    geo_df_envelop=gpd.GeoDataFrame(geo_df_envelop[['id_simulation_right']], geometry=geo_df_envelop['buffer'].convex_hull,crs = 'EPSG:2154')


    # we calculate the intersection and the union between the itineraire and their bles counterparts
    intersection = row.overlay(geo_df_envelop, how='intersection')
    row_area=row.area
    intersection['intersection_area'] = intersection.area # we calculate the area of the intersection
    geo_df_envelop['union_area'] = geo_df_envelop.area + row_area # and the area of the union. We must subtract the intersection area after the join
    geo_df_envelop = geo_df_envelop.join(intersection.set_index('id_simulation_right'), on='id_simulation_right',lsuffix='_caller', rsuffix='_other') # we join t
    geo_df_envelop = gpd.GeoDataFrame(geo_df_envelop[['id_simulation','id_simulation_right','union_area','intersection_area']],geometry=geo_df_envelop['geometry_caller'])

    #we calculate  the Jacaard's index

    geo_df_envelop['intersection_area']=geo_df_envelop['intersection_area'].fillna(0)
    geo_df_envelop['jaacard'] = geo_df_envelop['intersection_area']/(geo_df_envelop['union_area']-geo_df_envelop['intersection_area'])
    geo_df_envelop['intersection_area']=geo_df_envelop['intersection_area'].fillna(0)
    geo_df_envelop['id_simulation'] = row['id_simulation']


    return geo_df_envelop





jacaard= jacaard_index(row_sample,geo_df)

print(jacaard)