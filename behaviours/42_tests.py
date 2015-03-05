# coding: utf-8
import random
latest = get_latest()

if latest['event'] == 'brain.test.feeding':
	pass

if latest['event'] == 'brain.test.full':
	trigger('righteye.lights.level', {'level':1.0})
	trigger('righteye.servo.direction', {'dir':0.5})
	trigger('lefteye.lights.level', {'level':1.0})
	trigger('lefteye.servo.direction', {'dir':0.5})

	trigger('righteye.servo.direction', {'dir':1})
	trigger('lefteye.servo.direction', {'dir':1})

	play_sound('circle')
	# Test blink speeds
	for x in range(150, 50, -50):
		trigger('lefteye.lights.blink', {'time':x})
		trigger('righteye.lights.blink', {'time':x})
	# Test servo move
	play_sound('Rhinoceros'+str(random.choice(['11', '12', '13'])))
	trigger('righteye.servo.direction', {'dir':1})
	trigger('righteye.servo.direction', {'dir':0})
	trigger('righteye.servo.direction', {'dir':1})
	trigger('righteye.servo.direction', {'dir':0})
	trigger('righteye.servo.direction', {'dir':0.5})
	trigger('lefteye.servo.direction', {'dir':1})
	trigger('lefteye.servo.direction', {'dir':0})
	trigger('lefteye.servo.direction', {'dir':1})
	trigger('lefteye.servo.direction', {'dir':0})
	trigger('lefteye.servo.direction', {'dir':0.5})
	trigger('leftear.servo.waggle', {'angle':40}, True)
	trigger('rightear.servo.waggle', {'angle':-40})
	trigger('leftear.servo.waggle', {'angle':40}, True)
	trigger('rightear.servo.waggle', {'angle':40})
	trigger('leftear.servo.waggle', {'angle':-40}, True)
	trigger('rightear.servo.waggle', {'angle':-40})
	trigger('leftear.servo.waggle', {'angle':-40}, True)
	trigger('rightear.servo.waggle', {'angle':40})
	trigger('righteye.servo.waggle', {'dir':1})
	trigger('lefteye.servo.waggle', {'dir':1})

	trigger('lights.colours', {'theme':'horn.random'}, False)

	trigger('lights.colours', {'theme':'body.red'}, True)
        trigger('lights.colours', {'theme':'body.green'}, True)
        trigger('lights.colours', {'theme':'body.blue'}, True)
        trigger('lights.colours', {'theme':'body.yellow'}, True)
        trigger('lights.colours', {'theme':'body.white'}, True)
        trigger('lights.colours', {'theme':'body.off'}, True)

