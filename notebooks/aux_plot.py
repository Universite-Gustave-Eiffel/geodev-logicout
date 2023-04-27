import sys  
sys.path.insert(0, '../scripts')
import numpy as np
import indexes, use_data, IsInclude
import pandas as pd
import geopandas as gpd
from shapely import wkt,MultiLineString
import ast

def mutualisations_with_index(sample_itineraire,geodataframe,radius,buffer_hull,type,area):
    
    sample_itineraire = use_data.get_itineraire(sample_itineraire,geodataframe)
    gdf = IsInclude.IsIn_tournee_gdf(sample_itineraire,geodataframe,radius,type) #verify all the mutualisables itineraires

    gdf = indexes.jacaard_index(sample_itineraire, gdf,buffer_hull) # we apply the jaacard index

    gdf = indexes.dist_start(sample_itineraire,gdf) # we calculate the distance between their starting points

    gdf = indexes.max_distance(sample_itineraire,gdf) # We calculate the maximum distance between the itineraire and his mutualisables counterparts

    gdf = indexes.index(gdf,area) # We calculate the index of distance

    return gdf


def plot_mutualisations(id, dataframe,**parameters):
    sample = use_data.get_itineraire(id,dataframe)
    sample_gdf = mutualisations_with_index(id, dataframe,**parameters)
    best_mutualisations = sample_gdf[['id_simulation_right','index','index_with_jaacard']].sort_values(by='index_with_jaacard').head()
    best_mutualisations = best_mutualisations.sort_values(by='id_simulation_right')
    best_mutualisations_ind = best_mutualisations['index_with_jaacard'].values.tolist()
    best_mutualisations_ind.append(0)
    itineraires_to_plot = best_mutualisations['id_simulation_right'].values
    best_mutualisations_gdf = dataframe[dataframe['id_simulation'].isin(itineraires_to_plot)]
    best_mutualisations_gdf = gpd.GeoDataFrame( pd.concat( [best_mutualisations_gdf,sample], ignore_index=True) )
    best_mutualisations_gdf['final_index']= best_mutualisations_ind
    best_mutualisations_gdf=gpd.GeoDataFrame(best_mutualisations_gdf,geometry=best_mutualisations_gdf['start'].map(wkt.loads))
    m= best_mutualisations_gdf.explore(tiles='CartoDB positron',cmap = "plasma",column='final_index',categorical=True,style_kwds=dict(fill=False, stroke=True,weight=5))
    best_mutualisations_gdf=gpd.GeoDataFrame(best_mutualisations_gdf,geometry=best_mutualisations_gdf['itineraire'].map(wkt.loads))
    m= best_mutualisations_gdf.explore(m=m,tiles='CartoDB positron',cmap = "plasma",column='final_index',categorical=True,style_kwds=dict(fill=False, stroke=True,weight=3))
    
    return best_mutualisations,m


def plot_mutualisations_non_zero_index(id, dataframe,**parameters):
    sample = use_data.get_itineraire(id,dataframe)
    sample_gdf = mutualisations_with_index(id, dataframe,**parameters)
    sample_gdf=sample_gdf[sample_gdf['index_with_jaacard']!=0]
    best_mutualisations = sample_gdf[['id_simulation_right','index','index_with_jaacard']].sort_values(by='index_with_jaacard').head()
    best_mutualisations = best_mutualisations.sort_values(by='id_simulation_right')
    best_mutualisations_ind = best_mutualisations['index_with_jaacard'].values.tolist()
    best_mutualisations_ind.append(0)
    itineraires_to_plot = best_mutualisations['id_simulation_right'].values
    best_mutualisations_gdf = dataframe[dataframe['id_simulation'].isin(itineraires_to_plot)]
    best_mutualisations_gdf = gpd.GeoDataFrame( pd.concat( [best_mutualisations_gdf,sample], ignore_index=True) )
    best_mutualisations_gdf['final_index']= best_mutualisations_ind
    best_mutualisations_gdf=gpd.GeoDataFrame(best_mutualisations_gdf,geometry=best_mutualisations_gdf['start'].map(wkt.loads))
    m= best_mutualisations_gdf.explore(tiles='CartoDB positron',cmap = "plasma",column='final_index',categorical=True,style_kwds=dict(fill=False, stroke=True,weight=5))
    best_mutualisations_gdf=gpd.GeoDataFrame(best_mutualisations_gdf,geometry=best_mutualisations_gdf['itineraire'].map(wkt.loads))
    m= best_mutualisations_gdf.explore(m=m,tiles='CartoDB positron',cmap = "plasma",column='final_index',categorical=True,style_kwds=dict(fill=False, stroke=True,weight=3))
    
    return best_mutualisations,m



def plot_mutualisations_zero_index(id, dataframe,**parameters):
    sample = use_data.get_itineraire(id,dataframe)
    sample_gdf = mutualisations_with_index(id, dataframe,**parameters)
    best_mutualisations = sample_gdf[['id_simulation_right','index','index_with_jaacard']].sort_values(by='index_with_jaacard').head()
    best_mutualisations = best_mutualisations.sort_values(by='id_simulation_right')
    best_mutualisations_ind = best_mutualisations['index_with_jaacard'].values.tolist()
    #best_mutualisations_ind.append(0)
    itineraires_to_plot = best_mutualisations['id_simulation_right'].values
    best_mutualisations_gdf = dataframe[dataframe['id_simulation'].isin(itineraires_to_plot)]
    #best_mutualisations_gdf = gpd.GeoDataFrame( pd.concat( [best_mutualisations_gdf,sample], ignore_index=True) )
    
    m = sample.explore(tiles='CartoDB positron',cmap = "plasma",column='id_simulation',categorical=True,style_kwds=dict(color='black',fill=False, stroke=True,weight=15,opacity=0.4))
    sample = gpd.GeoDataFrame(sample,geometry=sample['itineraire'].map(wkt.loads))
    m= sample.explore(m=m,tiles='CartoDB positron',cmap = "plasma",column='id_simulation',categorical=True,style_kwds=dict(color='black',fill=False, stroke=True,weight=10,opacity=0.4))


    best_mutualisations_gdf['final_index']= best_mutualisations_ind

    best_mutualisations_gdf=gpd.GeoDataFrame(best_mutualisations_gdf,geometry=best_mutualisations_gdf['start'].map(wkt.loads))
    m= best_mutualisations_gdf.explore(m=m,tiles='CartoDB positron',cmap = "plasma",column='id_simulation',categorical=True,style_kwds=dict(fill=False, stroke=True,weight=5))
    best_mutualisations_gdf=gpd.GeoDataFrame(best_mutualisations_gdf,geometry=best_mutualisations_gdf['itineraire'].map(wkt.loads))
    m= best_mutualisations_gdf.explore(m=m,tiles='CartoDB positron',cmap = "plasma",column='id_simulation',categorical=True,style_kwds=dict(fill=False, stroke=True,weight=3))

    return best_mutualisations,m