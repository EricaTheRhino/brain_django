# coding: utf-8
latest = get_latest()

# Handle all energy

e = get_stat('energy')

if e == 0:
	# We're asleep - on every idle, we add a little to a buffer
	if latest['event'] == 'brain.idle':
		inc_stat('energy_buffer', SLEEP_E_INC)
	elif latest['event'].startswith('interaction.'):
		# No longer asleep!
		log('Erica is awake!')
		mqtt_pubevent(latest['event'], latest['params'], 'Woow, I\'m awake now! Who woke me up?');
		buf = get_stat('energy_buffer')
		set_stat('energy', buf)
		set_stat('energy_buffer', '0.0')

