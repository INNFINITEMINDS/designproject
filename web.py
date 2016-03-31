import thread
import time
from bottle import route, run, template
import os
import scipy.io as sio
from nn import *
import pickle
from pybrain.tools.customxml.networkreader import NetworkReader
import socket
from pylab import *
ion()

testfile_path = "final_net/test_set.p"
netfile_path = "final_net/final_last_bestnet_8.p"

ictal_data = []
ictal_labels = []
interictal_data = []
interictal_labels = []

plot_y = np.zeros(0)
plot_x = np.linspace(0,0,500)

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
	global ictal_data, ictal_labels, interictal_data, interictal_labels, plot_y, plot_x

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
			plot_x = ictal_data[ictal_index:ictal_index+length]
			test_data.append(plot_x)
			plot_y = ictal_labels[ictal_index:ictal_index+length]
			test_labels.append(plot_y)
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
			plot_x = interictal_data[interictal_index:interictal_index+length]
			test_data.append(plot_x)
			plot_y = interictal_labels[interictal_index:interictal_index+length]
			test_labels.append(plot_y)
			test_error, true_pos, true_neg, num_seizures = test_nn(net, test_data[index], test_labels[index])
			interictal_index +=  length
			index += 1 
		print "Number of seizures detected: %d, Test error: %02f, True pos: %02f, True neg: %02f" % (num_seizures,test_error, true_pos, true_neg)
	
@route('/draw')
def p_draw():
	clf()
	# import pdb; pdb.set_trace()
	# gcf().set_size_inches(10,10)

	plot(np.linspace(0,1,500), plot_x / 5000)
	ylim(ymin = -1000000000000000000, ymax = 1000000000000000000)
	xlabel('Time')
	ylabel('Signal')
	title('Patient Clip')
	draw()
	return 'check the plot in background'

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
	global oldepoch

	oldepoch = int(round(time.time() * 1000))
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


def run_app():
	run(host=socket.gethostbyaddr(socket.gethostname())[0], port=8082)


if __name__ == "__main__":
	isSeizure = False

	# Load data
	main()

	thread.start_new_thread( print_is_seizure, ("Thread-1", 1, ) )

	thread.start_new_thread( run_app, () )

	while True:
		p_draw()
		time.sleep(1)
	
