function[] = filter_kaggle_data(band_type, bound)

narginchk(2,2);
validStrings = cellstr(['alpha';'beta ';'gamma';'delta';'theta']);
validatestring(band_type, validStrings);

num_patients = 1;
path_to_patient_clips = '/u/course/ece496y/ece496y1/kaggle_data/clips/Patient_';
path_to_filtered_clips = '/u/d/dadlanid/tempdata/filtered_data/Patient_';

for i = 1:num_patients
    tic;
   dirnum = num2str(i);
   path = strcat(path_to_patient_clips, dirnum, '/');
   dir = what(path);
   datafiles = dir.mat;
   
    for j = 1:numel(datafiles)
       filename = char(datafiles(j));
       is_test = strfind(filename, 'test');
       if (is_test ~= 0)
           continue;
       end
       
       load(char(datafiles(j)));
       
       filtered_data = eeg_bp_filter(data, freq, bound);
       
       new_path = strcat(path_to_filtered_clips, dirnum, '/');
       folder = fullfile(new_path, band_type);
       if ~exist(folder, 'dir')
           mkdir(folder);
       end
           
       new_filename = strcat(folder, '/', filename(1:end-4), '_', band_type, 'band.mat');
       
       save(new_filename, 'filtered_data','band_type', 'freq');
       
   toc;
   end
    
end