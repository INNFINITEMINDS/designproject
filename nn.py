import numpy as np
import pybrain.datasets as pd
import pybrain.structure as ps
from pybrain.supervised.trainers import BackpropTrainer
import pickle
from request import *

indim = 16
outdim = 1


def nn_setup():
    # Create NN
    net = ps.FeedForwardNetwork()

    input_layer = ps.LinearLayer(indim)
    hidden_layer1 = ps.SigmoidLayer(10)
    hidden_layer2 = ps.SigmoidLayer(8)
    output_layer = ps.SigmoidLayer(outdim)

    input_to_hidden = ps.FullConnection(input_layer, hidden_layer1)
    hidden1_to_hidden2 = ps.FullConnection(hidden_layer1, hidden_layer2)
    hidden2_to_output = ps.FullConnection(hidden_layer2, output_layer)

    # Add input, hidden and output layers and connections
    net.addInputModule(input_layer)
    net.addModule(hidden_layer1)
    net.addModule(hidden_layer2)
    net.addOutputModule(output_layer)

    net.addConnection(input_to_hidden)
    net.addConnection(hidden1_to_hidden2)
    net.addConnection(hidden2_to_output)

    # Initialize NN
    net.sortModules()
    return net


def train_network_until_convergence(net, train_data, train_labels, valid_data, valid_labels, max_error=0.05,
                                    conv=0.0001, file_path=None):
    output_file = None
    if file_path is not None:
        output_file = open(file_path, "wb+")

    # Run training until high enough values are reached
    valid_error = 1
    train_error = 0
    num_epoch = 0

    train_error_history = []
    valid_error_history = []
    true_pos_history = []
    true_neg_history = []

    print "Training network..."

    while valid_error > max_error:
        num_epoch += 1
        net, train_error = train_nn(net, train_data, train_labels)
        new_valid_error, true_pos, true_neg = run_nn(net, valid_data, valid_labels)
        if abs(valid_error - new_valid_error) < conv:
            max_error = valid_error
        valid_error = new_valid_error
        correct_pred = (1 - valid_error) * 100

        print "Epoch %d, train error: %4f, valid_error: %4f" % (num_epoch, train_error, valid_error)
        print "Correct predictions: %2f %%, true positives: %4f, true negatives: %4f" % (
        correct_pred, true_pos, true_neg)
        if output_file is not None:
            train_error_history.append(train_error)
            valid_error_history.append(valid_error)
            true_pos_history.append(true_pos)
            true_neg_history.append(true_neg)

    if output_file is not None:
        result = {'train_error': train_error_history, 'valid_error': valid_error_history, 'true_pos': true_pos_history,
                  'true_neg': true_neg_history}
        pickle.dump(result, output_file)
        output_file.close()

    return net


def train_nn(net, train_data, train_labels):
    ntrain = len(train_data)
    train_dataset = pd.SupervisedDataSet(indim, outdim)

    for index in range(ntrain):
        train_dataset.addSample(train_data[index], train_labels[index])

    trainer = BackpropTrainer(net, train_dataset)
    train_error = trainer.train()

    return net, train_error


def run_nn(net, valid_data, valid_labels):
    output = []

    for datapt in valid_data:
        output_pt = np.round(net.activate(datapt))
        output.append(output_pt)

    valid_output = np.concatenate(output)
    nvalid = len(valid_data)

    # Calculate validation statistics
    valid_error = (nvalid - sum(np.equal(valid_output, valid_labels))) / float(nvalid)
    true_pos = sum(np.logical_and(valid_output, valid_labels)) / sum(valid_labels)
    true_neg = (nvalid - sum(np.logical_xor(valid_output, valid_labels)) - sum(
        np.logical_and(valid_output, valid_labels))) / (nvalid - sum(valid_labels))

    return valid_error, true_pos, true_neg


def test_nn(net, test_data, test_labels):
    output = []
    datapts_sec = 500
    num_seizures = 0
    default_check = 2 * datapts_sec
    check = default_check

    last_second = np.zeros(datapts_sec)
    for i in range(len(test_data)):
        # if i % datapts_sec == 0:
        #     time.sleep(1)
        output_pt = np.round(net.activate(test_data[i]))
        num = i % datapts_sec
        last_second.put(num, output_pt)
        output.append(output_pt)
        average = sum(last_second) / datapts_sec
        if (output_pt == 1) and (average > 0.5):
            # seizure
            if check == default_check:
                num_seizures += 1
                # thread.start_new_thread(send, ())
                send()

            check = 0
        else:
            if check < default_check:
                check += 1

    valid_output = np.concatenate(output)
    ntest = len(test_data)

    # Calculate validation statistics
    test_error = (ntest - sum(np.equal(valid_output, test_labels))) / float(ntest)
    if sum(test_labels) == 0:
        true_pos = 0
    else:
        true_pos = sum(np.logical_and(valid_output, test_labels)) / sum(test_labels)

    if ntest - sum(test_labels) == 0:
        true_neg = 0
    else:
        true_neg = (ntest - sum(np.logical_xor(valid_output, test_labels)) - sum(
        np.logical_and(valid_output, test_labels))) / (ntest - sum(test_labels))

    return test_error, true_pos, true_neg, num_seizures
