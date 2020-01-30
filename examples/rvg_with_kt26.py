import sys
import os
sys.path.append(os.path.join(os.getcwd(),'lib'))

import instruments as inst
import experiments as expr

paramDict = {'address':'169.254.0.1',
             'source_channel':'a',
             'sourceVolt':0.1,
             'gate_channel':'b',
             'gateSweep':[1,1,10],
             'dataLocation':'C:\\Users\\nemslab4\\Documents\\'}

rvg = expr.Rvg(paramDict)
rvg.setExperiment()
V,R = rvg.startExperiment()
print(V,R)
print(rvg.dataLocation)

rvg.closeExperiment()
