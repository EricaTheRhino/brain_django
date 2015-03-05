#!/bin/python
# controls LEDs on the Rhino
# several "modes" are defined here eg blends
import PITLC5940.LED as LED

HORN=3
BODY=2

controller = None

#############################
# helper functions
#############################

def floatCol(r, g, b, scale_factor=4095):
    """
    Takes floats between 0 and 1 as colours for LEDs and scales them to the 
    native values of 0 to 4095.
    """
    return (r*scale_factor, g*scale_factor, b*scale_factor)

def settingsForRGBLED(settings, brightness_index, colour):
    """
    Takes a single settings tuple with a brightness component at 
    brightess_index, along with the colour as a 3-tuple of floats, and returns 
    a list of 3 tuples, one for each coloured LED.
    """
    settings = [list(settings)] * 3

    for i in range(3):
        settings[i][brightness_index] = int(settings[i][brightness_index] * colour[i])
        settings[i] = tuple(settings[i])

    return settings

def quickPad(ledmodes, ledsettings):
    ledmodes = (ledmodes[0:15]  + [LED.off] +
                ledmodes[15:30] + [LED.off] +
                ledmodes[30:45] + [LED.off])
    ledsettings = (ledsettings[0:15]  + [(0,)] +
                   ledsettings[15:30] + [(0,)] +
                   ledsettings[30:45] + [(0,)])

    return (ledmodes, ledsettings)

def padListByMod(list, mod, pad):
    new_list = [list[0]]

    i = 1
    padded = False
    while i < len(list):
        if padded or i % mod:
            new_list.append(list[i])
            i = i + 1
            padded = False
        else:
            new_list.append(pad)
            padded = True

    return new_list

#############################
# led cordinates
#############################

# cordinates and angles of horn leds (one per rgbled)
ledcordinates=[(0,0),(0,180),
		(1,60),(1,180),(1,300),
		(2,60),(2,180),(2,300),
		(3,60),(3,180),(3,300),
		(2,0),
		(3,0),(3,120),(3,240)]

ledbackground=["yellow","yellow",
		"black","black","black",
		"yellow","yellow","yellow",
		"black","black","black",
		"yellow",
		"black","black","black"]


ledbodybackground=["red","red","red","red","red",
		"yellow","yellow","yellow",
		"blue","blue","blue","blue",
		"green","green",
		"white","white"]


BODY_LENGTH = 2100

# FIX DA NUMBERS!
LED_X_LEFT  = [0, 285, 370, 405, 420, 530, 565, 605, 715, 805, 810, 820, 1375, 1530, 1535, 1825]
#LED_X_RIGHT = [0, 200, 300, 350, 355, 430, 485, 570, 680, 760, 800, 1425, 1530, 1545, 1775, 2000]
LED_X_RIGHT = [0, 270, 450, 575, 615, 620, 690, 725, 805, 890, 970, 1000, 1635, 1740, 1750, 1960]

LED_BY_POS_LEFT  = [0, 1, 8, 12, 9, 10, 14, 5, 2, 13, 3, 6, 7, 15, 11, 4]
LED_BY_POS_RIGHT = [0, 1, 8, 9, 12, 10, 14, 5, 6, 2, 13, 3, 7, 15, 11, 4]


#############################
# initilise leds
#############################

def initiliserhinoleds(ledtype):
	global controller
	if ledtype == HORN:
		count=3
	elif ledtype == BODY:
		count=2
	else:
		print "unrecognised ledchain length"

	controller = LED.LEDController(count)
	controller.startledcontroler()
	return controller

#############################
# generic array build scripts
#############################

def testsequence(count=3, speed=1000):
	ledmode=[LED.blink]*16*count
	totaltime=count*16*speed
	ledsettings=[]
	
	for led in range(count*16):
		ledsettings.append((totaltime,speed,led*speed,3000))

	print count
	print ledsettings
	return(ledmode,ledsettings)

def breathe(count=3):
	ledmode=[LED.breathe]*16*count
	ledsettings=[(10000,3000)]*16*count

	return(ledmode,ledsettings)

#############################
# body array build scripts
#############################
def sweep(load_period=2500,
          on_period=2500,
          unload_period=2500,
          off_period=2500,
          brightness=3000):
    count = 2

    ledmodes = [LED.blink] * 16 * count
    ledsettings = [None] * 16 * count

    ledsettings_left = []
    for i in range(16):
        mult = LED_X_LEFT[i] / float(BODY_LENGTH)

        period = load_period + unload_period + on_period + off_period
        ontime = on_period + load_period*(1-mult) + unload_period*mult
        offset = load_period * mult

        ledsettings_left.append((period, ontime, offset, brightness))
    for i in range(16):
        ledsettings[LED_BY_POS_LEFT[i]] = ledsettings_left[i]


    ledsettings_right = []
    for i in range(16):
        mult = LED_X_RIGHT[i] / float(BODY_LENGTH)

        period = ((load_period + unload_period) * mult) + on_period + off_period
        ontime = on_period
        offset = load_period * mult

        ledsettings_right.append((period, ontime, offset, brightness))
    for i in range(16):
        ledsettings[LED_BY_POS_RIGHT[i] + 16] = ledsettings_right[i]

    return (ledmodes, ledsettings)

