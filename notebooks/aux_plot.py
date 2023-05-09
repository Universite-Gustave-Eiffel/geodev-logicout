import sys  
sys.path.insert(0, '../scripts')
import numpy as np
import indexes, use_data, IsInclude
import pandas as pd
import geopandas as gpd
from shapely import wkt,MultiLineString
import ast


# This script contains auxiliary functions for the plots of the notebooks


# We Generate random colormap using the module created by https://github.com/delestro/rand_cmap

# Generate random colormap
def rand_cmap(nlabels, type='bright', first_color_black=True, last_color_black=False, verbose=True):
    from itertools import cycle # to generate random colors
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """
    from itertools import cycle    
    from matplotlib.colors import LinearSegmentedColormap
    import colorsys
    import numpy as np
    

    if type not in ('bright', 'soft'):
        print ('Please choose "bright" or "soft" for type')
        return

    if verbose:
        print('Number of labels: ' + str(nlabels))

    # Generate color map for bright colors, based on hsv
    if type == 'bright':
        randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                          np.random.uniform(low=0.2, high=1),
                          np.random.uniform(low=0.9, high=1)) for i in range(nlabels)]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2]))

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in range(nlabels)]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Display colorbar
    if verbose:
        from matplotlib import colors, colorbar
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))

        bounds = np.linspace(0, nlabels, nlabels + 1)
        norm = colors.BoundaryNorm(bounds, nlabels)

        cb = colorbar.ColorbarBase(ax, cmap=random_colormap, norm=norm, spacing='proportional', ticks=None,
                                   boundaries=bounds, format='%1i', orientation=u'horizontal')

    return random_colormap




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



def map_gdf_mutualisables(sample, dataframe):
    #this function will return a map and a geodataframe consisting of all mutualisables itineraires for the given sample
    new_cmap = rand_cmap(100, type='bright', first_color_black=False, last_color_black=False, verbose=True)
    gdf=gpd.GeoDataFrame(sample,geometry=sample['start'].map(wkt.loads))
    m= gdf.explore(tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=4,color='black'))

    gdf=gpd.GeoDataFrame(gdf,geometry=gdf['itineraire'].map(wkt.loads))
    m= gdf.explore(m=m,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=2,color='black')) #to build the map
    
    geometry = gdf['cheflieu'].map(wkt.loads)
    cheflieu = gpd.GeoDataFrame(gdf, geometry=geometry, crs = 'EPSG:2154') # we get the center of the cheflieu as a geometry
    cheflieu['buffer'] = cheflieu.geometry.buffer(100000) # create the buffer based on the cheflieu point
    cheflieu = gpd.GeoDataFrame(cheflieu, geometry='buffer')
    print(cheflieu.geometry)
    m = cheflieu.explore(m=m,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=2,color='black'))

    gdf = IsInclude.IsIn_tournee_gdf(gdf,dataframe,100000,1) #we check the allowed itineraires

    gdf = gpd.GeoDataFrame(gdf, geometry=gdf['start_right'].map(wkt.loads), crs='EPSG: 2154')
    m = gdf.reset_index().explore(m=m,tiles='CartoDB positron', cmap = new_cmap,column='id_simulation_right', categorical=True,style_kwds=dict(fill=False, stroke=True,weight=5))
    
    gdf = gpd.GeoDataFrame(gdf, geometry=gdf['itineraire_right'].map(wkt.loads), crs='EPSG: 2154')
    m = gdf.reset_index().explore(m=m,tiles='CartoDB positron', cmap = new_cmap, column='id_simulation_right', categorical=True,
                                style_kwds=dict(opacity=0.5))
    return m, gdf

