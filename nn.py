import pybrain.structure as ps
import pybrain.datasets as pd
from pybrain.supervised.trainers import BackpropTrainer
import numpy as np
from util import *


def nn_setup():
    # Create NN
    net = ps.FeedForwardNetwork()

    inputLayer = ps.LinearLayer(68)
    hiddenLayer = ps.SigmoidLayer(34)
    outputLayer = ps.LinearLayer(1)

    input_to_hidden = ps.FullConnection(inputLayer, hiddenLayer)
    hidden_to_output = ps.FullConnection(hiddenLayer, outputLayer)

    # Add input, hidden and output layers and connections
    net.addInputModule(inputLayer)
    net.addModule(hiddenLayer)
    net.addOutputModule(outputLayer)

    net.addConnection(input_to_hidden)
    net.addConnection(hidden_to_output)

    # Initialize NN
    net.sortModules()
    return net


def nn():
    dataSource = "../clips/other"

    ictal_data, interictal_data, test_data = load_for_patient(dataSource)

    ictal = np.asarray(ictal_data)
    interictal = np.asarray(interictal_data)

    ictal_data = np.split(ictal, 3)
    interictal_data = np.split(interictal, 3)

    train_data = np.vstack([ictal_data[0], interictal_data[0]])
    valid_data = np.vstack([ictal_data[1], interictal_data[1]])
    test_data = np.vstack([ictal_data[2], interictal_data[2]])

    ntrain = train_data.size
    nvalid = valid_data.size
    ntest = test_data.size

    train_dataset = pd.SupervisedDataSet(68, 1)

    for index in range(ntrain):
        if index < ntrain / 2:
            train_dataset.addSample(train_data[index], 1)
        else:
            train_dataset.addSample(train_data[index], 0)

    net = nn_setup()

    trainer = BackpropTrainer(net, train_dataset)

    err = trainer.train()

    print "Error: %f" % err
