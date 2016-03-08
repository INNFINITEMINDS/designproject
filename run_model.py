from util import *
import nn
import numpy as np
import sys


def main(data_source):
    # data_source = "../shared_dir/kaggle_data/clips/"
    train_data, train_labels, valid_data, valid_labels = generate_datasets(data_source)
    net = nn.nn_setup()
    while 1:
        pid = os.fork()
        if pid == 0:
            nn.run_nn(net, train_data, train_labels, valid_data, valid_labels)
        else:
            ret = os.waitpid(pid, 0)

        raw_input('Press enter to restart')
        net.reset()
        reload(nn)


def generate_datasets(data_source):
    print "Preparing to load data from %s" % data_source
    # data_var = ''
    # patient_data = []

    if "kaggle" in data_source:
        data_var = 'data'
        patient_data = load_all_patients(data_source)
    else:
        data_var = 'filtered_data'
        patient_data = load_all_freq_bands(data_source)

    train_data = []
    valid_data = []
    train_labels = []
    valid_labels = []

    for patient in patient_data:
        ictal_files = patient[1]
        interictal_files = patient[2]

        num_files = min(len(ictal_files), len(interictal_files))

        ictal_data = []
        interictal_data = []

        for index in range(0, num_files):
            ictal_data.extend(ictal_files[index].get(data_var))
        for index in range(0, num_files):
            interictal_data.extend(interictal_files[index].get(data_var))

        # num_channels = len(ictal_data) / 50

        ictal_data = np.reshape(ictal_data, (-1, 50))
        interictal_data = np.reshape(interictal_data, (-1, 50))
        num_valid = int(round(num_files / 4))
        num_train = num_files - num_valid

        train_data.extend(np.vstack([ictal_data[:num_train], interictal_data[:num_train]]))

        train_labels.extend(np.ones(num_train))
        train_labels.extend(np.zeros(num_train))

        valid_data.extend(np.vstack([ictal_data[num_train:num_files], interictal_data[num_train:num_files]]))

        valid_labels.extend(np.ones(num_valid))
        valid_labels.extend(np.zeros(num_valid))

        return train_data, train_labels, valid_data, valid_labels


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python run_model.py <data_file_path>"
        sys.exit(1)

    main(sys.argv[1])
