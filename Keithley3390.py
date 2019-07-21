import vxi11
instr =  vxi11.Instrument("169.254.2.20",'inst0')
#instr =  vxi11.Instrument("169.254.2.20",'gpib,17')
print(instr.ask("*IDN?"))
instr.write("OUTP ON")
print(instr.ask("VOLT?"))
print(instr.ask("FREQ?"))

instr.write("VOLT:UNIT VRMS")
instr.write("VOLT 0.004")
instr.write("FREQ 1e6")

print(instr.ask("VOLT?"))
print(instr.ask("FREQ?"))

instr.write("OUTP OFF")
instr.write("OUTP ON")

for i in range(10):
	instr.write(("VOLT {0:10.5f}").format(0.004+i/1000))
	print(instr.ask("VOLT?"))
instr.write("OUTP OFF")
