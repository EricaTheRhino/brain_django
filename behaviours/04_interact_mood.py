# coding: utf-8

import random
import time
latest = get_latest()

if latest['event'] == 'interaction.pir.detect':
	inc_stat('interest', PIR_I_INCREMENT)
	mqtt_pubevent(latest['event'], latest['params'], 'Ooo what\'s that! Something moved!')
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


if latest['event'] == 'interaction.chip.press' and latest['params']['state'] == 1:
	existing = get_in_last(300, latest['event'])
	mqtttext = 'HeHeHe, '
	if len(existing) > TICKLE_MAX:
		# Tickled too much - a bit unhappy and tired.
		if len(existing) < TICKLE_MAX + 5:
			dec_stat('energy', TICKLE_E_DEC)
		dec_stat('mood', TICKLE_M_DEC)
		mqtttext += 'I have been tickled too much now :('
	else:
		inc_stat('mood', TICKLE_M_INC)
		inc_stat('interest', FEED_I_INC)
		mqtttext += 'that tickles!'

	mqtt_pubevent(latest['event'], latest['params'], mqtttext)
