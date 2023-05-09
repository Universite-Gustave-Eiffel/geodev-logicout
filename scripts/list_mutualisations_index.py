import use_data, IsInclude, indexes
from shapely import wkt, hausdorff_distance
import geopandas as gpd
import csv
import os
import numpy as np
import warnings
warnings.filterwarnings('ignore')

root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory


radius_=100000
buffer_hull_= 1000
type_= 1
geo_dataframe_logicout = use_data.create_gdf('simulations_reel_gdf.csv','cheflieu')
aire = np.pi*radius_**2



def calculate_mutualisations(geo_df,dist,buffer_hull,type):
    """
    Return a list containing a row for each itineraire in a geodataframe, with their ids, the ids of 
    their mutualisables itineraires with the respective indexes,

    Args:

        geodataframe {geopandas Geodataframe}: name of file in the directory ../data/raw
        dist {int}: buffer size in meters´
        buffer_hull {int}: size of the buffer applied to the lines before generating the convex hull
        type {int}: type of verification of itineraires within buffer : 1->simple 2->double
    """    


    mutualisations=[]
    for i in range (geo_df.shape[0]):
   
        row = geo_df.iloc[[i]] # we take the current itineraire
        
        gdf= IsInclude.IsIn_tournee_gdf(row,geo_df,dist,type) # we take all mutualisables itineraires

        #we chech if the dataframe of the mutualisables itineraires isn't empty
        if (gdf.shape[0]>0):  
            gdf = indexes.jacaard_index(row, gdf,buffer_hull) # we apply the jaacard index

            # we calculate the distance between their starting points and adjust the geodataframes
            gdf = indexes.dist_start(row,gdf) 
            
            # We calculate the maximum distance between the itineraire and his mutualisables counterparts
            gdf = indexes.max_distance(row,gdf) 
            
            # We calculate our index
            gdf = indexes.index(gdf,aire) 

            # we prepare to save the results in a csv , sorted by the index for the best mutualisations
            gdf = gdf.sort_values(by=['index_with_jaacard'])
            row = [[geo_df['id_simulation'].iloc[[i]].values[0],gdf[['id_simulation_right','jaacard','start_distance','max_distance','index','index_with_jaacard']].values.tolist()]]
            mutualisations = mutualisations + row
        
        #if there aren't any mutualisable itineraire
        else: 
            mutualisations = mutualisations + [[geo_df['id_simulation'].iloc[[i]].values[0],""]]
    return mutualisations


ranked_mutualisations = calculate_mutualisations(geo_dataframe_logicout,radius_,buffer_hull_,type_)




if __name__ == "__main__":

    with open(root + "/data/raw/" + 'ranked_mutualisations.csv', 'w') as f:
        
        # using csv.writer method from CSV package
        write = csv.writer(f)
        fields = ['id_simulation', 'mutualisations'] 
        write.writerow(fields)
        write.writerows(ranked_mutualisations)



