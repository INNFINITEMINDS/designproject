import thread
import time
from bottle import route, run, template
from test_util import *


isSeizure = False

# Define a function for the thread
def print_is_seizure( threadName, delay):
	count = 0
	#loop to poll value of isSeizure every ~2 seconds and call network
	while True:		
		time.sleep(delay)
		
		if isSeizure:
			main("yes")
			# print "%s: %s : seizure" % ( threadName, time.ctime(time.time()) )
		else:
			main("no")
			# print "%s: %s : not seizure" % ( threadName, time.ctime(time.time()) )


@route('/')
def root():	
	# return 'Welcome, go to /seizure/yes or /seizure/no to start this thing'
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



if __name__ == "__main__":
	# 
	isSeizure = False
	split_data()
	thread.start_new_thread( print_is_seizure, ("Thread-1", 0.5, ) )
	run(host='localhost', port=8082)
	# print_time( "threadName", 5)

# --> http://localhost:8080//seizure/yes
# --> http://localhost:8080//seizure/no
# --> http://localhost:8080/
