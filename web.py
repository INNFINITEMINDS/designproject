import thread
import time
from bottle import route, run, template
from test_util_ import *


isSeizure = False
switch = False

# Define a function for the thread
def print_is_seizure( threadName, delay):
	count = 0
	#loop to poll value of isSeizure every ~2 seconds and call network
	while True:		
		time.sleep(delay)

		# need some sort of synchronization mechanism here bet the thread in print_is_seizure
		# and thread in test_my_nn. wait() and signal() ??
		if switch:
			thread.exit()

		if isSeizure:			
			print "%s: %s : seizure" % ( threadName, time.ctime(time.time()) )
			test_my_nn("yes")
		else:			
			print "%s: %s : not seizure" % ( threadName, time.ctime(time.time()) )
			test_my_nn("no")

		# thread.exit()
		# thread.start_new_thread( print_is_seizure, ("Thread-1", 0.5, ) )


@route('/')
def root():	
	# return 'Welcome, go to /seizure/yes or /seizure/no to start this thing'
	return template("main.html")


@route('/seizure/:arg')
def hello(arg):
	global isSeizure, switch

	if arg == 'no':
		isSeizure = False
		switch = True
		return template("main_interictal.html")		

	else:
		isSeizure = True	
		switch = True	
		return template("main_ictal.html")



if __name__ == "__main__":
	# 
	isSeizure = False	
	thread.start_new_thread( print_is_seizure, ("Thread-1", 0.5, ) )
	main()
	print 'Spliced data'
	run(host='localhost', port=8082)
	# print_time( "threadName", 5)

# --> http://localhost:8080//seizure/yes
# --> http://localhost:8080//seizure/no
# --> http://localhost:8080/
