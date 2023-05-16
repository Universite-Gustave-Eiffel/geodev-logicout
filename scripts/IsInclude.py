import geopandas as gpd
from shapely import wkt
import use_data



def IsIn_tournee_gdf(tournee, gdf, dist, type):
    """
    Return a geodataframe containing all the itineraires mutualisables for an itineraire 
    We take 3 steps:
    1 - Take all itineraires from geodataframe are within a buffer of 100km from the row respective cheflieu .
    2 - Verify if we taking a differente user
    if type == 2:
        3 - Verify if the row are within a 100km each one of those itineraires filtered in the step 2
    
    Args:
        tournee {geopandas Geodataframe line}: a row of an geodataframe
        gdf {geopandas Geodataframe}: Geodataframe of the given file name in the directory ../data/raw
        dist {int}: buffer size in meters
        type {int}: 1 => single buffer inclusion | 2 => double buffer inclusion

    Output : 
        gdf_IsInclude {geopandas Geodataframe}: geodataframe containing all the itineraires mutualisables for an itineraire
        or 
        error message {geopandas Geodataframe}: if the 'type' argument is not properly filled in
    """
    # Step 1
    geometry = tournee['cheflieu'].map(wkt.loads)
    cheflieu = gpd.GeoDataFrame(tournee, geometry=geometry, crs = 'EPSG:2154') # we get the center of the cheflieu as a geometry
    cheflieu['buffer'] = cheflieu.geometry.buffer(dist) # create the buffer based on the cheflieu point

    cheflieu = cheflieu.drop(columns=['ID_COM']) # drop the column to do the jointure
    cheflieu = gpd.GeoDataFrame(cheflieu, geometry='buffer') # we set the buffer as the gdf geometry

    geometry_iti = gdf['itineraire'].map(wkt.loads)
    gdf2 = gpd.GeoDataFrame(gdf, geometry=geometry_iti, crs = 'EPSG:2154') #we set the line as a geometry

    gdf_IsInclude = cheflieu.sjoin(gdf2, predicate='contains', how='inner') # we join with lines from the simulations from before the manipulation
    
    # Step 2
    # former mutualisation constraint
    # gdf_IsInclude = gdf_IsInclude[gdf_IsInclude['id_utilisateur_right']!=gdf_IsInclude['id_utilisateur_left']] # filter the users with the same ID
    
    # new mutualisation constraint
    gdf_IsInclude = gdf_IsInclude[gdf_IsInclude['start_left']!=gdf_IsInclude['start_right']] # filter the users with the same starting point 
    gdf_IsInclude = gdf_IsInclude.drop(columns=['index_right']) # drop the column to do the jointure

    # Step 3
    if type == 1:
        return gdf_IsInclude
    
    elif type == 2:
        geometry_itiA = tournee['itineraire'].map(wkt.loads)
        tournee = gpd.GeoDataFrame(tournee, geometry=geometry_itiA, crs = 'EPSG:2154')

        geometry_isin = gdf_IsInclude['cheflieu_right'].map(wkt.loads)
        gdf_IsInclude = gpd.GeoDataFrame(gdf_IsInclude, geometry=geometry_isin, crs = 'EPSG:2154')
        gdf_IsInclude['buffer'] = gdf_IsInclude.geometry.buffer(dist)
        gdf_IsInclude = gpd.GeoDataFrame(gdf_IsInclude, geometry='buffer', crs = 'EPSG:2154')

        gdf_IsInclude = gdf_IsInclude.sjoin(tournee, predicate='contains', how='inner')

        return gdf_IsInclude

    else :
        return "ERROR : the 'type' argument is incorrectly filled in. As a reminder, it can only take a value of 1 or 2."






if __name__ == "__main__":

    # Example of the use of this function

    filename = "simulations_reel_gdf.csv"
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe of the selected csv file
    dist = 100000

    tournee = gdf.iloc[[10]] # choice of a sample in the detaframe

    print(IsIn_tournee_gdf(tournee, gdf, dist, 1).shape[0]) # number of samples that can be shared with the selected sample for simple inclusion
    print(IsIn_tournee_gdf(tournee, gdf, dist, 2).shape[0]) # number of samples that can be shared with the selected sample for double inclusion

    print(gdf[gdf['id_simulation']==1131]) # allows you to obtain a sample according to your 'id_simulation'

