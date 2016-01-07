import os
import scipy.io as sio

clips_src = '../clips/'

# Example call
# data, freq, channels, latency = get_contents_at_index(ictal_contents, 3)
def get_contents_at_index(contents, index):
	# Skipping the out of bounds check.

	data = contents[index].get('data')
	freq = contents[index].get('freq')
	channels = contents[index].get('channels')
	latency = contents[index].get('latency')
	return data, freq, channels, latency

def load_all_for_arr(fld_src, mat_src):
	contents = []
	for src in mat_src:
		name = '%s/%s' % (fld_src, src)
		contents.append(sio.loadmat(name))
	return contents

def load_for_patient(patient_source):
	# Read all file names
	files = os.listdir(patient_source)

	# Get ictal, interictal and test file names in the directory
	ictal_mat_file_name = [file_name for file_name in files if '_ictal' in file_name]
	interictal_mat_file_name = [file_name for file_name in files if '_interictal' in file_name]
	test_mat_file_name = [file_name for file_name in files if '_test' in file_name]
	
	# Get matlab contents in mat files
	ictal_contents = load_all_for_arr(patient_source, ictal_mat_file_name)
	interictal_contents = load_all_for_arr(patient_source, interictal_mat_file_name)
	test_contents = load_all_for_arr(patient_source, test_mat_file_name)

	return ictal_contents, interictal_contents, test_contents

def load_all_patients(src = clips_src):
	# TODO: save results for all patients.

	# Get all folders inside clip folder
	folders = os.listdir(src)

	# Filter folders starting with 'Patient'
	names_list = [folder for folder  in folders if folder.startswith('Patient_')]

	# Run for each folder
	for folder in names_list:
		ictal_contents, interictal_contents, test_contents = load_for_patient('%s%s' % (src,folder));

	import pdb; pdb.set_trace();

# TODO: Remove main block
if __name__ == '__main__':
	# raw_input("Press enter to begin")
	load_all_patients()
	raw_input("Press enter to finish");