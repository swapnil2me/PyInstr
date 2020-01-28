import sys
import os
sys.path.append(os.path.join(os.getcwd(),'lib'))
import matplotlib.pyplot as plt
import instruments as ins
import experiments as expr


try:
    vsAC = ins.Anapico('169.254.7.87')
    vgAC = ins.Anapico('169.254.7.42')
    liA = ins.SRS830(8,300)

    vsAC.name = 'VsAC'
    vgAC.name = 'VgAC'
    vsAC.unit = 'mV'
    vgAC.unit = 'mV'

    vsAC.voltageSweepRange = [300.,1.,300.]
    vgAC.voltageSweepRange = [300.,5.,305.]
    vsAC.freqSweepRange = [50,0.5,52]

    dataLocation = 'C:\\Users\\nemslab4\\Documents\\'
    mx = 1987
    print('Initiated Instr')
    sweep = expr.VoltageSweep(dataLocation, [vsAC,vgAC], liA, mx)
    print('Printing Sweep Summary')
    sweep.sweepSummary()
    sweep.setExperiment()
    print('Running Sweep')
    sweep.runVtgSweep()


except:
    print('Error Occured, closing instruments')
    vsAC.rampDown()
    vgAC.rampDown()
    vsAC.close()
    vsAC.close()
    vsAC.close()

vsAC.rampDown()
vgAC.rampDown()
vsAC.close()
vsAC.close()
vsAC.close()
