import numpy as np 
import pandas as pd
import yaml
from geopy import distance

config = yaml.safe_load(open('./config.yml'))
rayon = config['rayon']
tuple = config['tuple']
url = config['url']

def dist(coordA,coordB):
    return distance.lonlat((coordA[0],coordA[1]),(coordB[0],coordB[1])) / 1000

def is_mutu(ArrayA,ArrayB):
    '''
    Takes two arrays, one for a producer A, one for a producer B, and returns a boolean whether or not the mutualisation is possible
    (0 being not possible, 1 being possible)
    '''
    startA = ArrayA[0]
    startB = ArrayB[0]
    
    A_include_B = True
    B_include_A = True
    #Testing if all B points are in a 100km radius of A start
    for coord in ArrayB:
        if dist(coord,startA)>rayon:
            A_include_B = False
            break
    #Testing if all A points are in a 100km radius of B start
    for coord in ArrayA:
        if dist(coord,startB)>rayon:
            B_include_A = False
            break
    if A_include_B == True and B_include_A == True:
        return True
    else:
        return  False