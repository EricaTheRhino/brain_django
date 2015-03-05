from TLC5940 import *
import math
import sys

sl = 0.1;
if len(sys.argv) == 2:
	sl = float(sys.argv[1])

resetTLC()
for j in range(0, 100, 1):
	for i in range(0, 3, 1):
		val = (([0]*i + [4000] + [0]*(3-i-1))*5 + [0])*3
		print val
		setTLCvalue(buildvalue(val, regPWM), regPWM)
		time.sleep(sl)

