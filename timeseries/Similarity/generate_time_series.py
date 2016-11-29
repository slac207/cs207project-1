import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import distances
import numpy as np
import random
import BinarySearchDatabase
from series import ArrayTimeSeries as ts
import os

def generate_time_series():
    #script to generate and store 1000 timeseries
    for i in range(1000):
        x = distances.tsmaker(0.5, 0.15, 0.1)
        np.save("GeneratedTimeseries/Timeseries"+str(i), [x.times(),x.values()])
        
if __name__ == "__main__":
    generate_time_series()
        

