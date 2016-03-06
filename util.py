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


def load_freq_bands_for_patient(patient_source):
    # Read all file names
    folders = os.listdir(patient_source)

    freq_list = [folder for folder in folders]
    ictal_contents = []
    interictal_contents = []
    for folder in freq_list:
        folderpath = patient_source + folder
        files = os.listdir(folderpath)

        # Get ictal, interictal and test file names in the directory
        ictal_mat_file_name = [file_name for file_name in files if '_ictal' in file_name]
        interictal_mat_file_name = [file_name for file_name in files if '_interictal' in file_name]
        # test_mat_file_name = [file_name for file_name in files if '_test' in file_name]

        # Get matlab contents in mat files
        ictal_contents = load_all_for_arr(folderpath, ictal_mat_file_name)
        interictal_contents = load_all_for_arr(folderpath, interictal_mat_file_name)
        # test_contents = load_all_for_arr(patient_source, test_mat_file_name)

        # ictal_contents.extend(freq_ictal_contents)
        # interictal_contents.extend(freq_interictal_contents)

    return ictal_contents, interictal_contents


def load_all_patients(src=clips_src):
    # TODO: save results for all patients.

    # Get all folders inside clip folder
    folders = os.listdir(src)

    # Filter folders starting with 'Patient'
    names_list = [folder for folder in folders if folder.startswith('Patient_')]

    ictal_contents = []
    interictal_contents = []
    test_contents = []
    # Run for each folder
    for folder in names_list:
        temp_ictal, temp_interictal, temp_test = load_for_patient('%s%s' % (src, folder))
        ictal_contents.extend(temp_ictal)
        interictal_contents.extend(temp_interictal)
        test_contents.extend(temp_test)
        # import pdb; pdb.set_trace();

    return ictal_contents, interictal_contents, test_contents


# TODO: Remove main block
if __name__ == '__main__':
    # raw_input("Press enter to begin")
    load_freq_bands_for_patient("../shared_dir/filtered_data/Patient_1/")
    raw_input("Press enter to finish")
