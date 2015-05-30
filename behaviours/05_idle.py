# coding: utf-8

import random
latest = get_latest()

if latest['event'] == 'brain.idle':
	dec_stat('fullness', IDLE_F_DEC)

	#print all stats as retained topic
	mqtt_puballstats()

	# If nothing but idles in the RECENT_SECS, get a bit bored.
	recent = get_in_last(RECENT_SECS)
	nothing_happened = True
	for ev in recent:
		if not ev['event'] == 'brain.idle':
			nothing_happened = False

	if nothing_happened:
		interest = dec_stat('interest', IDLE_I_DEC)
		mqtt_pubevent(latest['event'], latest['params'], 'Nothing has happened, getting a little bored.')

