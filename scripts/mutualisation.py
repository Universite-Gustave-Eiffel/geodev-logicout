import numpy as np
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing
import api_logicout
import use_data
import csv
import os

root = os.path.join(os.path.dirname( __file__ ), os.pardir)

# Path to output files
gains_file = 'data/output/gains.csv'
pooled_travels = 'data/output/trajets_mutualises.csv'

def route_calculation(RouteA,RouteB):
    """
    Takes two routes and combine them into a new one, starting with the first point of A, then the first point of B, and then the most optimized path which visit each point once.
    It returns both the optimized path with or without the first point at the end.
    NB : It considers that the path will be returning at the path in both cases, it just won't put the starting point at the end.
    Args:
        RouteA (Array): An array of coordinates /!\ Latitude THEN longitude
        RouteB (Array): An array of coordinates /!\ Latitude THEN longitude
    
    Returns the new path as a Numpy ndarray
    """
    #We merge the two sets of coordinates together
    merged_coord = np.append(RouteA,RouteB,axis=0)
    #Now we have to optimize this list of coordinates, i.e rearranging them in the right order to minimize the travel time and the distance,
    #starting with the 1st point from A, then going to the 1st point from B
    
    #We're starting by computing the distance matrix
    distance_matrix = great_circle_distance_matrix(merged_coord)
    #We then modify the distance matrix to set the distance between A1 & B1 to zero, so that the algorithm is forced to put them one after the other
    #i = np.where(np.isclose(merged_coord, RouteB[0]))
    i = np.where((merged_coord[:, 0] == RouteB[0][0]) & (merged_coord[:, 1] == RouteB[0][1]))[0][0]
    distance_matrix[0,i] = 0
    #Then we get the permutation list, which is containing the order in which we need to rearrange the indexes from all_coord
    #permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    permutation, distance = solve_tsp_simulated_annealing(distance_matrix)

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
    
    Writes in trajets_mutualises.csv the pooled travels and in gains.csv, 
    the difference between the sum of all emissions and cost of the two original travels
    and thoses of the pooled travel.

    Returns the emissions and costs of the pooled travel and of the two original travels
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
    #print('Le trajet mutualisé est'+str(traj_mutu))
    
    #We need to stock the data about the prodcuer A vehicle, since it will be the one who takes in charge both products
    V_info = []
    with open(root+'/data/raw/simulation.csv', mode='r') as file:
        reader = csv.reader(file,delimiter=';')
        #Ignore the header
        next(reader)
        for row in reader:
            if int(row[0]) == idA:
                CostA = float(row[21])
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
                else:
                    V_info.append('GF')
            if int(row[0]) == idB:
                CostB = float(row[21])
    #print(V_info)
    #print(CostA,CostB)
    #Sending the new path to the logicout API with A's vehicule data, since he will carry the products

    results = {'parametres_vehicule': {'type_vehicule': 'Vehicule utilitaire frigorifique < 3,5 t', 'infos_vehicule': 'Grand fourgon diesel Euro 4', 'cout_vehicule_forfait': 0.0, 'cout_vehicule_km': 0.5759000000000001}, 'couts': {'total': 259.61049843333336, 'vehicule': 181.40216510000002, 'conduite': 50.708333333333336, 'livraison': 5.0, 'autres_activites': 22.5, 'autres_couts': 0.0}, 'temps_passe': {'total': 312.83333333333337, 'conduite': 202.83333333333334, 'livraison': 20.0, 'autre': 90.0}, 'kilometrage': 314.989, 'emissions': {'COV': 11.024615, 'CO2': 79981.376902, 'NH3': 0.3779868, 'CO': 118.120875, 'NOX': 261.755859, 'CH4': 0.0626505765659207, 'PB': 0.00131350413, 'PS': 12.8830501, 'N2O': 2.834901, 'SO2': 0.07559736}, 'cout_collectif': 5.883212963129608}
    results = api_logicout.calcul_couts(traj_mutu,vehicule=V_info[0],tps_act=V_info[1],tps_moy=V_info[2],frigo=V_info[3],v_type=V_info[4])

    #Gathering the data from the two original paths
    #id,tps,dist,CO_g,COV_g,NOX_g,NH3_g,PB_g,SO2_g,PS_g,CO2_g,N2O_g,CH4_g,cout_collectif
    dataA = [idA,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    dataB = [idB,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    with open(root +'/data/raw/trajet.csv', mode='r') as file:
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
                dataA[14] = CostA
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
                dataB[14] = CostB

    field_names = ['id','idA','idB','tps_min','distance_km','cout','CO_g','COV_g','NOX_g','NH3_g','PB_g','SO2_g','PS_g','CO2_g','N2O_g','CH4_g','cout_collectif']
    
    file_exist  =  os.path.exists(pooled_travels) # test if file already exist
    with open(pooled_travels, mode='a', newline='') as file:
        writer = csv.DictWriter(file,fieldnames=field_names)

        if not file_exist : # print csv header if new file, otherwise do nothing
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


    gains_file_exist  =  os.path.exists(gains_file) # test if file already exist

    with open(gains_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file,fieldnames=field_names)

        if not gains_file_exist : # print csv header if new file, otherwise do nothing
            writer.writeheader()
            
        writer.writerow(
            {'id': str(idA)+"_"+str(idB) ,
             'idA': idA ,
             'idB': idB ,
             'tps_min': (dataA[1]+dataB[1])-results['temps_passe']['total'] ,
             'distance_km': (dataA[2]+dataB[2])+results['kilometrage'] ,
             'cout': (CostA+CostB)-results['couts']['total'] ,
             'CO_g': (dataA[3]+dataB[3])-results['emissions']['CO'] ,
             'COV_g': (dataA[4]+dataB[4])-results['emissions']['COV'] ,
             'NOX_g': (dataA[5]+dataB[5])-results['emissions']['NOX'] ,
             'NH3_g': (dataA[6]+dataB[6])-results['emissions']['NH3'] ,
             'PB_g': (dataA[7]+dataB[7])-results['emissions']['PB'] ,
             'SO2_g': (dataA[8]+dataB[8])-results['emissions']['SO2'] ,
             'PS_g': (dataA[9]+dataB[9])-results['emissions']['PS'] ,
             'CO2_g': (dataA[10]+dataB[10])-results['emissions']['CO2'] ,
             'N2O_g': (dataA[11]+dataB[11])-results['emissions']['N2O'] ,
             'CH4_g': (dataA[12]+dataB[12])-results['emissions']['CH4'],
             'cout_collectif': (dataA[13]+dataB[13])-results['cout_collectif']}
        )         
    return(results,dataA,dataB)

if __name__ == "__main__":

    filename = "simulations_reel_gdf.csv"
    gdf = use_data.create_gdf(filename, 'itineraire')
    a,b,c = comparison(3474,8680,gdf)
    print("\n\n\nGains pour le trajet mutualisé entre le trajet n°"+str(b[0])+" et le n°"+str(c[0])+" :\n"
          +"Temps gagné (en min) : "+ str(b[1]+c[1]-a['temps_passe']['total'])+"\n"
          +"Kilométrage gagné : "+str(b[2]+c[2]-a['kilometrage'])+"\n"
          +"Gain économique (en €) : "+str(b[14]+c[14]-a['couts']['total'])+"\n"
          +"Gain CO2 (en g) : "+str(b[10]+c[10]-a['emissions']['CO2'])+"\n\n\n")
