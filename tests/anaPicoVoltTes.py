import sys
import os
sys.path.append(os.path.join(os.getcwd(),'lib'))
import matplotlib.pyplot as plt
import instruments as ins
import experiments as expr


try:
    vsAC = ins.Anapico('169.254.7.87')
    vgAC = ins.Anapico('169.254.7.42')
    vsAC.rampV(300,10)
    vgAC.rampV(300,10)
except:
    vsAC.rampDown(10)
    vgAC.rampDown(10)
    vsAC.close()
    vgAC.close()
vsAC.rampDown(10)
vgAC.rampDown(10)
vsAC.close()
vgAC.close()
