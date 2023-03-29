import numpy as np
import csv
import algo_mutu
# from algo_mutu import *
# file = './data/steps.csv'
# steps = []
# with open(file,newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#     for row in spamreader:
#         steps.append(row)

steps = [[5,[[1,2],[3,2]]],
         [9,[3,4],[2,5],[6,4]]]

# Attention : faire en sorte que la boucle ne tourne pas dans le sens inverse : trajet A vs trajet B, puis trajet B vs trajet A

def fonction(steps):

    tab_mutualisable = []
    n = len(steps)
    index = 0
    for i in range(n):

        tabA = []
        nb_steps_A = len(steps[i])
        for p in range(nb_steps_A-1):
            tabA.append(steps[i][p+1])

        for j in range(n-index):
            tabB = []
            index+=1
            nb_steps_B = len(steps[j])
            for q in range(nb_steps_B-1):
                tabB.append(steps[j][q+1])
            
            var = algo_mutu.is_mutu(tabA,tabB) 
            var = True
            if(var == True):
                    tab_mutualisable.append((steps[i][0],steps[j][0]))


def fonction(steps):

    tab_mutualisable = []

    for i in steps:
        for j in steps:
            if i != j:
                A = i[1:]
                B = j[1:]

                var = algo_mutu.is_mutu(A,B)
                
                if(var == True):
                    tab_mutualisable.append((i[0],j[0]))

    return tab_mutualisable
