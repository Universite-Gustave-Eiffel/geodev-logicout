import numpy as np
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.exact import solve_tsp_dynamic_programming
import api_logicout
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
    print(RouteA,RouteB)
    merged_coord = np.append(RouteA,RouteB,axis=0)
    #Now we have to optimize this list of coordinates, i.e rearranging them in the right order to minimize the travel time and the distance,
    #starting with the 1st point from A, then going to the 1st point from B
    
    #We're starting by computing the distance matrix
    distance_matrix = great_circle_distance_matrix(merged_coord)
    #We then modify the distance matrix to set the distance between A1 & B1 to zero, so that the algorithm is forced to put them one after the other
    i = np.where(np.isclose(merged_coord, RouteB[0]))
    distance_matrix[0,i] = 0
    #Then we get the permutation list, which is containing the order in which we need to rearrange the indexes from all_coord
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
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
    gdf['itineraire'] = gdf.geometry.to_crs(4326)
    
    trajA = use_data.line_to_coord(
        gdf.loc[gdf['id_simulation']==idA,'itineraire']
    )
    trajB = use_data.line_to_coord(
        gdf.loc[gdf['id_simulation']==idB,'itineraire']
    )
    #Computing the new path
    traj_mutu = route_calculation(trajA,trajB)
    print("Le trajet mutualisé est "+str(traj_mutu))
    
    #We need to stock the data about the prodcuer A vehicle, since it will be the one who takes in charge both products
    V_info = []
    with open('./data/raw/simulation.csv', mode='r') as file:
        reader = csv.reader(file,delimiter=';')
        #Ignore the header
        next(reader)
        for row in reader:
            if int(row[0]) == idA:
                V_info.append(row[4])   #id_vehicule (str)
                V_info.append(row[9])   #tps_autres_activités (str)
                temp = float(row[10])/float(row[7]) #Total tps_arret / nb_pts_arret (float)
                V_info.append('00:'+str(int(temp))+':00')
                if 'frigorifique' in row[6]: #Frigo (boolean) --> True if the vehicle is refrigirated
                    V_info.append(True)
                else:
                    V_info.append(False)
                if 'Fourgonnette' in row[5]: #Type of vehicle (relative to its size) (str)
                    V_info.append('FTTE')
                elif 'Fourgon' in row[5]:
                    V_info.append('F')
                elif 'Grand fourgon' in row[5]:
                    V_info.append('GF')
    print(V_info)
    #Sending the new path to the logicout API with A's vehicule data, since he will carry the products
    results = api_logicout.calcul_couts(traj_mutu,vehicule=V_info[0],tps_act=V_info[1],tps_moy=V_info[2],frigo=V_info[3],v_type=V_info[4])
    #Gathering the data from the two original paths
    #id,tps,dist,CO_g,COV_g,NOX_g,NH3_g,PB_g,SO2_g,PS_g,CO2_g,N2O_g,CH4_g,cout_collectif
    dataA = [idA,0,0,0,0,0,0,0,0,0,0,0,0,0]
    dataB = [idB,0,0,0,0,0,0,0,0,0,0,0,0,0]
    with open('./data/raw/trajet.csv', mode='r') as file:
        reader = csv.reader(file)
        #Ignore the header
        next(reader)
        for row in reader:
            if int(row[1]) == idA:
                dataA[1]+=float(row[6])
                dataA[2]+=float(row[5])
                dataA[3]+=float(row[12])
                dataA[4]+=float(row[13])
                dataA[5]+=float(row[14])
                dataA[6]+=float(row[15])
                dataA[7]+=float(row[16])
                dataA[8]+=float(row[17])
                dataA[9]+=float(row[18])
                dataA[10]+=float(row[19])
                dataA[11]+=float(row[20])
                dataA[12]+=float(row[21])
                dataA[13]+=float(row[22])
            if int(row[1]) == idB:
                dataB[1]+=float(row[6])
                dataB[2]+=float(row[5])
                dataB[3]+=float(row[12])
                dataB[4]+=float(row[13])
                dataB[5]+=float(row[14])
                dataB[6]+=float(row[15])
                dataB[7]+=float(row[16])
                dataB[8]+=float(row[17])
                dataB[9]+=float(row[18])
                dataB[10]+=float(row[19])
                dataB[11]+=float(row[20])
                dataB[12]+=float(row[21])
                dataB[13]+=float(row[22])
    field_names = ['id','idA','idB','tps_min','distance_km','cout','CO_g','COV_g','NOX_g','NH3_g','PB_g','SO2_g','PS_g','CO2_g','N2O_g','CH4_g','cout_collectif']
    with open('trajets_mutualises.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file,fieldnames=field_names)
        writer.writeheader()
        writer.writerow(
            {'id': str(idA)+"_"+str(idB) ,
             'idA': idA ,
             'idB': idB ,
             'tps_min': results['temps_passe']['total'] ,
             'distance_km': results['kilometrage'] ,
             'cout': results['couts']['total'] ,
             'CO_g': results['emissions']['CO'] ,
             'COV_g': results['emissions']['COV'] ,
             'NOX_g': results['emissions']['NOX'] ,
             'NH3_g': results['emissions']['NH3'] ,
             'PB_g': results['emissions']['PB'] ,
             'SO2_g': results['emissions']['SO2'] ,
             'PS_g': results['emissions']['PS'] ,
             'CO2_g': results['emissions']['CO2'] ,
             'N2O_g': results['emissions']['N2O'] ,
             'CH4_g': results['emissions']['CH4'],
             'cout_collectif': results['cout_collectif']}
        )     
    return(results,dataA,dataB)

if __name__ == "__main__":

    filename = "simulations_reel_gdf.csv"
    gdf = use_data.create_gdf(filename, 'itineraire')
    a,b,c = comparison(16316,11449,gdf)
    
    print("Données sur le trajet mutualisé entre le n°"+str(b[0])+" et le n°"+str(c[0])+" :" + str(a)+"\n Données sur le trajet n°"+str(b[0])+": "+str(b)+"\n Données sur le trajet n°"+str(c[0])+" : "+str(c))

    ###print(route_calculation(TestA,TestB))