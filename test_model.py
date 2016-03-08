import numpy as np
import pickle
import timeit
import scipy.signal as ss
from sklearn.decomposition import PCA
from wavelets import WaveletAnalysis
import pickle

from util import *
from nn import *

default_test_data = "/home/divd/ece496/shared_dir/kaggle_data/validation/"
net_path = "/home/divd/ece496/nets/best_net_4.p"


def main(data_src=default_test_data):
    # Load net
    net_file = open(net_path, "rb")
    result = pickle.load(net_file)
    net = result['net']

    # Load data
    patient_data = load_all_patients(data_src)

    pnum = 1
    for patient in patient_data:
        print "Processing data for patient %d" % pnum
        ictal_data, interictal_data = process_patient_data(patient)

        ictal_labels = np.ones(len(ictal_data))
        interictal_labels = np.zeros(len(interictal_data))

        for i in range(0, 1):
            used_ictal = 0
            used_int = 0
            num = 5

            # # first test case
            test_case_input = np.vstack([interictal_data[used_int:used_int+num], ictal_data[used_ictal:used_ictal+num], interictal_data[used_int+num:used_int+2*num]])
            test_case_labels = np.concatenate([interictal_labels[used_int:used_int+num], ictal_labels[used_ictal:used_ictal+num], interictal_labels[used_int+num:used_int+2*num]])

            output = test_nn(net, test_case_input, test_case_labels)
            print sum(output == test_case_labels)

            #
            # used_int += 2*num
            # used_ictal += num
            #
            # test_case_input = interictal_data[used_int:used_int+3*num]
            # test_case_labels = interictal_labels[used_int:used_int+3*num]
            #
            # used_int += 3*num
            #
            # test_case_input = ictal_data[used_ictal:used_ictal+3*num]
            # test_case_labels = ictal_labels[used_ictal:used_ictal+3*num]
            #
            # used_ictal += 3*num
            #
            # test_case_input = np.vstack([ictal_data[used_ictal:used_ictal+num], interictal_data[used_int:used_int+num], ictal_data[used_ictal+num:used_ictal+2*num]])
            # test_case_labels = np.vstack([ictal_labels[used_ictal:used_ictal+num], interictal_labels[used_int:used_int+num], ictal_labels[used_ictal+num:used_ictal+2*num]])
            #
            # used_ictal += 2*num
            # used_int += num

            test_case_input = np.concatenate([ictal_data[used_ictal:used_ictal+3*num], interictal_data[used_int:used_int+3*num]])
            test_case_labels = np.concatenate([ictal_labels[used_ictal:used_ictal+3*num], interictal_labels[used_int:used_int+3*num]])

            used_ictal += 3*num
            used_int += 3*num

            test_case_output = run_nn(net, test_case_input, test_case_labels)
            nvalid = len(test_case_input)
            test_case_error = (nvalid - sum(np.equal(test_case_output, test_case_labels))) / float(nvalid)
            print "Validation error: %f" % test_case_error
            correct_pred = (1 - test_case_error) * 100
            print "Correct predictions : %.3f%%" % correct_pred

            true_pos = 100 * sum(np.logical_and(test_case_output, test_case_labels)) / sum(test_case_labels)
            true_neg = 100 * (nvalid - sum(np.logical_xor(test_case_output, test_case_labels)) - sum(
                np.logical_and(test_case_output, test_case_labels))) / (nvalid - sum(test_case_labels))

            print "True positive: %.3f%%, True negative: %.3f%%" % (true_pos, true_neg)

            # Shuffle data
            seed = np.random.get_state()
            np.random.shuffle(ictal_data)
            np.random.set_state(seed)
            np.random.shuffle(ictal_labels)

            seed = np.random.get_state()
            np.random.shuffle(interictal_data)
            np.random.set_state(seed)
            np.random.shuffle(interictal_labels)

        # second test case


        pnum += 1


def process_patient_data(patient):
    freq = patient[0]
    ictal_files = patient[1]
    interictal_files = patient[2]

    wav_ictal_data = []
    wav_interictal_data = []

    num_files = min(len(ictal_files), len(interictal_files))
    datasize = int(round(freq / 10))

    for index in range(0, num_files):
        # print "Processing file %d " % index
        ictal_channels = ictal_files[index].get('data')
        for channel in ictal_channels:
            channel = ss.decimate(channel, datasize)
            ictal_wavelets = np.transpose(np.real(WaveletAnalysis(channel).wavelet_transform))
            wav_ictal_data.extend(ictal_wavelets)

        interictal_channels = interictal_files[index].get('data')
        for channel in interictal_channels:
            channel = ss.decimate(channel, datasize)
            interictal_wavelets = np.transpose(np.real(WaveletAnalysis(channel).wavelet_transform))
            wav_interictal_data.extend(interictal_wavelets)

    pca = PCA(n_components=16)
    ictal_data = pca.fit_transform(wav_ictal_data)
    interictal_data = pca.fit_transform(wav_interictal_data)
    print "Analyzed %d files for patient" % num_files

    return ictal_data, interictal_data

if __name__ == '__main__':
    main()
