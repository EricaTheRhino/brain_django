from processor.scripting import *

short_term = get_short_term()
latest = short_term[0]

if latest['event'] == 'mech.on':
	trigger('mech.led_on', {'n':1})

if latest['event'] == 'mech.off':
	trigger('mech.led_off', {'n':1})
