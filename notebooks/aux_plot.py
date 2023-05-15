import sys  
sys.path.insert(0, '../scripts')
import numpy as np
import indexes, use_data, IsInclude, mutualisation
import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.geometry import LineString, Point
import ast


# This script contains auxiliary functions for the plots of the notebooks




# Generate random colormap using the module created by https://github.com/delestro/rand_cmap
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
    """Return all mutualisations for a given itinerary

    Args:
        sample_itineraire (_type_): _description_
        geodataframe (_type_): _description_
        radius (_type_): _description_
        buffer_hull (_type_): _description_
        type (_type_): _description_
        area (_type_): _description_

    Returns:
        _type_: _description_
    """    

    sample_itineraire = use_data.get_itineraire(sample_itineraire,geodataframe)
    gdf = IsInclude.IsIn_tournee_gdf(sample_itineraire,geodataframe,radius,type) #verify all the mutualisables itineraires
    gdf = indexes.jacaard_index(sample_itineraire, gdf,buffer_hull) # we apply the jaacard index
    gdf = indexes.dist_start(sample_itineraire,gdf) # we calculate the distance between their starting points
    gdf = indexes.max_distance(sample_itineraire,gdf) # We calculate the maximum distance between the itineraire and his mutualisables counterparts
    gdf = indexes.index(gdf,area) # We calculate the index of distance

    return gdf

def plot_mutualisations(id, dataframe,**parameters):
    """Auxiliary function to plot all the possible mutualisations according to the parameters

    Args:
        id (int): Id number of the the chosen itinerary
        dataframe (geodataframe): name of file in the directory ../data/raw
        parameters (dict): dictionary with the parameters for the algorithm to run

    Returns:
        _type_: _description_
    """    
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
    """Returns an folium map and a dataframe containing the mutualisations

    Args:
        id (int): Id number of the the chosen itinerary
        dataframe (geodataframe): name of file in the directory ../data/raw
        parameters (dict): dictionary with the parameters for the algorithm to run

    Returns:
        best_mutualisations (geodataframe): Dataframe with their best ranked simulations
        m(folium map): map of those simulations

    """
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

    """Returns an folium map and a dataframe containing the mutualisations with the index of distance = 0 

    Args:
        id (int): Id number of the the chosen itinerary
        dataframe (geopandas Geodataframe): name of file in the directory ../data/raw
        parameters (dict): dictionary with the parameters for the algorithm to run

    Returns:
        best_mutualisations (geodataframe): Dataframe with their best ranked simulations
        m(folium map): map of those simulations

    """    

    sample = use_data.get_itineraire(id,dataframe)
    sample_gdf = mutualisations_with_index(id, dataframe,**parameters)
    best_mutualisations = sample_gdf[['id_simulation_right','index','index_with_jaacard']].sort_values(by='index_with_jaacard').head()
    best_mutualisations = best_mutualisations.sort_values(by='id_simulation_right')
    best_mutualisations_ind = best_mutualisations['index_with_jaacard'].values.tolist()
    #best_mutualisations_ind.append(0)
    itineraires_to_plot = best_mutualisations['id_simulation_right'].values
    best_mutualisations_gdf = dataframe[dataframe['id_simulation'].isin(itineraires_to_plot)]
    #best_mutualisations_gdf = gpd.GeoDataFrame( pd.concat( [best_mutualisations_gdf,sample], ignore_index=True) )
    m = sample.explore(tiles='CartoDB positron',cmap = "plasma",column='id_simulation',categorical=True,style_kwds=dict(color='black',fill=False, stroke=True,weight=15,opacity=0.3))
    sample = gpd.GeoDataFrame(sample,geometry=sample['itineraire'].map(wkt.loads))
    m= sample.explore(m=m,tiles='CartoDB positron',cmap = "plasma",column='id_simulation',categorical=True,style_kwds=dict(color='black',fill=False, stroke=True,weight=10,opacity=0.4))
    best_mutualisations_gdf['final_index']= best_mutualisations_ind
    best_mutualisations_gdf=gpd.GeoDataFrame(best_mutualisations_gdf,geometry=best_mutualisations_gdf['start'].map(wkt.loads))
    m= best_mutualisations_gdf.explore(m=m,tiles='CartoDB positron',cmap = "plasma",column='id_simulation',categorical=True,style_kwds=dict(fill=False, stroke=True,weight=5))
    best_mutualisations_gdf=gpd.GeoDataFrame(best_mutualisations_gdf,geometry=best_mutualisations_gdf['itineraire'].map(wkt.loads))
    m= best_mutualisations_gdf.explore(m=m,tiles='CartoDB positron',cmap = "plasma",column='id_simulation',categorical=True,style_kwds=dict(fill=False, stroke=True,weight=3))

    return best_mutualisations,m

