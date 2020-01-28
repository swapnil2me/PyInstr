import matplotlib.pyplot as plt
import instruments as ins
import experiments as expr

vsAC = ins.Anapico('169.254.7.87')
vgAC = ins.Anapico('169.254.7.42')
liA = ins.SRS830(8,300)

vsAC.rampV(300)
vgAC.rampV(300)

dataLocation = 'C:\\Users\\nemslab4\\Documents\\'
vgInstr = vgAC
vgInstr.vgDC = 0
vgInstr.vgAC = 300
vsInstr = vsAC
vsInstr.vsAC = 300
liaInstr = liA
sf = 50
ef = 55
df = 0.5
mx = 1987

experiment = expr.MixdownFreqSweep(dataLocation, vgInstr, vsInstr, liaInstr,
             sf, ef, df, mx, True)

experiment.runSweep()

vgInstr.rampV(0.001)
vsInstr.rampV(0.001)
vgInstr.close()
vsInstr.close()
liaInstr.close()