#############################
# horn array build scripts
#############################
def angularsweep(period=1000, colour=(1.0, 0.0, 0.0), brightness=1000):
    # 3 controllers
    count = 3

    ledmodes = (([LED.constant] * count) + ([LED.blink] * 10 * count) +
                ([LED.constant] * count) + ([LED.blink] *  3 * count))

    settings = [ (period, period/3,          0, brightness),
                 (period, period/3,   period/3, brightness),
                 (period, period/3, 2*period/3, brightness) ]

    ledsettings = []

    ledsettings = ledsettings + settingsForRGBLED([brightness], 0, colour)
    ledsettings = ledsettings + settingsForRGBLED(settings[1], 3, colour)

    for i in range(9):
        ledsettings = ledsettings + settingsForRGBLED(settings[i % 3], 3, colour)

    ledsettings = ledsettings + settingsForRGBLED([brightness], 0, colour)

    for i in range(3):
        ledsettings = ledsettings + settingsForRGBLED(settings[i], 3, colour)

    return quickPad(ledmodes, ledsettings)

def blends(rate=10000,xrate=0,yrate=0,brightness=1000):
	count=3
	tempmode=[LED.hueblend]*15
	tempmode.append(LED.off)
	ledmode=tempmode*count

	ledsettings=[]

	#buildcustomblendarray
	for led in range(15):
                print led
		offset=(ledcordinates[led][0]*rate*xrate)+(ledcordinates[led][1]*(rate/360)*yrate)
                ledsettings.append((rate,offset,brightness,1))
                ledsettings.append((rate,offset,brightness,2))
                ledsettings.append((rate,offset,brightness,3))

                if led == 4:
                        ledsettings.append((0,))
                if led == 9:
                        ledsettings.append((0,))
                if led == 14:
                        ledsettings.append((0,))

        return(ledmode,ledsettings)


def verticialblends(xrate=0.1,**kwargs):
	return(blends(xrate=xrate,**kwargs))

def horizontalblends(yrate=1,**kwargs):
	return(blends(yrate=yrate,**kwargs))

def neutral(brightness=255):
	ledmode=[]
	ledsettings=[]
	yellow=[(int(float(227)/255*brightness),0),
	(int(float(18)/255*brightness),0),
	(int(float(40)/255*brightness),0)]

	for led in range(15):
		if ledbackground[led]=="yellow":
			ledmode.extend([LED.constant]*3)
			ledsettings.extend(yellow)
		else:
			ledmode.extend([LED.off]*3)
			ledsettings.extend([(0,0),(0,0),(0,0)])
		if led == 4:
			ledmode.append(LED.off)
			ledsettings.append((0,))
                if led == 9:
			ledmode.append(LED.off)
			ledsettings.append((0,))
                if led == 14:
			ledmode.append(LED.off)
			ledsettings.append((0,))


	return(ledmode,ledsettings)



def modepercolour(
redmode=LED.off,redsettings=(0,),
bluemode=LED.off,bluesettings=(0,),
greenmode=LED.off,greensettings=(0,),
):
	ledmode=[]
	ledsettings=[]
	
	for led in range(15):
                ledmode.append(redmode)
		ledsettings.append(redsettings)
		ledmode.append(bluemode)
		ledsettings.append(bluesettings)
		ledmode.append(greenmode)
		ledsettings.append(greensettings)
                if led == 4:
			ledmode.append(LED.off)
			ledsettings.append((0,))
                if led == 9:
			ledmode.append(LED.off)
			ledsettings.append((0,))
                if led == 14:
			ledmode.append(LED.off)
			ledsettings.append((0,))


	return(ledmode,ledsettings)


############################
# brain functions for horn
############################

def solid(controller,R=0,G=0,B=0,blend=False,blendtime=10000):
	data=modepercolour(redmode=LED.constant,redsettings=(R,0),bluemode=LED.constant,bluesettings=(B,0),greenmode=LED.constant,greensettings=(G,0))
	if blend:
		controller.setmodemixer(data,LED.modeblend,(LED.millis(),LED.millis()+blendtime))
	else:
		controller.setconfig(*data)
	
def hues(controller,rate=10000,blend=False,blendtime=10000):
	speed=int((((1)-(rate*rate))*10000))+1000
	data=blends(rate=speed)
	print rate
	print speed
	if blend:
		controller.setmodemixer(data,LED.modeblend,(LED.millis(),LED.millis()+blendtime))
	else:
		controller.setconfig(*data)

############################
# brain functions for body
############################



############################
# generic brain functions 
############################

def test(controler,ledtype,speed=1000):
	controler.setconfig(*testsequence(count=ledtype,speed=speed))

def breathing(controler,ledtype,blend=False,blendtime=10000):
	data=breathe(count=ledtype)
	if blend:
		controller.setmodemixer(data,LED.modeblend,(LED.millis(),LED.millis()+blendtime))
	else:
		controller.setconfig(*data)


if __name__ == "__main__":
	import time
	initiliserhinoleds(BODY)
	#controller.setconfig(*verticialblends())
	controller.setconfig(*breathe(count=2))
	#controller.setconfig(*angularsweep())
	#controller.setconfig(*sweep())
        time.sleep(30)
	controller.setconfig(*testsequence(count=2))
	print "pulse"
	#controller.setmodemixer(modepercolour(redmode=LED.constant,redsettings=(3000,0)),LED.modeblend,(LED.millis(),LED.millis()+5000))
	#controller.setmodemixer(modepercolour(redmode=LED.constant,redsettings=(3000,0)),LED.pulse,(LED.millis()+5000,0))
	#print LED.ledmode
	time.sleep(10000)
