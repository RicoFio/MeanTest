from sys import argv
from openpyxl import Workbook
from openpyxl import load_workbook
import numpy as np

def getData(data):

    data_separation = np.zeros((0,3))

    for idx, row in enumerate(data.iter_rows(min_row=1)):
        new_data = np.array([row[0].value,row[1].value,row[2].value])
        if type(new_data[0]) == np.float64:
    	    #print new_data
            data_separation = np.vstack([data_separation,new_data])
    	    #print "added"

    return data_separation

def calc_diff_and_norm(m,dp,c):
    print m.shape
    r = (np.subtract(m[:,0],m[:,1])).T
    #print r.size
    f = r.copy()
    out = m.copy()

    for j in range(4):
        for i in range(c):
            minval = np.min(f[j*i*dp:(i+1)*dp*(j+1)])
            f[j*i*dp:(i+1)*dp*(j+1)] = np.subtract(f[j*i*dp:(i+1)*dp*(j+1)],minval)

    #print r
    #print f
    #print out
    m[:,:-1] = r
    m[:,:-1] = f

    return m


"""Collect command-line options in a dictionary"""

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

if __name__ == '__main__':

    myargs = getopts(argv)

    # load filename
    file =  myargs['-i']
    # load workbook
    wb = load_workbook(filename = file)
    # retrieve number of comets
    comets = int(myargs['-c'])
    # retrieve number of datapoints
    data_points = int(myargs['-dp'])
    # retrieve first sheet name
    sheet_name = wb.sheetnames[0]
    # load data from sheet
    data = wb.active
    # obtain matrices by iterating over it
    matrices = getData(data)
    # calculate differences and the normalize differences
    differencen, normalized = calc_diff_and_norm(matrices, data_points, comets)
    #

    #print matrices[1:size]
