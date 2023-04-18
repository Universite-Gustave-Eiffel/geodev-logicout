import matplotlib.pyplot as plt
import numpy as np
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



def histo_comparaison(single_incluson, double_inclusion):

    labels = ['50 km', '100 km', '150 km']

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, single_incluson, width, label='simple inclusion', color='deepskyblue')
    rects2 = ax.bar(x + width/2, double_inclusion, width, label='double inclusion', color='mediumorchid')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel("km du rayon considéré")
    ax.set_ylabel("% de tournées n'ayant aucune tournées dans son rayon")
    ax.set_title('Comparaison entre une simple et une double inclusion, pour des rayons différents')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    autolabel(rects1, ax)
    autolabel(rects2, ax)
    fig.tight_layout()
    plt.show()
    return 'Tracé effectué !'

def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')






def Pas_mutu(filename, dist):
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe du fichier csv choisi
    n = gdf.count()[0] # number of total rounds
    L1 = []
    L2 = []
    for j in range(1,3):
        for d in dist:
            pas_mutu = 0
            for i in range(n):
                tournee = gdf.iloc[[i]]
                gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, d, j)
                if gdf_IsInclude.count()[0] == 0:
                    pas_mutu += 1
            if i == 1:
                L1.append(pas_mutu * 100 / n)
            if i == 2:
                L2.append(pas_mutu * 100 / n)
    return L1, L2



def Mean_mutu(filename, dist):
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe du fichier csv choisi
    n = gdf.count()[0] # number of total rounds
    L1 = []
    L2 = []
    for j in range(1,3):
        for d in dist:
            mean_mutu = 0
            for i in range(n):
                tournee = gdf.iloc[[i]]
                gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, d, j)
                mean_mutu += gdf_IsInclude.count()[0]
            mean_mutu = mean_mutu / n
            if i == 1:
                L1.append(mean_mutu * 100 / n)
            if i == 2:
                L2.append(mean_mutu * 100 / n)
    return L1, L2



def Max_mutu(filename, dist):
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe du fichier csv choisi
    n = gdf.count()[0] # number of total rounds
    L1 = []
    L2 = []
    for j in range(1,3):
        for d in dist:
            max_mutu = 0
            for i in range(n):
                tournee = gdf.iloc[[i]]
                gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, d, j)
                mutu = gdf_IsInclude.count()[0]
                if mutu > max_mutu:
                    max_mutu = mutu
            if i == 1:
                L1.append(max_mutu * 100 / n)
            if i == 2:
                L2.append(max_mutu * 100 / n)
    return L1, L2







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

    single_incluson, double_inclusion = Pas_mutu(filename, dist)
    print(histo_comparaison(single_incluson, double_inclusion))


