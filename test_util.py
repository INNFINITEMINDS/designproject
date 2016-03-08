import os
import scipy.io as sio
from nn import *
import pickle
from pybrain.tools.customxml.networkreader import NetworkReader

testfile_path = "/home/divd/ece496/nets/test_set.p"
netfile_path = "/home/divd/ece496/nets/final_last_bestnet_8.p"


def main():
    testfile = open(testfile_path, 'rb+')

    testdict = pickle.load(testfile)
    test_data = testdict['test_data']
    test_labels = testdict['test_labels']

    test_case_data, test_case_labels, test_num_seizures = generate_test_cases(test_labels, test_data)

    net = NetworkReader.readFrom(netfile_path)

    for i in range(len(test_case_data)):
        test_error, true_pos, true_neg, num_seizures = test_nn(net, test_case_data[i], test_case_labels[i])
        print "Test error: %02f, True pos: %02f, True neg: %02f" % (test_error, true_pos, true_neg)
        print "Number of seizures detected: %d, Actual number of seizures: %d" % (num_seizures, test_num_seizures[i])
        raw_input("Press enter for next case")


def check_for(src, dst, value, message):
    src = np.array(src)
    dst = np.array(dst)

    src_first_interictal = np.argmax(src == value)
    dst_first_interictal = np.argmax(dst == value)
    print '%s, src = %d, dst = %d, difference = %d' % (
    message, src_first_interictal, dst_first_interictal, dst_first_interictal - src_first_interictal)


def check_trail(src, dst):
    import pdb;
    pdb.set_trace()
    src = np.array(src)
    dst = np.array(dst)

    check_for(src, dst, 0, "first interictal")
    check_for(src, dst, 1, "first cictal")


def generate_test_cases(inp_labels, inp_data):
    test_case_data = []
    test_case_labels = []
    test_num_seizures = []

    data_index = len(inp_data) / 2
    ictal_data = inp_data[:data_index]
    interictal_data = inp_data[data_index:]

    label_index = len(inp_data) / 2
    ictal_labels = inp_labels[:label_index]
    interictal_labels = inp_labels[label_index:]

    ictal_index = 0
    interictal_index = 0

    # 30 seconds of ictal + 3 seconds of interictal
    length = 10 * 500
    test_1_data = np.concatenate(
        (ictal_data[ictal_index: ictal_index + length], interictal_data[interictal_index: interictal_index + length]))
    test_1_labels = np.concatenate((ictal_labels[ictal_index: ictal_index + length],
                                    interictal_labels[interictal_index: interictal_index + length]))
    ictal_index += length
    interictal_index += length

    test_case_data.append(test_1_data)
    test_case_labels.append(test_1_labels)
    test_num_seizures.append(1)

    # + 30 seconds of ictal
    length = 10 * 500
    test_1_data = ictal_data[ictal_index: ictal_index + length]
    test_1_labels = ictal_labels[ictal_index: ictal_index + length]
    ictal_index += length

    test_case_data.append(test_1_data)
    test_case_labels.append(test_1_labels)
    test_num_seizures.append(1)

    # 30 seconds interictal
    length = 10 * 500
    test_1_data = interictal_data[interictal_index: interictal_index + length]
    test_1_labels = interictal_labels[interictal_index: interictal_index + length]
    interictal_index += length

    test_case_data.append(test_1_data)
    test_case_labels.append(test_1_labels)
    test_num_seizures.append(0)

    # # Ictal, interictal, ictal
    length = 10 * 500
    test_1_data = np.concatenate(
        (ictal_data[ictal_index: ictal_index + length], interictal_data[interictal_index: interictal_index + length], ictal_data[ictal_index + length: ictal_index + length*2]))
    test_1_labels = np.concatenate((ictal_labels[ictal_index: ictal_index + length],
                                    interictal_labels[interictal_index: interictal_index + length], ictal_labels[ictal_index + length: ictal_index + length*2]))
    ictal_index += length*2
    interictal_index += length

    test_case_data.append(test_1_data)
    test_case_labels.append(test_1_labels)
    test_num_seizures.append(2)

    return test_case_data, test_case_labels, test_num_seizures


if __name__ == '__main__':
    main()
