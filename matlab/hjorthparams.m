clear all;
close all;

ictal = load('Patient_1_ictal_segment_1.mat');
interictal = load('Patient_1_interictal_segment_1.mat');

num_channels = size(ictal.data, 1);
fs = ictal.freq;
activity = zeros(num_channels, 1);
filtered_signal = size(ictal.data);

    activity = var(ictal.data);
    filtered_signal = eeg_bp_filter(ictal.data, ictal.freq,  120);

