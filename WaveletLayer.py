from pybrain.structure.modules.neuronlayer import NeuronLayer
from pybrain.structure.parametercontainer import ParameterContainer
import scipy.signal as spsig


class WaveletLayer(NeuronLayer, ParameterContainer):
    def __init__(self):
        ParameterContainer.__init__(self, 1)

    def _forwardImplementation(self, inbuf, outbuf):
        outbuf[:] = spsig.ricker(inbuf, self.params)

    def _backwardImplementation(self, outerr, inerr, outbuf, inbuf):
        # rickerderiv =
        inerr[:] = outbuf - outerr
