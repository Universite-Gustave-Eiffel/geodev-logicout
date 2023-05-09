import use_data
import csv
import pandas as pd
import os
import mutualisation

root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory


gdf = use_data.create_gdf('simulations_reel_gdf.csv', 'itineraire')


with open('./data/raw/ranked_mutualisations.csv', mode='r') as file:
    reader = csv.reader(file,delimiter=',')
    next(reader)
    empty_list=[]
    for row in reader:
        if(row[1]):
            print('xxxx')
            print(int(row[0]) )
            print(int(eval(row[1])[0][0]))
            mutualisation.comparison(int(row[0]),int(eval(row[1])[0][0]),gdf)
            print('bbbbbbb')
               
        
     



