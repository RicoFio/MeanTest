from sys import argv
from openpyxl import Workbook
from openpyxl import load_workbook
import numpy as np

def getData(data):

    size = []
    data_separation = np.zeros((1,3))
    tracker = 2

    for idx, row in enumerate(data.iter_rows(min_row=1)):
	new_data = np.array([row[0].value,row[1].value,row[2].value])
        if type(new_data[0]) == np.float64:
		#print new_data
		data_separation = np.vstack([data_separation,new_data])  
		#print "added"		
	else:
	    print data_separation.size
	    size.append(data_separation.size)
	    print(new_data[0])

    size = np.unique(size)  
    print data_separation[0:size[1],]
    print np.unique(size)
    return data_separation, size

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
    comets = myargs['-c']
    # retrieve first sheet name
    sheet_name = wb.sheetnames[0]
    # load data from sheet
    data = wb.active
    # obtain matrices by iterating over it
    matrices, size = getData(data)

    #print matrices[1:size]





