import thread
import time
from bottle import route, run, template
from test_util import *


isSeizure = False

# Define a function for the thread
def print_is_seizure( threadName, delay):
	count = 0
	while count < 20:
		time.sleep(delay)
		count += 1
		if isSeizure:
			print "%s: %s : seizure" % ( threadName, time.ctime(time.time()) )
		else:
			print "%s: %s : not seizure" % ( threadName, time.ctime(time.time()) )


@route('/')
def root():
	
	# return 'Welcome, go to /seizure/yes or /seizure/no to start this thing'
	return template("main.html")


@route('/seizure/:arg')
def hello(arg):
	global isSeizure
	if arg == 'no':
		isSeizure = False
		# return 'Nothing to see here'
		return template("main_interictal.html")

	else:
		isSeizure = True
		# return 'ITS HAPPENING !!!'
		return template("main_ictal.html")

test_util.main()


if __name__ == "__main__":
	# 
	isSeizure = False
	thread.start_new_thread( print_is_seizure, ("Thread-1", 3, ) )
	run(host='localhost', port=8082)
	# print_time( "threadName", 5)

# --> http://localhost:8080//seizure/yes
# --> http://localhost:8080//seizure/no
# --> http://localhost:8080/
