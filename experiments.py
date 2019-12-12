import numpy as np
import os

class MixdownFreqSweep():

    def __init__(self, dataLocation, vgInstr, vsInstr, liaInstr, sf, ef, df, mx, bkwSweep = False):

        self.dataLocation = dataLocation
        self.vgInstr = vgInstr
        self.vsInstr = vsInstr
        self.liaInstr = liaInstr
        self.sf = sf
        self.ef = ef
        self.df = df
        self.mx = mx
        self.bkwSweep = bkwSweep


    def run(self):

        dataFile_name = ['{}V_VgDC_{}mV_VgAC_{}mV_VsAC_{}MHz_{}MHz_FWD.csv'.format(
                        vgInstr.vgDC, vgInstr.vgAC, vsInstr.vsAC, sf, ef),
                        '{}V_VgDC_{}mV_VgAC_{}mV_VsAC_{}MHz_{}MHz_BKW.csv'.format(
                        vgInstr.vgDC, vgInstr.vgAC, vsInstr.vsAC, ef, sf)]

        if not os.path.exists(self.dataLocation):
            os.makedirs(self.dataLocation)

        fwdData=os.path.join(self.dataLocation,dataFile_name[0])
        bkwData=os.path.join(self.dataLocation,dataFile_name[1])

        outF = open(fwdData,"w")
        outF.write("f,A,P\n")
        for i in np.arange(self.sf, self.ef, self.df):
            vgInstr.setFreq(i)
            vsInstr.setFreq(i - self.mx * 1e-6)
            A,P = liA.readLIA()
            outF.write(("{0:5.5f},{1:8.8f},{2:8.8f}\n").format(i,A,P))
        outF.close()

        if self.bkwSweep:
            outB = open(bkwData,"w")
            outB.write("f,A,P\n")
            for i in np.arange(self.ef, self.sf, - self.df):
                vgInstr.setFreq(i)
                vsInstr.setFreq(i - self.mx * 1e-6)
                A,P = liA.readLIA()
                outB.write(("{0:5.5f},{1:8.8f},{2:8.8f}\n").format(i,A,P))
            outB.close()

class
