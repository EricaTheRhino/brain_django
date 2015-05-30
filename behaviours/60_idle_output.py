# coding: utf-8


def lookrl():
	global trigger
	trigger('righteye.servo.direction', {'dir':1}, True)
	trigger('lefteye.servo.direction', {'dir':1})
	trigger('righteye.servo.direction', {'dir':0}, True)
	trigger('lefteye.servo.direction', {'dir':0})
	trigger('righteye.servo.direction', {'dir':0.5}, True)
	trigger('lefteye.servo.direction', {'dir':0.5})
	trigger('righteye.servo.direction', {'dir':1}, True)
	trigger('lefteye.servo.direction', {'dir':1})
	trigger('righteye.servo.direction', {'dir':0.5}, True)
	trigger('lefteye.servo.direction', {'dir':0.5})

def looklr():
	global trigger
	trigger('righteye.servo.direction', {'dir':0}, True)
	trigger('lefteye.servo.direction', {'dir':0})
	trigger('righteye.servo.direction', {'dir':1}, True)
	trigger('lefteye.servo.direction', {'dir':1})
	trigger('righteye.servo.direction', {'dir':0.5}, True)
	trigger('lefteye.servo.direction', {'dir':0.5})
	trigger('righteye.servo.direction', {'dir':1}, True)
	trigger('lefteye.servo.direction', {'dir':1})
	trigger('righteye.servo.direction', {'dir':0.5}, True)
	trigger('lefteye.servo.direction', {'dir':0.5})

def blink():
	global trigger
	trigger('righteye.lights.blink', {'time':300}, True)
	trigger('lefteye.lights.blink', {'time':300}, True)

def earslr(speed=0):
	global trigger
	trigger('leftear.servo.waggle', {'angle':40, 'speed':speed}, True)
	trigger('rightear.servo.waggle', {'angle':40, 'speed':speed}, True)

def earsrl(speed=0):
	global trigger
	trigger('leftear.servo.waggle', {'angle':-40, 'speed':speed}, True)
	trigger('rightear.servo.waggle', {'angle':-40, 'speed':speed}, True)

def earsout(speed=0):
	global trigger
	trigger('leftear.servo.waggle', {'angle':-40, 'speed':speed}, True)
	trigger('rightear.servo.waggle', {'angle':40, 'speed':speed}, True)

def earsin(speed=0):
	global trigger
	trigger('leftear.servo.waggle', {'angle':40, 'speed':speed}, True)
	trigger('rightear.servo.waggle', {'angle':-40, 'speed':speed}, True)

def random_ears(speed=0):
	global earslr
	global earsrl
	global earsout
	global earsin
	global trigger
	dir = random.choice([0, 1, 2, 3])
	if dir == 0:
		earslr(speed)
	elif dir == 1:
		earsrl(speed)
	elif dir == 2:
		earsout(speed)
	elif dir == 3:
		earsin(speed)

def random_eyes(speed=0):
	global lookrl
	global looklr
	global blink
	global trigger
	dir = random.choice([0, 1, 2])
	if dir == 0:
		lookrl()
	elif dir == 1:
		looklr()
	elif dir == 2:
		blink()

latest = get_latest()
if latest['event'] == 'brain.idle_skip':
	energy = get_stat('energy')
	mood = get_stat('mood')
	if energy > 1:
		recent = get_in_last(300)
		for ev in recent:
			if not ev['event'] == 'brain.idle':
				nothing_happened = False
		nothing_happened = True
		if nothing_happened:
			rate = energy/Decimal(6.0)
			# Try to get attention.
			opt = random.choice([0, 1, 2, 2, 2, 3, 3, 3])

			if opt == 0:
				if mood < 4:
					if energy < 4:
						trigger('horn.colours', {'theme':'red', 'time':500}, True)
						random_ears(1)
					else:
						if random.choice([0,1,2,3,4,5]) == 3:
							play_sound(random.choice(IDLE_SOUNDS))
						else:
							random_eyes(1)
			if opt == 1:
				random_eyes(rate)
			if opt == 2 or opt == 3:
				random_ears(rate)
	elif energy > 0:
		opt = random.choice([0,1,2,3,4,5])
		if opt == 0:
			play_sound(IDLE_TIRED_SOUND)
		elif opt == 1:
			random_ears(1)
		else:
			random_eyes(1)
	else:
		if random.choice([0,1,2,3,4,5]) == 1:
			play_sound(IDLE_ASLEEP_SOUND)
		else:
			random_ears(1)
