import sys
import os
sys.path.append(os.path.join(os.getcwd(),'lib'))
import instruments as ins

liA = ins.SRS830(8,300)

for i in range(20):
    A,P = liA.readLIA()
    print(A,P)

liA.close()
