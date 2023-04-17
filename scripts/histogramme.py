import matplotlib.pyplot as plt
import use_data
import IsInclude



def histo(filename, dictFilename, dist, type, dictType):
    gdf = use_data.create_gdf(filename) # dataframe du fichier csv choisi
    n = gdf.count()[0] # number of total rounds
    A = []
    for i in range(n):
        tournee = gdf.iloc[[i]]
        gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, dist, type)
        nbrMutu = gdf_IsInclude.count()[0]
        A.append(nbrMutu)

    # affichage de l'histogramme
    plt.hist(A,bins=20,color="blue",edgecolor="gray",label="histogramme")
    plt.title('Histogramme du nombre de mutualisations possibles : tournées '+dictFilename[filename])
    plt.xlabel('Nombre de tournées dans un rayon de '+str(dist*1e-3)+' km pour des utilisateurs différents ('+dictType[type]+' inclusion)')
    plt.ylabel('Fréquence')
    plt.rcParams['svg.fonttype'] = 'none'
    plt.show()
    return 'Histogramme [ '+dictFilename[filename]+' '+dictType[type]+' '+str(dist*1e-3)+' ] tracé !'






if __name__ == "__main__":
    filename = ["simulations_reel_gdf.csv", "simulations_gdf.csv"]
    dictFilename = {"simulations_reel_gdf.csv": "reelles", "simulations_gdf.csv": "quelconques"}
    dist = [50e3, 100e3, 150e3]
    typeIsIn = [1, 2]
    dictType = {1:"simple", 2:"double"}

    for file in filename:
        for d in dist:
            for type in typeIsIn:
                print(histo(file, dictFilename, d, type, dictType))



