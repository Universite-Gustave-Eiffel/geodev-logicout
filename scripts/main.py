import use_data
import csv
import pandas as pd
import os
import mutualisation
from tqdm import tqdm

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#   Attention : Running this script will request the LOGICOUT API 
#   1 time per row in the database, for the best ranked itinerary to mutualise
#
#   The code is commented to ensure that this doesn't happens by chance
#________________________________________________________________________________


#root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory

block_size = 2 # number of travels to compare
skipped_row  = 0
if __name__ == "__main__":

    root = os.getcwd()

    gdf = use_data.create_gdf('simulations_reel_gdf.csv', 'itineraire')

    pooled_travels = root+'/data/output/trajets_mutualises.csv'

    # get already computed pooled travels
    computed_travels = []
    if os.path.exists(pooled_travels):
        #print("open pooled travels")    
        with open(pooled_travels, mode='r') as file:
            computed_travels = pd.read_csv(file, sep=",",usecols=[0])
            computed_travels = computed_travels["id"].tolist()  

    with open(root+'/data/raw/ranked_mutualisations.csv', mode='r') as file:
        reader = csv.reader(file,delimiter=',')
        next(reader)
        row_counter = 0

        for row in reader:
            if (len(row) >0 and row[1]!=""):

                row_id=str(row[0])+"_" + str(int(eval(row[1])[0][0]))
                if(row_id in computed_travels):
                    #print(f"{row_id} pooled travel have been already computed.")
                    skipped_row += 1
                else:
                    if row_counter < block_size:
                        print(f"Computing {row_id}")
                        #print(row_id) #delete this line
                        mutualisation.comparison(int(row[0]),int(eval(row[1])[0][0]),gdf)
                        row_counter +=1
                        #print(row_counter)
                    else:
                        #print("Stopping loop")
                        break
                        
        print(f"{row_counter} pooled travels have been computed and compared in this run. {row_counter + skipped_row} travels in total")

     







