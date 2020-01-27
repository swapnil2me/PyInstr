import matplotlib.pyplot as plt
import instruments as ins

vsAC = ins.Anapico('169.254.7.87')
vgAC = ins.Anapico('169.254.7.42')
liA = ins.SRS830(8,300)

vsAC.rampV(300)
vgAC.rampV(300)

vgAC.setFreq(50)
vsAC.setFreq(50-1987e-6)


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

#liA.sensitivity = 20
#liA.matchSensitivity()

for i in range(20):
    A,P = liA.readLIA()
    ax1.plot(i, A, 'ro')
    print(A,P)
    #plt.plot(i, P, 'ko')
    #plt.pause(0.000000001)


vsAC.rampV(0.001)
vgAC.rampV(0.001)

vsAC.close()
vgAC.close()
liA.close()
plt.show()
