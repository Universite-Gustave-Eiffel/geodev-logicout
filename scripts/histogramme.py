import numpy as np
import matplotlib as plt 

# Import CSV 

link = ''
data = np.genfromtxt(link, delimiter=',')

# Appel algo rayon 100km
A = []



plt.hist(A,bins=20,range=(0,4),color="y",edgecolor="gray",label="histogramme")
plt.title('Histogramme de mutualisation des producteurs sur la France, dans un rayon de 100km autour des exploitations')
plt.xlabel('Nombre de producteur dans le rayon de 100 km')
plt.ylabel('Count')
plt.show()

