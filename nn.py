import pybrain.structure as ps
import pybrain.datasets as pd
from pybrain.supervised.trainers import BackpropTrainer
import numpy as np
from util import *


def nn_setup():
    # Create NN
    net = ps.FeedForwardNetwork()

    inputLayer = ps.LinearLayer(68)
    hiddenLayer1 = ps.SigmoidLayer(34)
    hiddenLayer2 = ps.SigmoidLayer(34)
    outputLayer = ps.LinearLayer(1)

    input_to_hidden = ps.FullConnection(inputLayer, hiddenLayer1)
    hidden_to_hidden = ps.FullConnection(hiddenLayer1, hiddenLayer2)
    hidden_to_output = ps.FullConnection(hiddenLayer2, outputLayer)

    # Add input, hidden and output layers and connections
    net.addInputModule(inputLayer)
    net.addModule(hiddenLayer1)
    net.addModule(hiddenLayer2)
    net.addOutputModule(outputLayer)

    net.addConnection(input_to_hidden)
    net.addConnection(hidden_to_hidden)
    net.addConnection(hidden_to_output)

    # Initialize NN
    net.sortModules()
    return net


def main():
    data_source = "../clips"

    ictal_data = np.zeros((30, 68, 500))
    interictal_data = np.zeros((30, 68, 500))

    ictal_files, interictal_files, test_files = load_for_patient(data_source)

    for index in range(0, len(ictal_files)):
        ictal_data[index], ictal_freq, ictal_channels, ictal_latency = get_contents_at_index(ictal_files, index)

    for index in range(0, len(interictal_files)):
        interictal_data[index], interictal_freq, interictal_channels, interictal_latency = get_contents_at_index(
            interictal_files, index)

    ictal = np.split(ictal_data, 3)
    interictal = np.split(interictal_data, 3)

    train_data = np.reshape(np.vstack([ictal[0], ictal[1], interictal[0], interictal[1]]), (20000, 68))
    valid_data = np.reshape(np.vstack([ictal[2], interictal[2]]), (10000, 68))

    ntrain = train_data.shape[0]
    nvalid = valid_data.shape[0]

    print "Generating training dataset"
    train_dataset = pd.SupervisedDataSet(68, 1)
    valid_dataset = pd.ClassificationDataSet(68, 1)

    for index in range(ntrain):
        if index < ntrain / 2:
            train_dataset.addSample(train_data[index], 1)
        else:
            train_dataset.addSample(train_data[index], 0)

    net = nn_setup()

    print("Training network on given data")
    trainer = BackpropTrainer(net, train_dataset)

    train_error = trainer.train()

    print "Training error: %f" % train_error

    print "Generating validation dataset"

    for index in range(nvalid):
        if index < ntrain / 2:
            valid_dataset.addSample(valid_data[index], 1)
        else:
            valid_dataset.addSample(valid_data[index], 0)

    print "Classifying validation data"
    output = np.round(np.concatenate(net.activateOnDataset(valid_dataset)))
    labels = np.append(np.ones(5000), np.zeros(5000))

    valid_error = (nvalid - sum(np.equal(output, labels)))/float(nvalid)
    print "Validation error: %f" % valid_error


if __name__ == '__main__':
    main()
