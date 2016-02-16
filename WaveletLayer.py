from pybrain.structure.modules.neuronlayer import NeuronLayer


class WaveletLayer(NeuronLayer):
    def _forwardImplementation(self, inbuf, outbuf):
        outbuf[:] = inbuf

    def _backwardImplementation(self, outerr, inerr, outbuf, inbuf):
        inerr[:] = outerr
