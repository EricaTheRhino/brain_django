# coding: utf-8

from random import randint

latest = get_latest()

if latest['event'] == 'brain.reset':
	log('Resetting rhino.')

	#print all stats as retained topic
	mqtt_puballstats()
	mqtt_pubevent(latest['event'], latest['params'], 'Resetting ;)');
	
	r.ltrim('short_term', 0, 0)
	r.ltrim('log', 0, 0)
	r.delete('long_term')
	r.delete('stats')
	set_stat('fullness', randint(2,3)) 
	set_stat('energy', randint(3,5))
	set_stat('mood', randint(1,5))
	set_stat('interest', randint(3,5))
	set_stat('energy_buffer', 0)