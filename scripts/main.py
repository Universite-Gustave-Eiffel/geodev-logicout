import use_data
import csv
import pandas as pd
import os
root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory



ranked_simulations = pd.read_csv(root + "/data/raw/ranked_mutualisations.csv")
gdf = use_data.create_gdf('simulations_reel_gdf.csv', 'itineraire')

gdf['coordinates'] = gdf.apply(lambda x : list(x.coords))
print(gdf['coordinates'])