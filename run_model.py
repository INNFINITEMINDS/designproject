import scipy.signal as ss
from sklearn.decomposition import PCA
from wavelets import WaveletAnalysis
from datetime import datetime
import time
from pybrain.tools.customxml.networkwriter import NetworkWriter
import pickle;

import nn
from features import *

default_src = "/home/divd/ece496/shared_dir/kaggle_data/training/"
net_file_base = "/home/divd/ece496/nets/bestnet_"
result_path = "/home/divd/ece496/nets/results.txt"
testset_path = "/home/divd/ece496/nets/test_set.p"


def main(data_source=default_src):
    train_data, train_labels, valid_data, valid_labels, test_data, test_labels = generate_datasets(data_source)
    # train_data = np.random.rand(500, 16)
    # train_labels = np.random.rand(500, 1)
    # valid_data = np.random.rand(500, 16)
    # valid_labels = np.random.rand(500, 1)

    net = nn.nn_setup()

    timestamp = datetime.now().strftime("%Y%m%d_%H:%M:%S")
    netpath = net_file_base + timestamp + ".p"

    trained_net = nn.train_network_until_convergence(net, train_data, train_labels, valid_data, valid_labels,
                                                  file_path=result_path)
    NetworkWriter.writeToFile(trained_net, netpath)
    testset_file = open(testset_path, "wb+")
    test_set = {'test_data' : test_data, 'test_labels' : test_labels}
    pickle.dump(test_set, testset_file)

def generate_datasets(data_source):
    print "Preparing to load data from %s" % data_source

    data_var = 'data'
    if "Patient" in data_source:
        patient_data = []
        patient_data.insert(0, load_for_patient(data_source))
    else:
        start_time_load = time.time()
        patient_data = load_all_patients(data_source)
        print "Time taken to load %d patients: %f" % (len(patient_data), time.time() - start_time_load)

    wav_ictal_data = []
    wav_interictal_data = []

    pnum = 1
    start_time_patient_process = time.time()
    for patient in patient_data:
        print "Processing data for patient %d" % pnum
        freq = patient[0]
        ictal_files = patient[1]
        interictal_files = patient[2]

        num_files = min(len(ictal_files), len(interictal_files))
        datasize = int(round(freq / 10))

        for index in range(0, num_files):
            # print "Processing file %d " % index
            ictal_channels = ictal_files[index].get(data_var)
            for channel in ictal_channels:
                channel = ss.decimate(channel, datasize)
                ictal_wavelets = np.transpose(np.real(WaveletAnalysis(channel).wavelet_transform))
                wav_ictal_data.extend(ictal_wavelets)

            interictal_channels = interictal_files[index].get(data_var)
            for channel in interictal_channels:
                channel = ss.decimate(channel, datasize)
                interictal_wavelets = np.transpose(np.real(WaveletAnalysis(channel).wavelet_transform))
                wav_interictal_data.extend(interictal_wavelets)

        pnum += 1

    pca = PCA(n_components=16)
    ictal_data = pca.fit_transform(wav_ictal_data)
    interictal_data = pca.fit_transform(wav_interictal_data)

    print "Generating datasets"
    num_datapts = len(ictal_data)

    # train_data = []
    # train_labels = []
    #
    # valid_data = []
    # valid_labels = []
    #
    # test_data = []
    # test_labels = []

    # seed = np.random.get_state()
    np.random.shuffle(ictal_data)
    # np.random.set_state(seed)
    np.random.shuffle(interictal_data)

    num_test = int(round(num_datapts / 5))
    num_valid = int((num_datapts - num_test) / 4)
    num_train = num_datapts - num_valid - num_test

    train_data = np.array(np.vstack([ictal_data[:num_train], interictal_data[:num_train]]))
    train_labels = np.concatenate([np.ones(num_train), np.zeros(num_train)])

    seed = np.random.get_state()
    np.random.shuffle(train_data)
    np.random.set_state(seed)
    np.random.shuffle(train_labels)

    valid_data = np.array(np.vstack([ictal_data[num_train:num_train + num_valid], interictal_data[num_train:num_train + num_valid]]))
    valid_labels = np.concatenate([np.ones(num_valid), np.zeros(num_valid)])

    seed = np.random.get_state()
    np.random.shuffle(valid_data)
    np.random.set_state(seed)
    np.random.shuffle(valid_labels)

    test_data = np.array(np.vstack([ictal_data[num_train + num_valid:num_datapts], interictal_data[num_train + num_valid:num_datapts]]))
    test_labels = np.concatenate([np.ones(num_test), np.zeros(num_test)])


    print "Time taken to process files: %f" % (time.time() - start_time_patient_process)
    return train_data, train_labels, valid_data, valid_labels, test_data, test_labels


if __name__ == '__main__':
    main()
