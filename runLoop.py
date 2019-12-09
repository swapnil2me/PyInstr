import instruments as ins

vsAC = ins.Anapico('169.254.7.87')
vgAC = ins.Anapico('169.254.7.42')
liA = ins.SRS830(8,300)

vsAC.rampV(500)
vgAC.rampV(500)

vgAC.setFreq(50)
vsAC.setFreq(50-1987e-6)

liA.sensitivity = 20
liA.matchSensitivity()

print(liA.readLIA())

vsAC.rampV(0.001)
vgAC.rampV(0.001)

vsAC.close()
vgAC.close()
liA.close()

