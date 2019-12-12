import vxi11
import pyvisa
import time

class Instrument:

    def __init__(self,address):

        self.address = address
        self._instR = vxi11.Instrument(address,'inst0')
        

    def rampV(self,askStr,writeStr):
        pass
    
    
    def close(self):
        self._instR.close()


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
        for i in range(rampN):
            increment = (outV - i*rampStep) / 1000 # in Volts
            self._instR.write(":pow {0:.8f}".format(increment))


    def setFreq(self, freq, phs = 0):

        self._instR.write('FREQ {0:.8f} MHz; PHAS {0:.8f};'.format(freq, phs))


class  Anapico(Instrument):

    def __init__(self, address):

        super(Anapico, self).__init__(address)
        self._instR.write("UNIT:POW V\n")
        if not int(self._instR.ask("OUTP:STAT?\n")):
            self._instR.write(':sour:pow:lev:imm:ampl 0.001\n')
            self._instR.write(':OUTP:STAT ON\n')


    def rampV(self, setV, rampN = 200,ps = 0.05):

        if setV == 0:
            setV = 1
        outV = float(self._instR.ask(':sour:pow:lev?\n')) * 1000 #in miliVolts
        rampStep = (outV - setV)/rampN
        if rampStep == 0:
            print('Already at set voltage')
        for i in range(rampN):
            increment = (outV - i*rampStep) / 1000 # in Volts
            self._instR.write(":sour:pow:lev:imm:ampl {0:.8f}\n".format(increment))


    def setFreq(self, freq, phs = 0):

        self._instR.write('FREQ {0:.8f}e6\n'.format(freq))
        self._instR.write('SOUR:PHAS {0:.8f}\n'.format(phs))


class SRS830(Instrument):
    """docstring for SRS830."""

    def __init__(self, address, waitFor):

        rm = pyvisa.ResourceManager()
        self.address = address
        self.waitFor = waitFor
        self._instR = rm.open_resource('GPIB0::'+str(address)+'::INSTR')

    
    def checkStatus(self):
    
        ovldI = self._instR.query('lias?0\n')
        ovldTC = self._instR.query('lias?1\n')
        return any(list(map(int,(ovldI, ovldTC))))

   
    def unlocked(self):
        
        return int(self._instR.query('lias?3\n')) == 1

    
    @property
    def sensitivity(self):
        self._sensitivity = int(self._instR.query('SENS ?'))
        return self._sensitivity
    
    
    @sensitivity.setter
    def sensitivity(self, numB):
        
        self._instR.write('SENS' + str(int(numB)))
        self._sensitivity = int(numB)
        print('LIA sensitivity changed to: {}'.format(numB))
        return self._sensitivity
    
    
    def outputOverload(self):
        
        return int(self._instR.query('lias?2\n')) == 1
    
    
    def matchSensitivity(self):
        
        self.sensitivity = self.sensitivity - 1
        while not self.outputOverload():
            self.sensitivity = self.sensitivity - 1
            
    
    def readLIA(self):
        
        while self.checkStatus():
            print('Check Instrument for overload')
            time.sleep(self.waitFor/1000)
        #print('Overload Resolved')
        while self.unlocked():
            print('Reference is unlocked')
            time.sleep(self.waitFor/1000)
        #print('Locked to the reference')
        while self.outputOverload():
            self.sensitivity = self.sensitivity + 1
            time.sleep(self.waitFor/1000)
        time.sleep(self.waitFor/1000)
        return list(map(float,(self._instR.query('SNAP?3, 4').split(','))))
        
