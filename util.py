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
    # test_mat_file_name = [file_name for file_name in files if '_test' in file_name]

    minimum = min(len(ictal_mat_file_name), len(interictal_mat_file_name))

    # Get matlab contents in mat files
    ictal_contents = load_all_for_arr(patient_source, ictal_mat_file_name[:minimum])
    interictal_contents = load_all_for_arr(patient_source, interictal_mat_file_name[:minimum])
    # test_contents = load_all_for_arr(patient_source, test_mat_file_name)

    freq = ictal_contents[0].get('freq')
    patient = (freq, ictal_contents, interictal_contents)
    # return ictal_contents, interictal_contents, test_contents
    return patient


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

        # Get matlab contents in mat files
        ictal_contents.extend(load_all_for_arr(folderpath, ictal_mat_file_name))
        interictal_contents.extend(load_all_for_arr(folderpath, interictal_mat_file_name))

    freq = ictal_contents[0].get('freq')
    patient = (freq, ictal_contents, interictal_contents)
    return patient


def load_all_patients(src=clips_src):
    # TODO: save results for all patients.

    # Get all folders inside clip folder
    folders = os.listdir(src)

    # Filter folders starting with 'Patient'
    names_list = [folder for folder in folders if folder.startswith('Patient_')]

    patient_data = []
    i = 0
    # Run for each folder
    for folder in names_list:
        print 'Loading files from %s%s' % (src, folder)
        patient_data.append(load_for_patient('%s%s' % (src, folder)))
        i += 1
        if i == 2:
            break

    return patient_data


def get_metadata_for_patient(patient_source):
    files = os.listdir(patient_source)
    patient_files = [file for file in files if file.startsWith('Patient_')]

    if patient_files is not None:
        matfile = sio.loadmat(patient_files[0])
        frequency = matfile.get('freq')
        channels = matfile.get('channels')
        return frequency, channels

    else:
        return None, None


def load_all_freq_bands(src):
    # Get all folders inside filtered_data folder
    folders = os.listdir(src)

    # Filter folders starting with 'Patient'
    patient_list = [folder for folder in folders if folder.startswith('Patient_')]

    patient_data = []
    i = 0

    for folder in patient_list:
        print "Loading from %s%s" % (src, folder)
        patient_data.append(load_freq_bands_for_patient('%s%s/' % (src, folder)))
        i += 1
        # if i == 2:
        #     break

    return patient_data


# TODO: Remove main block
if __name__ == '__main__':
    # raw_input("Press enter to begin")
    load_freq_bands_for_patient("../shared_dir/filtered_data/Patient_1/")
    raw_input("Press enter to finish")
