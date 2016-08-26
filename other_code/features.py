import numpy as np 
import pandas as pd 
import itertools
from util import *


def getAllFeatures(inp_files):

	out_dataframe = []

	import pdb; pdb.set_trace();

	for file_index in range(0, len(inp_files)):
		data, freq, channels, latency = get_contents_at_index(inp_files, file_index)

		resultList = []
		featureList = []

		#1st derivatives of features
		firstDeriv = data.values[1:,:] - data.values[:times,:]   
	   	#2nd derivatives of features
    	secondDeriv = firstDeriv[1:,:] - firstDeriv[:times-1,:] 

		# Channel featureList
		for i in range(0, len(channels[0][0])):
			ch_tag = 'channel:%s' % channels[0][0][i][0].encode("ascii")
			
			resultList.append(np.max(np.abs(data[i])))
			featureList.append('%sMaxAmp'%(ch_tag))

			resultList.append(np.mean(np.abs(data[i])))
			featureList.append('%sMeanAmp'%(ch_tag))

			resultList.append(np.var(data[i]))
			featureList.append('%sVar'%(ch_tag))

			fft_data = abs(np.fft.fft(data[i]))

			resultList.append(fft_data.max())
			featureList.append('%sMaxFourierAmp'%(ch_tag))

			resultList.append(fft_data.mean())
			featureList.append('%sMeanFourierAmp'%(ch_tag))

			resultList.append(fft_data.var())
			featureList.append('%sVarFourierAmp'%(ch_tag))


			# 1st Derivative Channel Features
	        resultList.append(np.max(np.abs(firstDeriv[:,i])))
	        featureList.append('%sMaxfirstDeriv'%(ch_tag))

	        resultList.append(np.mean(np.abs(firstDeriv[:,i])))
	        featureList.append('%sMeanfirstDeriv'%(ch_tag))	     

	        resultList.append(np.var(firstDeriv[:,i]))
	        featureList.append('%sVarfirstDeriv'%(ch_tag))	   

	        # 2nd Derivative Channel Features
	        resultList.append(np.max(np.abs(secondDeriv[:,i])))
	        featureList.append('%sMaxsecondDeriv'%(ch_tag))

	        resultList.append(np.mean(np.abs(delta2[:,i])))
	        featureList.append('%sMeansecondDeriv'%(ch_tag))	 

	        resultList.append(np.var(secondDeriv[:,i]))
	        featureList.append('%sVarsecondDeriv'%(ch_tag))

		#Convert pandas dataframe as a matrix so that can be used by numpy in main
		out_dataframe.append(pd.DataFrame(data=resultList, index=featureList).as_matrix().T)

	return out_dataframe

