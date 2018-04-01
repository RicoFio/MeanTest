from sys import argv
from openpyxl import Workbook
from openpyxl import load_workbook
import numpy as np
import sys

def getData(data):

    data_matrix = [[row[0].value,row[1].value,row[2].value, x] for x,row in enumerate(data.iter_rows(min_row=1)) if type(row[0].value) == float]
    data_matrix = np.matrix(data_matrix)
    separation = []

    for x,i in enumerate(data_matrix[1:,3]):
        if i != (data_matrix[x,3]+1):
            separation.append(x+1)

    data_matrix = data_matrix[:,0:3]
    data_matrix = np.split(data_matrix, separation)
    return data_matrix

def calc_diff_and_norm(m,c):
    #print m.shape
    normalized = []
    differences = []

    for i in range(2*c):
        diff = np.subtract(m[i][:,2],m[i+(2*c)][:,2])
        differences.append(diff)

    for norm in differences:
        g = np.subtract(norm, norm.min())
        normalized.append(g)

    return differences, normalized

def get_maximum(n, c):
    max_com = [x.argmax() for x in n]
    return max_com

def get_array_boundaries(pos, n):
    min_dist_from_center = min(pos)
    
    dist_center_end = [(len(x))-pos[i] for i,x in enumerate(n)]
    max_dist_from_center = min(dist_center_end)
    return (min_dist_from_center,max_dist_from_center)

def get_sets(n, aLen, c_pos, c):
    set1 = np.zeros((aLen[1]+aLen[0],0))
    set2 = set1.copy()

    for g,i in enumerate(n[0:c]):
        to_stack = i[c_pos[g]-aLen[0]:c_pos[g]+aLen[1]]
        set1 = np.hstack([set1,to_stack])

    for f,j in enumerate(n[c:2*c]):
        to_stack = j[c_pos[f]-aLen[0]:c_pos[f]+aLen[1]]
        #print to_stack.shape
        set2 = np.hstack([set2,to_stack])

    # get averages
    avgs1 = np.mean(set1, axis = 1)
    avgs2 = np.mean(set2, axis = 1)
    return avgs1,avgs2
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
    # retrieve first sheet name
    data = wb.active
    # obtain matrices by iterating over it
    matrices = getData(data)
    # calculate the differences and the normalized differences
    diff, norm = calc_diff_and_norm(matrices,comets)
    # check if set fullfills constraints
    pass_check = [1 for x in norm if x.max() > 100 and x.max() < 250]
    #print pass_check
    #if len(pass_check) != len(diff):
    #    print "sorry but this dataset cannot be regarded"
    #    sys.exit()

    # get highest values from the different commets for set 1
    pos_of_max_vals = get_maximum(norm[0:comets], comets)
    #print pos_of_max_vals
    # check the array lengths
    array_lengths = get_array_boundaries(pos_of_max_vals, norm[0:comets])
    # take averages of set 1 & set 2
    set1, set2 = get_sets(norm, array_lengths, pos_of_max_vals, comets)

    # give result
    print "-------------Averages-------------"
    print "Set1 ------------------------ Set2"
    print "----------------------------------"
    for i,x in enumerate(set1):
        print "{0:.8f}            {0:.8f}".format(set1[i,0],set2[i,0])
    print "----------------------------------"
