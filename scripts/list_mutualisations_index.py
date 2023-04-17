import jacaard, use_data, IsInclude
from shapely import wkt
import geopandas as gpd
import csv
import os

root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory


radius_=100000
buffer_hull_= 1000
type_= 1
geo_df_= use_data.create_gdf('_simulations_reel_gdf.csv')



def calculate_mutualisations(geo_df, dist,buffer_hull,type):
    """
    Return a list containing a row for each itineraire in a geodataframe, with their ids, the ids of their mutualisables itineraires with the respective jaacard indexes,



    Args:

        geodataframe {geopandas Geodataframe}: name of file in the directory ../data/raw
        dist {int}: buffer size in meters´
        buffer_hull {int}: size of the buffer applied to the lines before generating the convex hull
        type {int}: type of verification of itineraires within buffer : 1->simple 2->double
    """    


    empty_list=[]
    for i in range (geo_df.shape[0]):
    
        df = jacaard.jacaard_index(geo_df.iloc[[i]],geo_df,dist,buffer_hull,type)
        #df = df[df['jaacard']!=0]
        df = df.sort_values(by='jaacard')
        row = [[geo_df['id_simulation'].iloc[[i]].values[0],df[['id_simulation_right','jaacard']].values.tolist()]]
        empty_list = empty_list + row
    return empty_list


ranked_mutualisations = calculate_mutualisations(geo_df_,radius_,buffer_hull_,type_)




if __name__ == "__main__":

    with open(root + "/data/raw/" + 'ranked_mutualisations.csv', 'w') as f:
        
        # using csv.writer method from CSV package
        write = csv.writer(f)
        fields = ['id_simulation', 'mutualisations'] 
        write.writerow(fields)
        write.writerows(ranked_mutualisations)



