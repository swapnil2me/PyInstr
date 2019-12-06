import vxi11
import pyvisa
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
        self._instR.write("UNIT:POW V\n")
        if not(int(self._instR.ask("OUTP:STAT?\n")):
            self._instR.write(':sour:pow:lev:imm:ampl 0.001\')
            self._instR.write(':OUTP:STAT ON\')


    def rampV(self, setV, rampN = 200,ps = 0.05):

        if setV == 0:
            setV = 1
        outV     = float(self._instR.ask(':sour:pow:lev?\n')) * 1000 #in miliVolts
        rampStep = (outV - setV)/rampN
        if rampStep == 0:
            print('Already at set voltage')
        for i in range(rampStep):
            increment = (outV - i*rampStep) / 1000
            self._instR.write(":sour:pow:lev:imm:ampl {0:.8f}\n".format(increment))


    def setFreq(self, freq, phs = 0):

        self._instR.write('FREQ {0:.8f}e6\n'.format(freq))
        self._instR.write('SOUR:PHAS {0:.8f}\n'.format(phs))

class SRS830():
    """docstring for SRS830."""

    def __init__(self, address):

        rm = pyvisa.ResourceManager()
        self.address = address
        self._instR = rm.open_resource('GPIB0::'+str(address)+'::INSTR')

    def checkStatus(self):
        ovldI = self._instR.query('lias?0\n')
        ovldTC = self._instR.query('lias?1\n')
        ovldOP = self._instR.query('lias?2\n')
        return ovldI, ovldOP, ovldTC

    def unlocked(self):
        return int(self._instR.query('lias?3\n')) == 1

    def readLIA(self, waitFor):
        status_=list(map(int,self.checkStatus))
        while not(all(status_)):
            print('Check Instrument for overload')
        while self.unlocked():
            self._instR.write('SENS' + str(int(self._instR.query('SENS ?')) + 1))
        return [A,P] = list(map(float,(inst.query('SNAP?3, 4').split(','))))
        