def map_gdf_mutualisables(sample, dataframe):

    """
    Returns a folium map and a geodataframe with all mutualisable itineraries for a given sample:
    
    sample: original itinerary
    dataframe: mutualised itineraries

    Args:
        a (Geopanda's gdf): geodataframe of the itinerary a
        b (Geopanda's gdf): geodataframe of the itinerary b

    Returns:

        m(folium map): map of chosen sample
        gdf (geodataframe): Geodataframe with all the simulations candidates
        
    """    

    new_cmap = rand_cmap(100, type='bright', first_color_black=False, last_color_black=False, verbose=True)
    gdf=gpd.GeoDataFrame(sample,geometry=sample['start'].map(wkt.loads))
    m= gdf.explore(tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=4,color='black'))
    gdf=gpd.GeoDataFrame(gdf,geometry=gdf['itineraire'].map(wkt.loads))
    m= gdf.explore(m=m,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=2,color='black')) #to build the map
    geometry = gdf['cheflieu'].map(wkt.loads)
    cheflieu = gpd.GeoDataFrame(gdf, geometry=geometry, crs = 'EPSG:2154') # we get the center of the cheflieu as a geometry
    cheflieu['buffer'] = cheflieu.geometry.buffer(100000) # create the buffer based on the cheflieu point
    cheflieu = gpd.GeoDataFrame(cheflieu, geometry='buffer')
    m = cheflieu.explore(m=m,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=2,color='black'))
    gdf = IsInclude.IsIn_tournee_gdf(gdf,dataframe,100000,1) #we check the allowed itineraires
    gdf = gpd.GeoDataFrame(gdf, geometry=gdf['start_right'].map(wkt.loads), crs='EPSG: 2154')
    m = gdf.reset_index().explore(m=m,tiles='CartoDB positron', cmap = new_cmap,column='id_simulation_right', categorical=True,style_kwds=dict(fill=False, stroke=True,weight=5))
    gdf = gpd.GeoDataFrame(gdf, geometry=gdf['itineraire_right'].map(wkt.loads), crs='EPSG: 2154')
    m = gdf.reset_index().explore(m=m,tiles='CartoDB positron', cmap = new_cmap, column='id_simulation_right', categorical=True,
                                style_kwds=dict(opacity=0.5))
    return m, gdf

def plot_itineraires_and_mutualisation(a,b):
    """
    Returns two folium maps containing two itineraries and their mutualisation:


    Args:
        a (Geopanda's gdf): geodataframe of the itinerary a
        b (Geopanda's gdf): geodataframe of the itinerary b

    
    Returns:
        m1 (folium map): original itineraries
        m2 (folium map): mutualised itineraries
    """
    
    # loads the GDF with the geometry of their itineraries
    it1 = gpd.GeoDataFrame(a, geometry=a['itineraire'].map(wkt.loads))
    it2 = gpd.GeoDataFrame(b, geometry=b['itineraire'].map(wkt.loads))

    #transform their projection to match the projection of the API Logicout
    it1['itineraire_4326'] = it1.geometry.to_crs(4326)
    it2['itineraire_4326'] = it2.geometry.to_crs(4326)
    it1 = gpd.GeoDataFrame(it1, geometry='itineraire_4326')
    it2 = gpd.GeoDataFrame(it2, geometry='itineraire_4326')

    #transform the itineraries in lists of points and calcul the mutualisation
    it1_points = it1.geometry.map(use_data.coord_lister).tolist()
    it2_points = it2.geometry.map(use_data.coord_lister).tolist()
    mutu = mutualisation.route_calculation(it1_points[0],it2_points[0])


    #Create a dataframe for the new itinerary
    mutu_geom = LineString(mutu)
    d = {'mutualisation': [1] }
    mutu_gdf = pd.DataFrame(data=d)
    mutu_gdf['itineraire']= mutu_geom
    mutu_gdf = gpd.GeoDataFrame(d,crs='epsg:4326', geometry=[mutu_geom])

    #start the construction of the plots


    m1 = it1.explore(color='red',tiles='CartoDB positron') # red line of the itinerary A
    m1 = it2.explore(m=m1,color='blue',tiles='CartoDB positron') # blue line of the itinerary B
    m2 = mutu_gdf.explore(color='green',tiles='CartoDB positron') # green line of the mutualised itinerary

    it1point = gpd.GeoDataFrame(it1, geometry=it1['start'].map(wkt.loads)) # To highlight the start of A in both maps
    m1 = it1point.explore(m=m1,color='red',tiles='CartoDB positron',style_kwds=dict(fill=True, stroke=True,weight=7))
    m2 = it1point.explore(m=m2,color='red',tiles='CartoDB positron',style_kwds=dict(fill=True, stroke=True,weight=7))

    it2point = gpd.GeoDataFrame(it2, geometry=it2['start'].map(wkt.loads)) # To highlight the start of B in both maps
    m1 = it2point.explore(m=m1,color='blue',tiles='CartoDB positron',style_kwds=dict(fill=True, stroke=True,weight=7))
    m2 = it2point.explore(m=m2,color='blue',tiles='CartoDB positron',style_kwds=dict(fill=True, stroke=True,weight=7))

  
    #to highlight the steps in both maps

    #Steps of A
    data = {'coors':it1_points[0]}
    df = pd.DataFrame.from_dict(data)
    df['geometry'] = df.coors.apply(Point)
    gdf = gpd.GeoDataFrame(df)
    m1=gdf.explore(m=m1,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=2,color='red'))
    m2=gdf.explore(m=m2,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=2,color='red'))

    #Steps of B
    data = {'coors':it2_points[0]}
    df = pd.DataFrame.from_dict(data)
    df['geometry'] = df.coors.apply(Point)
    gdf = gpd.GeoDataFrame(df)
    m1=gdf.explore(m=m1,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=2,color='blue'))
    m2=gdf.explore(m=m2,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=2,color='blue'))


    return m1,m2



