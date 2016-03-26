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
def main():
    testfile = open(testfile_path, 'rb+')

    testdict = pickle.load(testfile)
    inp_data = testdict['test_data']
    inp_labels = testdict['test_labels']

    data_index = len(inp_data) / 2
    global ictal_data
    ictal_data = inp_data[:data_index]
    global interictal_data
    interictal_data = inp_data[data_index:]

    label_index = len(inp_data) / 2
    global ictal_labels
    ictal_labels = inp_labels[:label_index]
    global interictal_labels
    interictal_labels = inp_labels[label_index:]

    return ictal_data, ictal_labels, interictal_data, interictal_labels


def test_my_nn(arg):
        
    net = NetworkReader.readFrom(netfile_path)

    index = 0
    ictal_index = 0
    interictal_index = 0
    test_data = []
    test_labels = []
    global ictal_data, ictal_labels, interictal_data, interictal_labels

    #loop to send 1 second (500 datapoints) worth of data to network
    #continues to send until user toggles button
    # need to change while condition to while thread.isAlive()
    while True:
        if(arg == "yes"):            
            if(ictal_index >= 110500):
                ictal_index = 0
                index = 0
                ictal_data = []
                ictal_labels = []

            length = 1 * 500
            test_data.append(ictal_data[ictal_index:ictal_index+length])
            test_labels.append(ictal_labels[ictal_index:ictal_index+length])
            test_error, true_pos, true_neg, num_seizures = test_nn(net, test_data[index],test_labels[index])
            ictal_index += length
            index += 1
            # print "INDEX: " 
            # print ictal_index , index

        elif(arg == "no"):           
            if(interictal_index >= 110500):
                interictal_index = 0
                index = 0
                interictal_data = []
                interictal_labels = []

            length = 1 * 500
            test_data.append(interictal_data[interictal_index:interictal_index+length])
            test_labels.append(interictal_labels[interictal_index:interictal_index+length])
            test_error, true_pos, true_neg, num_seizures = test_nn(net, test_data[index], test_labels[index])
            interictal_index +=  length
            index += 1
            # print "INDEX: "
            # print interictal_index , index
    
        print "Test error: %02f, True pos: %02f, True neg: %02f" % (test_error, true_pos, true_neg)
    # print "Number of seizures detected: %d, Actual number of seizures: %d" % (num_seizures, test_num_seizures[i])


if __name__ == '__main__':
    main()
