import time
import pickle
import thread

from pylab import *
ion()

def function():

	f = open('plot_data/data.p', 'rb')
	s_data = pickle.load(f)
	f.close()

	plot_x = s_data['x']
	plot_y = s_data['y']

	clf()
	
	plot(range(0,len(plot_x)),plot_x / 10000)
	ylim(ymin = -1000000000000000000, ymax = 1000000000000000000)
	draw()	

if __name__ == "__main__":
	while True:
		function()
		time.sleep(1)

	raw_input("press enter")

