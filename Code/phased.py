import numpy as np


class URA:
    def __init__(self, size=None, elementSpacing=None):
        self.__size = size if size is not None else [2, 2]
        self.__elementSpacing = elementSpacing if elementSpacing is not None else [0.5, 0.5]

    @property
    def Size(self):
        return self.__size

    @property
    def ElementSpacing(self):
        return self.__elementSpacing


class AbstractSpectralDOA(object):
    def __init__(self, numSignals=1, azimuthScanAngles=np.arange(-90, 90), elevationScanAngles=0):
        self.__azimuthScanAngles = azimuthScanAngles
        self.__elevationScanAngles = elevationScanAngles
        self.__numSignals = numSignals

        self.__patternSize = None
        self.__pattern = None
        self.__steeringVector = None
        self.__isOneCut = None

        self.__scanAngles = None
        self.__numIter = None
        self.__scanAngleBlockSize = None
        self.__oneIterFlag = None

        self.__scanAngleBlockIndex = None

    @property
    def PatternSize(self):
        return self.__patternSize

    @PatternSize.setter
    def PatternSize(self, patternSize):
        self.__patternSize = patternSize

    @property
    def Pattern(self):
        return self.__pattern

    @Pattern.setter
    def Pattern(self, pattern):
        self.__pattern = pattern

    @property
    def IsOneCut(self):
        return self.__isOneCut

    @IsOneCut.setter
    def IsOneCut(self, isOneCut):
        self.__isOneCut = isOneCut

    @property
    def AzimuthScanAngles(self):
        return self.__azimuthScanAngles

    @property
    def ElevationScanAngles(self):
        return self.__elevationScanAngles

    @property
    def NumSignals(self):
        return self.__numSignals

    @property
    def SteeringVector(self):
        return self.__steeringVector

    @SteeringVector.setter
    def SteeringVector(self, steeringVector):
        self.__steeringVector = steeringVector

    def step(self, X):
        # self.cCovEstimator = phased.internal.SpatialCovEstimator(NumSubarrays = 1, # No subarray smoothing for 2D.
        #                                                         ForwardBackwardAveraging = self.ForwardBackwardAveraging);
        #
        # self.cSteeringVector = phased.SteeringVector(SensorArray = self.SensorArray,
        #                                             PropagationSpeed = self.PropagationSpeed,
        #                                             NumPhaseShifterBits = self.pNumPhaseShifterBits);

        az = self.AzimuthScanAngles
        el = self.ElevationScanAngles

        len_az = np.size(az)
        len_el = np.size(el)

        self.IsOneCut = (len_el == 1) or (len_az == 1)

        NumEl = np.size(np.array(el))
        NumAz = np.size(az)

        self.PatternSize = [NumEl, NumAz]
        [ScanAz, ScanEl] = np.meshgrid(az, el)

        self.__scanAngles = [ScanAz, ScanEl]

        if NumEl * NumAz < 400:
            self.__numIter = 1
            self.__scanAngleBlockSize = NumEl * NumAz
            self.__oneIterFlag = True
        else:
            self.__numIter = min(NumEl, NumAz)
            self.__scanAngleBlockSize = max(NumEl, NumAz)
            self.__oneIterFlag = False

        self.__scanAngleBlockIndex = np.arange(1, self.__scanAngleBlockSize + 1)

        self.Pattern = np.zeros(np.prod(self.PatternSize))

        # if self.__oneIterFlag:
        #    self.__steeringVectors = super(MVDREstimator2D, self).SteeringVector.step(self.OperatingFrequency,
        #                                                                              self.__scanAngles);

        return self.stepImpl(X)

    def stepImpl(self, X):
        # estimate the covariance matrix
        # Cx = self.CovEstimator.step(X)

        # generate spatial spectrum
        # self.privDOASpectrum(Cx)

        scanpattern = np.reshape(np.sqrt(np.abs(self.__pattern)), self.__patternSize)
        azang = self.AzimuthScanAngles
        elang = self.ElevationScanAngles

        if X is not None:
            numSignals = self.NumSignals

            # TODO: etc...

        return scanpattern

class MVDREstimator2D(AbstractSpectralDOA):
    def __init__(self, sensorArray=URA(), operatingFrequency=3e8, dOAOutputPort=False, numSignals=1,
                 azimuthScanAngles=np.arange(-90, 90), elevationScanAngles=0):
        super(MVDREstimator2D, self).__init__(numSignals=numSignals,
                                              azimuthScanAngles=azimuthScanAngles,
                                              elevationScanAngles=elevationScanAngles)

        self.__sensorArray = sensorArray
        self.__operatingFrequency = operatingFrequency
        self.__dOAOutputPort = dOAOutputPort

        self.__elevationScanAngles = elevationScanAngles

    @property
    def SensorArray(self):
        return self.__sensorArray

    @property
    def OperatingFrequency(self):
        return self.__operatingFrequency

    @property
    def DOAOutputPort(self):
        return self.__dOAOutputPort

    def step(self, X):
        return super(MVDREstimator2D, self).step(X)