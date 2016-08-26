function[] = extract_feature(feature_name)
%% Copy this script and use it to run your own function.
% This script will save it to the folder specified by <feature_name>
% in filtered_data/Patient_#/

%% Validate function arguments if necessary here:
%
%

num_patients = 8;
path_to_patient_clips = '/u/course/ece496y/ece496y1/kaggle_data/clips/Patient_';
path_to_feature_clips = '/u/course/ece496y/ece496y1/filtered_data/Patient_';

%% Default path to store feature clips:
% /u/course/ece496/ece496y1/filtered_data/Patient_#/<feature_name>/Patient_#_ictal_segment_1_<feature_name>.mat
% Change feature name as needed

for i = 1:num_patients
   dirnum = num2str(i);
   path = strcat(path_to_patient_clips, dirnum, '/');
   dir = what(path);
   datafiles = dir.mat;
   
   %% Ignore test data 
   %  (don't want to extract features from that yet)
    for j = 1:numel(datafiles)
       filename = char(datafiles(j));
       is_test = strfind(filename, 'test');
       if (is_test ~= 0)
           continue;
       end
       
       load(char(datafiles(j)));
       %% Call the function here
       % Change this to be your own function - eg: get_power
       % feature_data = func(args);
       
       
       new_path = strcat(path_to_feature_clips, dirnum, '/');
       folder = fullfile(new_path, feature_name);
       if ~exist(folder, 'dir')
           mkdir(folder);
       end
           
       new_filename = strcat(folder, '/', filename(1:end-4), '_', feature_name, '.mat');
       
       %% Change this to save the variables that you want to save
       % save(new_filename, 'feature_data','feature_name', 'freq');
       
   
   end
    
end