import thread
import time
from bottle import route, run, template
import os
import scipy.io as sio
from nn import *
import pickle
from pybrain.tools.customxml.networkreader import NetworkReader
import socket

testfile_path = "final_net/test_set.p"
netfile_path = "final_net/final_last_bestnet_8.p"

ictal_data = []
ictal_labels = []
interictal_data = []
interictal_labels = []

isSeizure = False

# Define a function for the thread
def print_is_seizure( threadName, delay):
	
	net = NetworkReader.readFrom(netfile_path)

	index = 0
	length = 500
	ictal_index = 0
	interictal_index = 0
	test_data = []
	test_labels = []
	global ictal_data, ictal_labels, interictal_data, interictal_labels

	#loop to send 1 second (500 datapoints) worth of data to network
	#continues to send until user toggles button
	while True:	
		time.sleep(delay)

		if isSeizure:			
			# print "%s: %s : seizure" % ( threadName, time.ctime(time.time()) )
			if(ictal_index >= len(ictal_data)):
				ictal_index = 0
				index = 0
				test_data = []
				test_labels = []

			length = 1 * 500
			test_data.append(ictal_data[ictal_index:ictal_index+length])
			test_labels.append(ictal_labels[ictal_index:ictal_index+length])
			test_error, true_pos, true_neg, num_seizures = test_nn(net, test_data[index],test_labels[index])
			ictal_index += length
			index += 1

		else:			
			# print "%s: %s : not seizure" % ( threadName, time.ctime(time.time()) )
			if(interictal_index >= len(interictal_data)):
				interictal_index = 0
				index = 0
				test_data = []
				test_labels = []

			length = 1 * 500
			test_data.append(interictal_data[interictal_index:interictal_index+length])
			test_labels.append(interictal_labels[interictal_index:interictal_index+length])
			test_error, true_pos, true_neg, num_seizures = test_nn(net, test_data[index], test_labels[index])
			interictal_index +=  length
			index += 1 
		print "Number of seizures detected: %d, Test error: %02f, True pos: %02f, True neg: %02f" % (num_seizures,test_error, true_pos, true_neg)
	

@route('/')
def root():	
	return template("main.html")


@route('/seizure/:arg')
def hello(arg):
	global isSeizure

	if arg == 'no':
		isSeizure = False
		return template("main_interictal.html")		

	else:
		isSeizure = True	
		return template("main_ictal.html")

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


if __name__ == "__main__":
	isSeizure = False

	# Load data
	main()

	thread.start_new_thread( print_is_seizure, ("Thread-1", 0.3, ) )

	print 'Spliced data'
	# run(host=socket.gethostbyname(socket.gethostname()), port=8082)
	# run(host='localhost'), port=8082)
	run(host=socket.gethostbyaddr(socket.gethostname())[0], port=8082)
