import sys
import pybrain.structure as ps
import pybrain.datasets as pd
from pybrain.supervised.trainers import BackpropTrainer
import numpy as np


# from WaveletLayer import *


def nn_setup():
    # Create NN
    net = ps.FeedForwardNetwork()

    input_layer = ps.LinearLayer(50)
    hidden_layer1 = ps.SigmoidLayer(40)
    hidden_layer2 = ps.SigmoidLayer(30)
    hidden_layer3 = ps.SigmoidLayer(20)
    hidden_layer4 = ps.SigmoidLayer(10)
    output_layer = ps.SigmoidLayer(1)

    input_to_hidden = ps.FullConnection(input_layer, hidden_layer1)
    hidden1_to_hidden2 = ps.FullConnection(hidden_layer1, hidden_layer2)
    hidden2_to_hidden3 = ps.FullConnection(hidden_layer2, hidden_layer3)
    hidden3_to_hidden4 = ps.FullConnection(hidden_layer3, hidden_layer4)
    hidden4_to_output = ps.FullConnection(hidden_layer4, output_layer)

    # Add input, hidden and output layers and connections
    net.addInputModule(input_layer)
    net.addModule(hidden_layer1)
    net.addModule(hidden_layer2)
    net.addModule(hidden_layer3)
    net.addModule(hidden_layer4)
    net.addOutputModule(output_layer)

    net.addConnection(input_to_hidden)
    net.addConnection(hidden1_to_hidden2)
    net.addConnection(hidden2_to_hidden3)
    net.addConnection(hidden3_to_hidden4)
    net.addConnection(hidden4_to_output)

    # Initialize NN
    net.sortModules()
    return net


def run_nn(net, train_data, train_labels, valid_data, valid_labels):
    nvalid = len(valid_data)
    ntrain = len(train_data)

    print "Generating training dataset"
    train_dataset = pd.SupervisedDataSet(50, 1)
    valid_dataset = pd.ClassificationDataSet(50, 1)

    for index in range(ntrain):
        train_dataset.addSample(train_data[index], train_labels[index])

    # net = nn_setup()

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

    true_pos = sum(np.logical_and(output, valid_labels)) / sum(valid_labels)
    true_neg = (nvalid - sum(np.logical_xor(output, valid_labels)) - sum(np.logical_and(output, valid_labels))) / (nvalid - sum(valid_labels))

    print "True pos: %f, True neg: %f" % (true_pos, true_neg)

