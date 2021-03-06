# coding: utf-8

latest = get_latest()

now = time.time()

if latest['event'] == 'environment.weather.temperature':
	# Decide how best to handle this.
	if latest['params']['temperature'] > 20:
		# At hottest, get more energy and better mood.
		inc_stat('mood', TEMP_M_INC)
		dec_stat('energy', TEMP_E_DEC)
		mqtt_pubevent(latest['event'], latest['params'], 'Boy, it\'s a bit hot today!')
	elif latest['params']['temperature'] > 15:
		inc_stat('mood', TEMP_M_INC)
		mqtt_pubevent(latest['event'], latest['params'], 'Aah, the temperature is about right!')
	elif latest['params']['temperature'] > 10:
		dec_stat('mood', TEMP_M_DEC)
		mqtt_pubevent(latest['event'], latest['params'], 'Ooh, it\'s a bit chilly today!')
	else:
		# At coldest, get a bit down, and a bit lethargic.
		dec_stat('mood', TEMP_M_DEC)
		dec_stat('energy', TEMP_E_DEC)
		mqtt_pubevent(latest['event'], latest['params'], 'Brrr, I\'m frozen!')
