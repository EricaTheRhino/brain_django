#!/bin/python
import PITLC5940.LED as LED
# as LED

#Brightness=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#ledmode=[hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,off]
#ledsettings=[(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3),(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3),(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3),(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3),(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3),(0)]


count=3

LED.Brightness=[0]*16*count
print LED.Brightness
tempmode=[LED.hueblend]*15
tempmode.append(LED.off)
LED.ledmode=tempmode*count
print LED.ledmode
#ledsettings=[(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3)]*5
#ledsettings.append(0)
#ledsettings=ledsettings*count

LED.ledsettings=[]
# build custom blend array

ledoffset=[0,0,1000,1000,1000,2000,2000,2000,3000,3000,3000,2000,3000,3000,3000]

for led in range(15):
	print led
	LED.ledsettings.append((10000,ledoffset[led],3000,1))
	LED.ledsettings.append((10000,ledoffset[led],3000,2))
	LED.ledsettings.append((10000,ledoffset[led],3000,3))
	if led == 4:
		LED.ledsettings.append(0)
	if led == 9:
		LED.ledsettings.append(0)
	if led == 14:
		LED.ledsettings.append(0)

print LED.ledsettings


LED.startledcontroler()

import time
time.sleep(1000)
