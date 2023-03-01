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
    Takes two arrays, one for a producer A, one for a producer B, and returns a boolean showing whether or not the mutualisation is possible
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
    
def is_mutu_3(ArrayA,ArrayB,ArrayC):
    '''
    Takes three arrays of producers' routes, and returns a boolean showing whether or not the mutualisation is possible
    (0 being not possible, 1 being possible)
    '''
    startA = ArrayA[0]
    startB = ArrayB[0]
    startC = ArrayC[0]
    
    A = True
    B = True
    C = True
    
    for coord in ArrayA:
        if dist(coord,startB)>rayon:
            B = False
            break
        if dist(coord,startC)>rayon:
            C = False
            break
    for coord in ArrayB:
        if dist(coord,startA)>rayon:
            A = False
            break
        if dist(coord,startC)>rayon:
            C = False
            break
    for coord in ArrayC:
        if dist(coord,startA)>rayon:
            A = False
            break
        if dist(coord,startB)>rayon:
            B = False
            break
    
    if A == True and B == True and C == True:
        return True
    else:
        return False