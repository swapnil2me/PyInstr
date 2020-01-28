import numpy as np
import os
from math import isclose


class MixdownFreqSweep():

    def generateName(self):
        fileName = ''
        for i in range(len(self.instrList)):
            fileName += str(round(self.instrList[-1-i].askVolt())) + ''
            fileName += str(self.instrList[-1-i].unit) + '_'
            fileName += str(self.instrList[-1-i].name) + '_'
        fileName += str(self.sf) + 'MHz_' + str(self.ef) + 'MHz_'
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
        self.liaInstr = liaInstr
        self.instrList[0].freqOffSet = mx
        self.sf = instrList[0].freqSweepRange[0]
        self.ef = instrList[0].freqSweepRange[-1]
        self.df = instrList[0].freqSweepRange[1]
        self.mx = mx
        self.bkwSweep = bkwSweep


    def sweepSummary(self):
        print('ID     | Name | Unit | Voltage Range  | Freq Range  | Freq Offset')
        for i in range(len(self.instrList)):
            print('Instr ' + str(i) + ': '+str(self.instrList[i].name)
                                    + ': '+str(self.instrList[i].unit)
                                    + ': '+str(self.instrList[i].voltageSweepRange)
                                    + ': '+str(self.instrList[i].freqSweepRange)
                                    + ': '+str(self.instrList[i].freqOffSet))


    def setExperiment(self):
        voltage_ranges = [i.voltageSweepRange for i in self.instrList]
        assert None not in voltage_ranges, "Please set voltage_ranges for all instrs"
        if self.instrList[0].askVolt() != self.instrList[0].voltageSweepRange[0]:
            self.instrList[0].rampV(self.instrList[0].voltageSweepRange[0])
        if self.instrList[1].askVolt() != self.instrList[1].voltageSweepRange[0]:
            self.instrList[1].rampV(self.instrList[1].voltageSweepRange[0])


    def generateSweepSpace(self):
        voltage_ranges = [i.voltageSweepRange for i in self.instrList]
        assert None not in voltage_ranges, "Please set voltage_ranges for all instrs"
        voltages = [np.arange(i[0],i[-1]+i[1],i[1]) for i in voltage_ranges]
        grids = np.meshgrid(*voltages)
        gridsFlatten = [gr.flatten() for gr in grids]
        sweepSpace = list(zip(*gridsFlatten))
        return sweepSpace


    def runVtgSweep(self):
        sweepSpace = self.generateSweepSpace()
        for i in sweepSpace:
            for j in range(len(self.instrList)):
                self.instrList[j].rampV(i[j])
            self.runSweep()


#class SweepLoop():
