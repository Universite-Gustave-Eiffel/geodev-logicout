import pandas as pd
import numpy as np
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.exact import solve_tsp_dynamic_programming
import api_logicout
import geopandas as gpd
import use_data
import csv

def route_calculation(RouteA,RouteB):
    """
    Takes two routes and combine them into a new one, starting with the first point of A, then the first point of B, and then the most optimized path which visit each point once.
    It returns both the optimized path with or without the first point at the end.
    NB : It considers that the path will be returning at the path in both cases, it just won't put the starting point at the end.
    Args:
        RouteA (Array): An array of coordinates /!\ Latitude THEN longitude
        RouteB (Array): An array of coordinates /!\ Latitude THEN longitude
    """
    #We merge the two sets of coordinates together
    merged_coord = np.append(RouteA,RouteB,axis=0)
    print(merged_coord)
    #Now we have to optimize this list of coordinates, i.e rearranging them in the right order to minimize the travel time and the distance,
    #starting with the 1st point from A, then going to the 1st point from B
    
    #We're starting by computing the distance matrix
    distance_matrix = great_circle_distance_matrix(merged_coord)
    #We then modify the distance matrix to set the distance between A1 & B1 to zero, so that the algorithm is forced to put them one after the other
    i = np.where(np.isclose(merged_coord, RouteB[0]))
    distance_matrix[0,i] = 0
    print(distance_matrix)
    #Then we get the permutation list, which is containing the order in which we need to rearrange the indexes from all_coord
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    print(permutation,distance)
    #We then rearrange the all_coord array into a new array
    rearranged_coord = np.zeros(np.shape(merged_coord))
    for i in range(len(permutation)):
        rearranged_coord[i] = merged_coord[permutation[i]]
    #We just have to put back the first point of A at the end.
    path = rearranged_coord
    
    return(path)

def comparison(idA,idB,gdf):
    """
    Takes the IDs of two routes and returns the time,money and gas emission saved

    Args:
        idA (int): The index of the first route(A)
        idB (int): The index of the second route(B)
        gdf (geodataframe): A gdf containing data on all the routes (created from simulation_reel_gdf.csv)
    """
    #Getting the array containing the coordinates of the two routes
    trajA = use_data.line_to_coord(
        gdf[gdf['id_simulation']==idA]['itineraire']
        )
    trajB = use_data.line_to_coord(
        gdf[gdf['id_simulation']==idB]['itineraire']
        )
    #Computing the new path
    traj_mutu = route_calculation(trajA,trajB)
    #Sending the new path to the logicout API
    ###results = api_logicout.calcul_couts(traj_mutu)
    #Gathering the data from the two original paths
    dataA = []
    dataB = []
    with open('trajet.csv', mode='r') as file:
        reader = csv.reader(file)
        
        #Ignore the header
        next(reader)
        for row in reader:
            if row[1] == idA:
                dataA = row
            if row[1] == idB:
                dataB = idB

if __name__ == "__main__":

    TestA = np.array([
        [50.63194,3.0575],
        [50.28917,2.78],
        [50.37083,3.07917]
        ])
    TestB = np.array([
        [49.61694,0.75306],
        [48.850322,2.308333],
        [48.99056,1.71667]
        ])

    ###print(route_calculation(TestA,TestB))