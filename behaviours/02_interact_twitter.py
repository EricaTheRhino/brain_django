

if latest['event'] == 'twitter.mention':
    inc_stat('mood', '0.8')
    inc_stat('energy', '0.2')
    play_sound('tweet')
    mqtt_pubevent(latest['event'], latest['params'], 'Someone has just mentioned me on twitter!')

if latest['event'] == 'twitter.colour':
    colour = latest['params']['colour']
    if colour in ['red', 'green', 'blue', 'aqua', 'pink', 'christmas', 'ice']:
	trigger('lights.colours', {'theme':'horn.'+colour}, False)
    	inc_stat('mood', '0.8')
    	mqtt_pubevent(latest['event'], latest['params'], 'Someone has just suggested ' + colour + ' on twitter!')
