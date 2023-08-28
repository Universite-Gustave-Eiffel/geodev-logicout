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


root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory

if __name__ == "__main__":

    print(root)
    root = os.getcwd()
    with open(root+'/trajets_mutualises.csv', mode='r') as file:
        
        calculated=pd.read_csv(file, sep=",",usecols=[0])
        calculated=calculated["id"].tolist()
        print(calculated)

    with open(root+'/data/raw/ranked_mutualisations.csv', mode='r') as file:
        reader = csv.reader(file,delimiter=',')
        next(reader)
        for row in reader:
            if (len(row) >0 and row[1]!=""):

                row_id=str(row[0])+"_" + str(int(eval(row[1])[0][0]))
                if(row_id in calculated):
                    print(row_id + " have already been calculated.")
                else:
                    print(row_id) #delete this line
                    #mutualisation.comparison(int(row[0]),int(eval(row[1])[0][0]),gdf)

     







