
function [y] = eeg_bp_filter(x, Fs, bound)

bound = bound / (Fs/2);

t = (0:length(x) - 1) / Fs;
% new_t = (0:699)/Fs;
% new_x = zeros(1, 700);
% new_x(1:500) = x;

blo = fir1(99,bound, chebwin(100));
freqz(blo,1);

% figure(2);
% y = filter(blo,1,new_x);
y = filter(blo,1,x);

if isnan(y)
    error('NaN found.');
end


%% Plots to see the filtered output
% subplot(4,1,1)
% plot(abs(x))
% title ('FFT of original Signal');
% 
% subplot(4,1,2)
% plot(t,x)
% title('Original Signal')
% ys = ylim;
% 
% subplot(4,1,3)
% % plot(new_t,y)
% plot(t,y);
% title('Lowpass Filtered Signal')
% xlabel('Time (s)')
% ylim(ys)
% 
% fdata = fft(y);
% subplot(4,1,4)
% plot(abs(fdata(1:length(fdata)/2)));
% title('FFT')

