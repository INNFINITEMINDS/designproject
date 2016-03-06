import pybrain.structure as ps
import pybrain.datasets as pd
from pybrain.supervised.trainers import BackpropTrainer
import numpy as np
from util import *


# from WaveletLayer import *


def nn_setup():
    # Create NN
    net = ps.FeedForwardNetwork()

    input_layer = ps.LinearLayer(50)
    hidden_layer1 = ps.SigmoidLayer(40)
    hidden_layer2 = ps.SigmoidLayer(20)
    hidden_layer3 = ps.SigmoidLayer(10)
    output_layer = ps.SigmoidLayer(1)

    input_to_hidden = ps.FullConnection(input_layer, hidden_layer1)
    hidden1_to_hidden2 = ps.FullConnection(hidden_layer1, hidden_layer2)
    hidden2_to_hidden3 = ps.FullConnection(hidden_layer2, hidden_layer3)
    hidden3_to_output = ps.FullConnection(hidden_layer3, output_layer)

    # Add input, hidden and output layers and connections
    net.addInputModule(input_layer)
    net.addModule(hidden_layer1)
    net.addModule(hidden_layer2)
    net.addModule(hidden_layer3)
    net.addOutputModule(output_layer)

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

    print "Preparing to load data from %s" % data_source
    # ictal_files, interictal_files = load_freq_bands_for_patient(data_source)
    patient_data = load_all_freq_bands(data_source)

    train_data = []
    valid_data = []
    train_labels = []
    valid_labels = []

    for patient in patient_data:
        num_samples = int(patient[0])
        ictal_files = patient[1]
        interictal_files = patient[2]

        # Number of ictal OR interictal files. Total files will be num_files*2
        num_files = min(len(ictal_files), len(interictal_files))

        ictal_data = []
        interictal_data = []

        for index in range(0, num_files):
            ictal_data.extend(ictal_files[index].get('filtered_data'))
        for index in range(0, num_files):
            interictal_data.extend(interictal_files[index].get('filtered_data'))

        num_channels = len(ictal_data) / 50

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
    while epochs < 200:
        train_error = trainer.train()
        print "Epoch %d, Training error: %f" % (epochs, train_error)
        epochs += 1

    print "Generating validation dataset"

    for index in range(nvalid):
        valid_dataset.addSample(valid_data[index], valid_labels[index])

    print "Classifying validation data"
    output = np.round(np.concatenate(net.activateOnDataset(valid_dataset)))

    valid_error = (nvalid - sum(np.equal(output, valid_labels))) / float(nvalid)
    print "Validation error: %f" % valid_error
    correct_pred = (1 - valid_error) * 100
    print "Correct predictions : %.2f%%" % correct_pred

if __name__ == '__main__':
    main()