def plot_itineraires_convex_hull(a,b):
    """
    Returns a folium maps with the itineraries a and b and their convex hulls

    Args:
        a (Geopanda's gdf): geodataframe of the itinerary a
        b (Geopanda's gdf): geodataframe of the itinerary b

    Returns:
        m (folium map): map of the convex hulls
    """

    #line of a
    it1 = gpd.GeoDataFrame(a,geometry=a['itineraire'].map(wkt.loads)) 
    m = it1.explore(tiles='CartoDB positron',color='red') #line of the itinerary A in red
    it1_points = it1.geometry.map(use_data.coord_lister).tolist() #save the points of the itinerary a for the highlight

    #line of b
    it2 = gpd.GeoDataFrame(b,geometry=b['itineraire'].map(wkt.loads)) 
    m = it2.explore(m=m,tiles='CartoDB positron',color='blue')
    it2_points = it2.geometry.map(use_data.coord_lister).tolist() #save the points of the itinerary b for the highlight
    

    #convex hulls
    it1 = gpd.GeoDataFrame(it1,geometry=it1.geometry.buffer(1000).convex_hull)
    it2 = gpd.GeoDataFrame(it2,geometry=it2.geometry.buffer(1000).convex_hull) 
    m = it1.explore(m=m,tiles='CartoDB positron',style_kwds=dict(fill=True,fillOpacity=0.1, stroke=False,color='red'))
    m = it2.explore(m=m,tiles='CartoDB positron',style_kwds=dict(fill=True,fillOpacity=0.1, stroke=False,color='blue'))

    #Starting points
    it1 =gpd.GeoDataFrame(it1,geometry=it1['start'].map(wkt.loads))
    m= it1.explore(m=m,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=5,color='red'))
    it2 =gpd.GeoDataFrame(it2,geometry=it2['start'].map(wkt.loads))
    m= it2.explore(m=m,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=5,color='blue'))

    #to highlight the steps 

    #Steps of A
    data = {'coors':it1_points[0]}
    df = pd.DataFrame.from_dict(data)
    df['geometry'] = df.coors.apply(Point)
    gdf = gpd.GeoDataFrame(df,crs = 'EPSG:2154')
    m=gdf.explore(m=m,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=2,color='red'))
   
    #Steps of B
    data = {'coors':it2_points[0]}
    df = pd.DataFrame.from_dict(data)
    df['geometry'] = df.coors.apply(Point)
    gdf = gpd.GeoDataFrame(df,crs = 'EPSG:2154')
    m=gdf.explore(m=m,tiles='CartoDB positron',style_kwds=dict(fill=False, stroke=True,weight=2,color='blue'))
 
    return m