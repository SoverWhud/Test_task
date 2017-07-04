function [x, noise] = collectPlaneWaveWithNoise(fc, URA_size, URA_elementSpacing)

fs = 8000;
t = (0:1/fs:1).';

x1 = cos(2*pi*t*300);
x2 = cos(2*pi*t*400);

ha = phased.URA('Size',URA_size,'ElementSpacing',URA_elementSpacing);

ha.Element.FrequencyRange = [100e6 300e6];

x = collectPlaneWave(ha,[x1 x2],[-37 0;17 20]',fc);

% additive noise
noise = 0.1*(randn(size(x))+1i*randn(size(x)));

% construct MVDR DOA estimator for URA
hdoa = phased.MVDREstimator2D('SensorArray',ha,...
    'OperatingFrequency',fc,...
    'DOAOutputPort',true,'NumSignals',2,...
    'AzimuthScanAngles',-50:50,...
    'ElevationScanAngles',-30:30);

% use the step method to obtain the output and DOA estimates
[~,doas] = step(hdoa,x+noise);

save('hdoa.mat', 'hdoa');
save('doas.mat', 'doas');
end