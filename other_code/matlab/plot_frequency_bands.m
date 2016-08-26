
patient_filtered_clips = '/u/course/ece496y/ece496y1/filtered_data/Patient_1/';

bands = ['alpha';'beta ';'gamma';'theta';'delta'];

ictal_clip = 'Patient_1_ictal_segment_1_';
interictal_clip = 'Patient_1_interictal_segment_1_';

for i = 1:length(bands)
   band = bands(i,:);
   ictal_path = strcat(patient_filtered_clips, band, '/', ictal_clip, band, 'band');
   ictal = load(ictal_path);
   
   figure(i);
   subplot (2,1,1);
   plot(ictal.filtered_data(1,:));
   title('Ictal Segment');
   xlabel('Time');
   ylabel('Amplitude');
   
   interictal_path = strcat(patient_filtered_clips, band, '/', interictal_clip, band, 'band');
   interictal = load(interictal_path);

   subplot (2,1,2);
   plot(interictal.filtered_data(1,:));
   title('Interictal Segment');
   xlabel('Time');
   ylabel('Amplitude');
   
end

