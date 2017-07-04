import scipy.io
import numpy as np
import math
import phased
import copy

import matlab.engine

fc = 150e6
URA_size = [5, 10]
URA_elementSpacing = [1, 0.6]

eng = matlab.engine.start_matlab()
res = eng.collectPlaneWaveWithNoise(fc, matlab.double(URA_size), matlab.double(URA_elementSpacing))

x = np.array(res[0])
noise = np.array(res[1])

ha = phased.URA(size=URA_size, elementSpacing=URA_elementSpacing);

hdoa = phased.MVDREstimator2D(sensorArray=ha,
                              operatingFrequency=fc,
                              dOAOutputPort=True,
                              numSignals=2,
                              azimuthScanAngles=np.arange(-50, 51),
                              elevationScanAngles=np.arange(-30, 31))

(_, doa) = hdoa.step(x+noise)

# test = scipy.io.loadmat('file1.mat')
#
# np.testing.assert_array_equal(test['H'], x + noise)
