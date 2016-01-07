from util import *
from features import *
from svm import *



def main():
	a = 1;
	ictal_contents, interictal_contents, test_contents = load_for_patient('../clips/Patient_1')

	ictal_df = getAllFeatures(ictal_contents)

	import pdb; pdb.set_trace();

	interictal_df = getAllFeatures(interictal_contents)

	import pdb; pdb.set_trace();

	split_arr = np.split(np.array(ictal_df), 2)
	split_arr2 = np.split(np.array(interictal_df), 2)

	training_segments = np.append(split_arr[0], split_arr2[0])
	validation_segments = np.append(split_arr[1], split_arr2[1])

	training_target = np.append(np.ones(len(split_arr[0])), np.zeros(len(split_arr2[0])))
	validation_target = np.append(np.ones(len(split_arr[1])), np.zeros(len(split_arr2[1])))



if __name__ == '__main__':
	# raw_input("Press enter to begin")
	main()
	raw_input("Press enter to finish");