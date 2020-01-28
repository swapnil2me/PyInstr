import numpy as np
import os
from math import isclose

class MixdownFreqSweep():

    def generateName(self):
        fileName = ''
        for i in range(len(self.instrList)):
            fileName += self.instrList[i].askVolt + ''
            fileName += self.instrList[i].unit + '_'
            fileName += self.instrList[i].name + '_'
        fileName += self.sf + 'MHz_' + self.ef + 'MHz_'
        return fileName+'FWD.csv', fileName+'BKW.csv'

    def runSweep(self):

        try:
            dataFile_name = self.generateName()

            if not os.path.exists(self.dataLocation):
                os.makedirs(self.dataLocation)

            fwdData=os.path.join(self.dataLocation,dataFile_name[0])
            bkwData=os.path.join(self.dataLocation,dataFile_name[1])

            outF = open(fwdData,"w")
            outF.write("f,A,P\n")
            for i in np.arange(self.sf, self.ef + 1, self.df):
                self.instrList[1].setFreq(i)
                self.instrList[0].setFreq(i)
                A,P = self.liaInstr.readLIA()
                outF.write(("{0:5.5f},{1:8.8f},{2:8.8f}\n").format(i,A,P))
            outF.close()

            if self.bkwSweep:
                outB = open(bkwData,"w")
                outB.write("f,A,P\n")
                for i in np.arange(self.ef, self.sf - 1, - self.df):
                    self.instrList[1].setFreq(i)
                    self.instrList[0].setFreq(i)
                    A,P = self.liaInstr.readLIA()
                    outB.write(("{0:5.5f},{1:8.8f},{2:8.8f}\n").format(i,A,P))
                outB.close()

        except AttributeError as arrtErr:
            print(arrtErr)
            print('Error Occured')
            for i in range(len(self.instrList)):
                self.instrList[i].rampV(0.001)
                self.instrList[i].close()
            self.liaInstr.close()
            print('instruments closed')


class VoltageSweep(MixdownFreqSweep):

    def __init__(self, dataLocation, instrList, liaInstr, mx, bkwSweep = False):
        self.dataLocation = dataLocation
        self.instrList = instrList
        self.instrList[0].freqOffSet = mx
        self.liaInstr = liaInstr
        self.sf = instr1.freqSweepRange[0]
        self.ef = instr1.freqSweepRange[-1]
        self.df = instr1.freqSweepRange[1]
        self.mx = mx
        self.bkwSweep = bkwSweep


    def setExperiment(self):
        if self.instrList[0].askVolt() != self.instrList[0].voltageSweepRange[0]:
            self.rampV(self.instrList[0].voltageSweepRange[0])
        if self.instrList[1].askVolt() != self.instrList[1].voltageSweepRange[0]:
            self.rampV(self.instrList[1].voltageSweepRange[0])


    def runVtgSweep(self):
        while (self.instrList[1].askVolt() <= self.instrList[1].voltageSweepRange[-1] and
            not isclose(self.instrList[1].askVolt(), self.instrList[1].voltageSweepRange[-1], rel_tol = 5)):
            self.instrList[1].incrementSweepVolt()
            self.rampV(self.instrList[0].voltageSweepRange[0])
            while (self.instrList[0].askVolt() <= self.instrList[0].voltageSweepRange[-1] and
                not isclose(self.instrList[0].askVolt(), self.instrList[0].voltageSweepRange[-1], rel_tol = 5)):
                self.instrList[0].incrementSweepVolt()
                self.runSweep()


#class SweepLoop():
