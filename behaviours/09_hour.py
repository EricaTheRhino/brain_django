# coding: utf-8

import time
latest = get_latest()

now = time.time()

if latest['event'] == 'brain.hour':
	dec_stat('energy', HOUR_E_DEC)
	mqtt_pubevent(latest['event'], latest['params'], 'Is that the time? Another hour gone!')
