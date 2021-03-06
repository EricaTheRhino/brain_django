# coding: utf-8
import random
import time
latest = get_latest()

if latest['event'] == 'interaction.touchscreen.sound':
        play_sound(random.choice(TOUCHSCREEN_SOUNDS))

if latest['event'] == 'interaction.touchscreen.eyes':
	mqtt_pubevent(latest['event'], latest['params'], 'Look into my eyes!');
	trigger('righteye.servo.direction', {'dir':0.5}, True)
	trigger('lefteye.servo.direction', {'dir':1}, True)
	trigger('righteye.servo.direction', {'dir':1}, False)
	trigger('lefteye.servo.direction', {'dir':0}, True)
	trigger('righteye.servo.direction', {'dir':0}, False)
	trigger('lefteye.servo.direction', {'dir':1}, True)
	trigger('righteye.servo.direction', {'dir':1}, False)
	trigger('lefteye.servo.direction', {'dir':0}, True)
	trigger('righteye.servo.direction', {'dir':0}, False)
	trigger('lefteye.servo.direction', {'dir':0.5}, True)
	trigger('righteye.servo.direction', {'dir':0.5}, False)

if latest['event'] == 'interaction.touchscreen.ears':
	mqtt_pubevent(latest['event'], latest['params'], 'Watch my ears waggle!');
	#trigger('leftear.servo.home', {})
	#trigger('rightear.servo.home', {})
	trigger('leftear.servo.waggle', {'angle':90, 'speed':0.5}, True)
	trigger('rightear.servo.waggle', {'angle':-90, 'speed':0.5})

if latest['event'] == 'interaction.touchscreen.hornlights':
	mqtt_pubevent(latest['event'], latest['params'], 'Watch my horn change colour!');
	trigger('lights.colours', {'theme':'horn.random'}, False)

if latest['event'] == 'interaction.touchscreen.bodylights':
        mqtt_pubevent(latest['event'], latest['params'], 'Watch my lights flicker!');
	trigger('lights.colours', {'theme':'body.red'}, True)
	time.sleep(1)
	trigger('lights.colours', {'theme':'body.green'}, True)
        time.sleep(1)
	trigger('lights.colours', {'theme':'body.blue'}, True)
        time.sleep(1)
	trigger('lights.colours', {'theme':'body.yellow'}, True)
        time.sleep(1)
	trigger('lights.colours', {'theme':'body.white'}, True)
