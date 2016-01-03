import numpy as np 
import pandas as pd 
import itertools
from util import *

def getAllFeatures(data):

	data, freq, channels, latency = get_contents_at_index(data, 0)

	resultList = []
	featureList = []

	# Channel featureList

	for i in range(0, len(channels[0][0])):
		
		resultList.append(np.max(np.abs(data[i])))
		featureList.append('channel%iMaxAmp'%(i))

		resultList.append(np.mean(np.abs(data[i])))
		featureList.append('channel%iMeanAmp'%(i))

		resultList.append(np.var(np.abs(data[i])))
		featureList.append('channel%iAbsVar'%(i))

		resultList.append(np.var(data[i]))
		featureList.append('channel%iVar'%(i))

		fft_data = abs(np.fft.fft(data[i]))

		resultList.append(fft_data.max())
		featureList.append('channel%iMaxFourierAmp'%(i))

		resultList.append(fft_data.mean())
		featureList.append('channel%iMeanFourierAmp'%(i))

		resultList.append(fft_data.var())
		featureList.append('channel%iVarFourierAmp'%(i))

		# resultList.append(abs(freq[np.argmax(fft_data)])
		# featureList.append('chan%iMaxFreq'%(i-1))
	import pdb; pdb.set_trace();


	return pd.DataFrame(data=resultList, index=featureList).T
