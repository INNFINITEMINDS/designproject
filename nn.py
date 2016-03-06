import pybrain.structure as ps
import pybrain.datasets as pd
from pybrain.supervised.trainers import BackpropTrainer
import numpy as np
from util import *


# from WaveletLayer import *


def nn_setup():
    # Create NN
    net = ps.FeedForwardNetwork()

    inputLayer = ps.LinearLayer(50)
    hiddenLayer1 = ps.SigmoidLayer(10)
    hiddenLayer2 = ps.SigmoidLayer(20)
    hiddenLayer3 = ps.SigmoidLayer(10)
    outputLayer = ps.SigmoidLayer(1)

    input_to_hidden = ps.FullConnection(inputLayer, hiddenLayer1)
    hidden1_to_hidden2 = ps.FullConnection(hiddenLayer1, hiddenLayer2)
    hidden2_to_hidden3 = ps.FullConnection(hiddenLayer2, hiddenLayer3)
    hidden3_to_output = ps.FullConnection(hiddenLayer1, outputLayer)

    # Add input, hidden and output layers and connections
    net.addInputModule(inputLayer)
    net.addModule(hiddenLayer1)
    net.addModule(hiddenLayer2)
    net.addModule(hiddenLayer3)
    net.addOutputModule(outputLayer)

    net.addConnection(input_to_hidden)
    net.addConnection(hidden1_to_hidden2)
    net.addConnection(hidden2_to_hidden3)
    net.addConnection(hidden3_to_output)

    # Initialize NN
    net.sortModules()
    return net


def main():
    # data_source = "../clips/"
    data_source = "../shared_dir/filtered_data/"
    # num_channels = 68
    # num_samples = 500

    print "Loading data files from files at %s" % data_source
    # ictal_files, interictal_files = load_freq_bands_for_patient(data_source)
    patient_data = load_all_freq_bands(data_source)

    train_data = []
    valid_data = []
    train_labels = []
    valid_labels = []

    for patient in patient_data:
        num_channels = patient[0]
        num_samples = patient[1]
        ictal_files = patient[2]
        interictal_files = patient[3]

        # Number of ictal OR interictal files. Total files will be num_files*2
        num_files = min(len(ictal_files), len(interictal_files))

        ictal_data = np.zeros((num_files, num_channels, num_samples))
        interictal_data = np.zeros((num_files, num_channels, num_samples))

        for index in range(0, num_files):
            ictal_data[index] = ictal_files[index].get('filtered_data')
        for index in range(0, num_files):
            interictal_data[index] = interictal_files[index].get('filtered_data')

        dim = (num_samples / 50) * num_channels * num_files

        ictal_data = np.reshape(ictal_data, (dim, 50))
        interictal_data = np.reshape(interictal_data, (dim, 50))
        # num_valid_files = int(round(num_files / 3))
        # num_train_files = num_files - num_valid_files
        num_valid = int(round(num_files / 3))
        num_train = num_files - num_valid

        train_data.extend(np.vstack([ictal_data[:num_train], interictal_data[:num_train]]))
        train_labels.extend(np.vstack([np.ones(num_train), np.zeros(num_train)]))
        valid_data.extend(np.vstack([ictal_data[num_train:num_files], interictal_data[num_train:num_files]]))
        valid_labels.extend(np.vstack([np.ones(num_valid), np.zeros(num_valid)]))
        # train_data.extend(
        #     np.reshape(np.vstack([ictal_data[:num_train_files, :, :], interictal_data[:num_train_files, :, :]]),
        #                (num_train_files * num_channels * dim * 2, 50)))
        # valid_data.extend(np.reshape(
        #     np.vstack([ictal_data[num_train_files:num_train_files + num_valid_files:, :, :],
        #                interictal_data[num_train_files:num_train_files + num_valid_files, :, :]]),
        #     (num_valid_files * num_channels * dim * 2, 50)))

    nvalid = len(valid_data)
    ntrain = len(train_data)

    print "Generating training dataset"
    train_dataset = pd.SupervisedDataSet(50, 1)
    valid_dataset = pd.ClassificationDataSet(50, 1)

    for index in range(ntrain):
        train_dataset.addSample(train_data[index], train_labels[index])

    net = nn_setup()

    print("Training network on given data")
    trainer = BackpropTrainer(net, train_dataset)
    epochs = 0
    train_error = 1.0
    while epochs < 1:
        train_error = trainer.train()
        print "Epoch %d, Training error: %f" % (epochs, train_error)
        epochs += 1

    # print "Training error: %f" % train_error

    print "Generating validation dataset"

    for index in range(nvalid):
        valid_dataset.addSample(valid_data[index], valid_labels[index])

    print "Classifying validation data"
    # output = np.round(np.concatenate(net.activateOnDataset(valid_dataset)))
    output = net.activateOnDataset(valid_dataset)
    # num = len(output)
    # classif = np.zeros(nvalid)
    # for i in range(num):
    #     # print i
    #     if output[i, 0] > output[i, 1]:
    #         classif[i] = 1
    #
    #     else:
    #         classif[i] = 0
    # labels = np.append(np.ones(nvalid / 2), np.zeros(nvalid - (nvalid / 2)))

    valid_error = (nvalid - sum(np.equal(output, valid_labels))) / float(nvalid)
    print "Validation error: %f" % valid_error


if __name__ == '__main__':
    main()
