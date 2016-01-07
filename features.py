import numpy as np 
import pandas as pd 
import itertools
from util import *

def getAllFeatures(inp_files):

	out_dataframe = []

	# import pdb; pdb.set_trace();

	for file_index in range(0, len(inp_files)):
		data, freq, channels, latency = get_contents_at_index(inp_files, file_index)

		resultList = []
		featureList = []
		# Channel featureList
		for i in range(0, len(channels[0][0])):

			ch_tag = 'channel:%s' % channels[0][0][i][0].encode("ascii")
			
			resultList.append(np.max(np.abs(data[i])))
			featureList.append('%sMaxAmp'%(ch_tag))

			resultList.append(np.mean(np.abs(data[i])))
			featureList.append('%sMeanAmp'%(ch_tag))

			resultList.append(np.var(np.abs(data[i])))
			featureList.append('%sAbsVar'%(ch_tag))

			resultList.append(np.var(data[i]))
			featureList.append('%sVar'%(ch_tag))

			fft_data = abs(np.fft.fft(data[i]))

			resultList.append(fft_data.max())
			featureList.append('%sMaxFourierAmp'%(ch_tag))

			resultList.append(fft_data.mean())
			featureList.append('%sMeanFourierAmp'%(ch_tag))

			resultList.append(fft_data.var())
			featureList.append('%sVarFourierAmp'%(ch_tag))

			# resultList.append(abs(freq[np.argmax(fft_data)])
			# featureList.append('chan%iMaxFreq'%(i-1))

		out_dataframe.append(pd.DataFrame(data=resultList, index=featureList).T)

	return out_dataframe
