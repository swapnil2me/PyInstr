import sys
import os
import time
sys.path.append(os.path.join(os.getcwd(),'lib'))

import instruments as inst

liA = inst.SRS830(8,300)
liA.auxOutPort = 1
liA.rampV(10,20)
time.sleep(2)
liA.rampDown()
