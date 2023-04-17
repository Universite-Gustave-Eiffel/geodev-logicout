import jacaard, use_data, IsInclude
from shapely import wkt
import geopandas as gpd
import seaborn as sns


radius=100000
buffer_hull= 1000
type= 1
geo_df= use_data.create_gdf('_simulations_reel_gdf.csv')


empty_list=[]
for i in range (2):
    #range geo_df.shape[0]
    df = jacaard.jacaard_index(geo_df.iloc[[i]],geo_df,radius,buffer_hull,1)
    df = df[df['jaacard']!=0]
    df = df.sort_values(by='jaacard')

    empty_list = empty_list + df[['id_simulation','id_simulation_right','jaacard']].values.tolist()

    

print(empty_list)