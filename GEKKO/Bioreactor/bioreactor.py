import numpy as np

'''
Cultivation of isolated plant cells in suspension culture (adapted from APMonitor example for Cell Cultrure). Only cell and substrate are considered (product is the cells in this process). A set of hypothetical experimental data is used to fit theoretical model to experiment.

Munack A., Posten C. (1989): Design of optimal dynamical experiments for parameter estimation, Proceedings of the Americal Control Conference, Vol. 4, 2010-2016. 
'''

'''
# Data init
data_file = np.loadtxt('GEKKO/Bioreactor/data.txt', delimiter=',')
time = data_file[:,0]
data = data_file[:,1]
print(data[0:2])
'''