import matplotlib.pyplot as plt
import use_data
import IsInclude



def histo(filename, dictFilename, dist, type, dictType):
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe du fichier csv choisi
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




def comparaison(filename, dist, type):
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe du fichier csv choisi
    n = gdf.count()[0] # number of total rounds
    nbr_sans_mutu = 0
    for i in range(n):
        tournee = gdf.iloc[[i]]
        gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, dist, type)
        if gdf_IsInclude.count()[0] == 0:
            nbr_sans_mutu += 1
    
    return [type, dist, n, nbr_sans_mutu]

def histo_0_mutu_bis():
    x1 = [1, 2, 2, 3, 4, 4, 4]
    x2 = [1, 1, 1, 2, 2, 3, 3]
    bins = [x + 0.5 for x in range(0, 4)]
    plt.hist([x1, x2], bins = bins, color = ['deepskyblue', 'mediumorchid'], label = ['simple', 'double'])
    plt.ylabel("% de tournées n'ayant aucune tournées dans son rayon")
    plt.xlabel('km du rayon considéré')
    plt.title('Comparaison entre une simple et une double inclusion, pour des rayons différents')
    plt.legend()
    plt.show()
    return 'Histogramme tracé !'

def histo_0_mutu():
    dist = [50e3, 100e3, 150e3]
    typeIsIn = [1, 2]
    dictType = {1:"simple", 2:"double"}

    # Préparation de la figure
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])

    etiquettes = ['C', 'C++', 'Java', 'Python', 'PHP']
    valeurs = [23, 17, 35, 29, 12]

    # Affichage des données
    ax.bar(etiquettes, valeurs)

    plt.title("Histogramme")  # Titre du graphique
    ax.set_ylabel('Valeurs')  # Titre de l'axe y
    ax.set_xlabel('Langages de programmation')
    ax.legend()
    plt.show()  # Affichage d'une courbe

    # fig = plt.figure()
    # ax = fig.add_axes([0, 0, 1, 1])
    # x = ['50', '100', '150'] # définition des étiquettes pour chaque bin
    # y1 = [1, 2, 3] # pourcentage à obtenir pour =>
    # y2 = [1, 1, 1] # pourcentage à obtenir pour <=>

    # bins = [x + 0.5 for x in range(0, 4)]  # définit les bins pour l'histogramme
    # ax.bar(x, y1)
    # ax.bar(x, y1)
    # # plt.hist([y1, y2], bins=bins, color = ['deepskyblue', 'slateblue'], label = ['simple', 'double'])
    # # plt.xticks(bins, x)
    # plt.title('Comparaison entre une simple et une double inclusion, pour des rayons différents')
    # plt.xlabel('km du rayon considéré')
    # plt.ylabel("% de tournées n'ayant aucune tournées dans son rayon")
    # # plt.legend(['simple', 'double'])

    # plt.show()






# etiquettes = ['C', 'C++', 'Java', 'Python', 'PHP']
# valeurs = [23, 17, 35, 29, 12]

# # Affichage des données
# ax.bar(etiquettes, valeurs)




if __name__ == "__main__":
    filenames = ["simulations_reel_gdf.csv", "simulations_gdf.csv"]
    filename = "simulations_reel_gdf.csv"
    dictFilename = {"simulations_reel_gdf.csv": "reelles", "simulations_gdf.csv": "quelconques"}
    dist = [50e3, 100e3, 150e3]
    typeIsIn = [1, 2]
    dictType = {1:"simple", 2:"double"}

    ###      Tracer les histogrammes      ###

    # for file in filenames:
    #     for d in dist:
    #         for type in typeIsIn:
    #             print(histo(file, dictFilename, d, type, dictType))


    ###      Obtenir des comparaisons quantitatives      ###

    # for d in dist:
    #     for type in typeIsIn:
    #         print(comparaison(filename, d, type))

    print(histo_0_mutu())

