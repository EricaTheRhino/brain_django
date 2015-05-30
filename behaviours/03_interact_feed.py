# coding: utf-8

# Config moved to 00_config.py
#FEED_MAX = 3

#FEED_F_INC = '0.5'
#FEED_I_INC = '1.0'
#FEED_OVERFULL_M_DEC = '0.2'
#FEED_OVERFEED_M_DEC = '0.2'

#FEED_VFULL_E_DEC = '0.4'
#FEED_FULL_E_DEC = '0.2'

if latest['event'] == 'interaction.chin.press':# and latest['params']['state'] == 1:
	existing = get_in_last(300, latest['event'])
	mqtttext = 'Being Fed: '
	if get_stat('fullness') == 6:
		# Trying to overfeed - so maybe fart...
		if random.randint(1,2) == 1:
			play_sound('fart')
		# And get a little unhappy
		mqtttext += 'Definitely full now, (I would stop feeding me, as I could become quite grumpy)'
		dec_stat('mood', FEED_OVERFULL_M_DEC)

	elif len(existing) >= FEED_MAX:
		dec_stat('mood', FEED_OVERFEED_M_DEC)
		play_sound('fart')
		mqtttext += 'Feeling a bit sick now (Have been overfed!)'
		inc_stat('fullness', FEED_F_INC)
	else:
		# Getting more full
		f = inc_stat('fullness', FEED_F_INC)
		if f > 5:
			# Very full, so lose a little energy
			dec_stat('energy', FEED_VFULL_E_DEC)
			mqtttext += 'Getting a quite full now (Definitely stop feeding me soon or I will embarrass myself)'
		elif f > 4:
			# Quite full, so lose a small amount of energy
			dec_stat('energy', FEED_FULL_E_DEC)
			mqtttext += 'Getting a little full now (You should stop feeding me soon)'
		else:
			mqtttext += 'Yum!'

		inc_stat('interest', FEED_I_INC)

	mqtt_pubevent(latest['event'], latest['params'], mqtttext)

if latest['event'] == 'interaction.righteye.scan':
	play_sound('Rhinoceros3')
	trigger('rightear.servo.waggle', {'angle':-40, 'speed':1}, True)

if latest['event'] == 'interaction.lefteye.scan':
	play_sound('Rhinoceros3')
	trigger('leftear.servo.waggle', {'angle':-40, 'speed':1}, True)
