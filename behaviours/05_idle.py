# coding: utf-8

import random
latest = get_latest()

if latest['event'] == 'brain.idle':
	dec_stat('fullness', 0.5)

	#print all stats as retained topic
	mqtt_puballstats()

	# If nothing but idles in the last 5 minutes, get a bit bored.
	recent = get_in_last(300)
	nothing_happened = True
	for ev in recent:
		if not ev['event'] == 'brain.idle':
			nothing_happened = False

	if nothing_happened:
		interest = dec_stat('interest', '1.0')
		mqtt_pubevent(latest['event'], latest['params'], 'Nothing has happened, getting a little bored.')

