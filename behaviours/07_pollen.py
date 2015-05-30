# coding: utf-8

latest = get_latest()

now = time.time()

if latest['event'] == 'environment.weather.pollen':
	band = latest['params']['pollen']
	if band == 'high':
		mqtt_pubevent(latest['event'], latest['params'], 'Achoo! Whoa, that pollen count is quite high!')
		play_sound(POLLEN_HIGH_SOUND)
		dec_stat('mood', POLLEN_M_DEC)
	elif band == 'low':
		inc_stat('mood', POLLEN_M_INC)

