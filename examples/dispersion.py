import sys
import os
sys.path.append(os.path.join(os.getcwd(),'lib'))

import instruments as inst
import experiments as expr

paramDict = {'experintName':'Dispersion',
            'sweep':{'type':'VgDC',
                      'unit':'V'},
             'VsAC':{'instClass':'Anapico',
                     'address': '169.254.7.87',
                     'name':'VsAC',
                     'unit':'mV',
                     'volt':300,
                     'mixDownFreq':1987,
                     'freqRange':[50.0,0.1,52]},
             'VgAC':{'instClass':'Anapico',
                     'address': '169.254.7.42',
                     'name':'VgAC',
                     'unit':'mV',
                     'volt':300},
             'VgDC':{'instClass':'SRS830',
                     'address':'8',
                     'name':'VgDC',
                     'unit':'V',
                     'auxOutPort':1,
                     'sweepVolt':[0.0,0.5,2.0]},
             'LIA':{'instClass':'SRS830',
                     'address':'8',
                     'name':'LIA',
                     'unit':'NA',
                     'timeConstant':100},
            'backSweep':True,
            'dataDir':'C:/Users/nemslab4/Documents/'
            }
dispersion = expr.DispersionSweep(paramDict)
try:
    dispersion = expr.DispersionSweep(paramDict)
    dispersion.runDispersion()
except:
    print('error')
    dispersion.closeAll()


#dispersion.closeAll()
print('')
print('Experiment Closed')
print('-----------------')
dispersion.createImage()
#print(X)
#print(Y)
#print(Z)
