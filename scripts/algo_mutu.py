import numpy as np 
import pandas as pd
import yaml

config = yaml.safe_load(open('./config.yml'))
rayon = config['rayon']
tuple = config['tuple']
url = config['url']

def is_mutu(ArrayA,ArrayB):
    '''
    Takes two arrays, one for a producer A, one for a producer B, and returns a boolean 
    
    
    
    '''