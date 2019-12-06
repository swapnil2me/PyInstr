import vxi11
import time

class Instrument:

    def __init__(self,address):

        self.address = address
        self._instR = vxi11.Instrument(address,'inst0')

    def rampV(self,askStr,writeStr)


class Sma100A(Instrument):

    def __init__(self,address):

        #Instrument.__init__(self,address)
        super(Sma100A, self).__init__(address)
        self._instR.write('UNIT:POW V')


    def rampV(self, setV, rampN = 200,ps = 0.05):

        if setV == 0:
            setV = 1
        outV     = float(self._instR.ask(':sour:pow:lev?')) * 1000 #in miliVolts
        rampStep = (outV - setV)/rampN
        if rampStep == 0:
            print('Already at set voltage')
        for i in range(rampStep):
            increment = (outV - i*rampStep) / 1000
            self._instR.write(":pow {0:.8f}".format(increment))


    def setFreq(self, freq, phs = 0):

        self._instR.write('FREQ {0:.8f} MHz; PHAS {0:.8f};'.format(freq, phs))

class  Anapico(Instrument):


    def __init__(self, address):

        super(Anapico, self).__init__(address)
        self._instR.write('UNIT:POW V')
        if int(self._instR.ask(':OUTP:STAT?')):
            self._instR.write(':sour:pow:lev:imm:ampl 0.001')
            self._instR.write(':OUTP:STAT ON')


    def rampV(self, setV, rampN = 200,ps = 0.05):

        if setV == 0:
            setV = 1
        outV     = float(self._instR.ask(':sour:pow:lev?')) * 1000 #in miliVolts
        rampStep = (outV - setV)/rampN
        if rampStep == 0:
            print('Already at set voltage')
        for i in range(rampStep):
            increment = (outV - i*rampStep) / 1000
            self._instR.write(":sour:pow:lev:imm:ampl {0:.8f}".format(increment))


    def setFreq(self, freq, phs = 0):

        self._instR.write('FREQ {0:.8f}'.format(freq))
