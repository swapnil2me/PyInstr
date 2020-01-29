import sys
import os
sys.path.append(os.path.join(os.getcwd(),'lib'))

import instruments as inst
import experiments as expr

paramDict = {'vsAC':{'instClass':'Anapico',
                     'address': '169.254.7.87',
                     'volt':300,
                     'mixDownFreq':1987,
                     'freqRange':[50.0,0.5,51]},
             'vgAC':{'instClass':'Anapico',
                     'address': '169.254.7.42',
                     'volt':300},
             'vgDC':{'instClass':'SRS830',
                     'address':'8',
                     'auxOutPort':1,
                     'sweepVolt':[0.0,2.0,2.0]},
             'LIA':{'instClass':'SRS830',
                     'address':'8',
                     'timeConstant':300},
                     'dataDir':'C:\\Users\\nemslab4\\Documents\\'
            }

try:
    dispersion = expr.DispersionSweep(paramDict)
    dispersion.runDispersion()
except:
    dispersion.closeAll()


dispersion.closeAll()
print('')
print('Experiment Closed')
print('-----------------')
