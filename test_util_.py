import os
import scipy.io as sio
from nn import *
import pickle
from pybrain.tools.customxml.networkreader import NetworkReader

testfile_path = "/u/d/rajgolik/Sublime Text 2/UX/ECE496/final_net/test_set.p"
netfile_path = "/u/d/rajgolik/Sublime Text 2/UX/ECE496/final_net/final_last_bestnet_8.p"

ictal_data = []
ictal_labels = []
interictal_data = []
interictal_labels = []

#split data before testing network
def split_data():
    testfile = open(testfile_path, 'rb+')

    testdict = pickle.load(testfile)
    inp_data = testdict['test_data']
    inp_labels = testdict['test_labels']

    data_index = len(inp_data) / 2
    ictal_data = inp_data[:data_index]
    interictal_data = inp_data[data_index:]

    label_index = len(inp_data) / 2
    ictal_labels = inp_labels[:label_index]
    interictal_labels = inp_labels[label_index:]


def main(arg):
        
    net = NetworkReader.readFrom(netfile_path)

    ictal_index = 0
    interictal_index = 0

    #loop to send 1 second (500 datapoints) worth of data to network
    #continues to send until user toggles button
    while True:
        if(arg == 'yes'):
            print 'User-ictal'
            length = 1 * 500
            test_error, true_pos, true_neg, num_seizures = test_nn(net, ictal_data[ictal_index:ictal_index+length], ictal_labels[ictal_index:ictal_index+length])
            ictal_index += length

        elif(arg == "no"):
            print 'User-inter ictal'            
            length = 1 * 500
            test_error, true_pos, true_neg, num_seizures = test_nn(net, interictal_data[interictal_index:interictal_index+length], interictal_labels[interictal_index:interictal_index+length])
            interictal_index +=  length
            
        print "Test error: %02f, True pos: %02f, True neg: %02f" % (test_error, true_pos, true_neg)
    # print "Number of seizures detected: %d, Actual number of seizures: %d" % (num_seizures, test_num_seizures[i])
    # raw_input("Press enter for next case")


if __name__ == '__main__':
    main()
