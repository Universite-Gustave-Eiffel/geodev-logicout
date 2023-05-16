import matplotlib.pyplot as plt
import numpy as np
import use_data
import IsInclude



def histo_comparaison(single_incluson, double_inclusion, typeHisto):

    """
        Allows you to plot a histogram comparing the mutualisation of single or double inclusion rounds according to the radius 
    
    Args:
        single_incluson {List}: list of id's sample that can be mutualised in single inclusion
        double_incluson {List}: list of id's sample that can be mutualised in double inclusion
        typeHisto {String}: '

    Output : 
        graphic window containing the histogram and a confirmation of the histogram plot as a String 
    """

    labels = ['50 km', '100 km', '150 km']

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, single_incluson, width, label='simple inclusion', color='deepskyblue')
    rects2 = ax.bar(x + width/2, double_inclusion, width, label='double inclusion', color='mediumorchid')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel("km du rayon considéré")
    if typeHisto == 'Mutu':
        ax.set_ylabel("% de tournées mutualisables") # i.e. with at least one sample in its buffer
    if typeHisto == 'Mean':
        ax.set_ylabel("nombre de tournées moyennes dans un rayon de X km")
    if typeHisto == 'Max':
        ax.set_ylabel("nombre maximum de tournées dans un rayon de X km")
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






def mutu(filename, dist):
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe of the selected csv file
    n = gdf.count()[0] # number of total rounds
    L1 = []
    L2 = []
    for j in range(1,3):
        for d in dist:
            pas_mutu = 0
            for i in range(n):
                tournee = gdf.iloc[[i]]
                gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, d, j)
                if gdf_IsInclude.count()[0] != 0:
                    pas_mutu += 1
            if j == 1:
                L1.append(int(pas_mutu * 100 / n))
            if j == 2:
                L2.append(int(pas_mutu * 100 / n))
    return L1, L2



def mean_mutu(filename, dist):
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe of the selected csv file
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
            if j == 1:
                L1.append(int(mean_mutu))
            if j == 2:
                L2.append(int(mean_mutu))
    return L1, L2



def max_mutu(filename, dist):
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe of the selected csv file
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
            if j == 1:
                L1.append(int(max_mutu))
            if j == 2:
                L2.append(int(max_mutu))
    return L1, L2







if __name__ == "__main__":

    # choice to work only with actual samples
    filename = "simulations_reel_gdf.csv"

    # test distances for the buffer radius
    dist = [50e3, 100e3, 150e3]


    ###      Obtaining quantitative comparisons      ###

    # You just have to enter one of the 3 parameters proposed in the python console to obtain a histogram, allowing you to visualise the selected parameter:
    # - average number of mutualisable tours
    # - maximum number of mutualisable tours
    # - percentage of mutualisable tours).

    print("Choose from the 3 possible histogram types:\n- 'Mean' to obtain a histogram of the AVERAGE number of samples that can be shared\n- 'Max' to obtain a histogram of the MAXIMUM number of samples that can be shared\n- 'Mutu' to obtain a histogram of the percentage of samples that can be shared.")
    typeHisto = input()

    if typeHisto == 'Mutu':
        single_incluson, double_inclusion = mutu(filename, dist)
        print(single_incluson)
        print(double_inclusion)
        print(histo_comparaison(single_incluson, double_inclusion, typeHisto))

    elif typeHisto == 'Mean':
        single_incluson, double_inclusion = mean_mutu(filename, dist)
        print(single_incluson)
        print(double_inclusion)
        print(histo_comparaison(single_incluson, double_inclusion, typeHisto))

    elif typeHisto == 'Max':
        single_incluson, double_inclusion = max_mutu(filename, dist)
        print(single_incluson)
        print(double_inclusion)
        print(histo_comparaison(single_incluson, double_inclusion, typeHisto))
    
    else :
        print("Erreur de saisi du type d'histrogramme")

