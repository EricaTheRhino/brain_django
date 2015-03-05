# coding: utf-8

latest = get_latest()

now = time.time()

if latest['event'] == 'environment.weather.pollen':
	band = latest['params']['pollen']
	if band == 'high':
		mqtt_pubevent(latest['event'], latest['params'], 'Achoo! Whoa, that pollen count is quite high!')
		play_sound('sneeze')
		dec_stat('mood')
	elif band == 'low':
		inc_stat('mood')

