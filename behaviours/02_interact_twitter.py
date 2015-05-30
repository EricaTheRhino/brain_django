

if latest['event'] == 'twitter.mention':
    inc_stat('mood', TWITTER_M_INC)
    inc_stat('energy', TWITTER_E_INC)
    play_sound(TWITTER_SOUND)
    mqtt_pubevent(latest['event'], latest['params'], 'Someone has just mentioned me on twitter!')

if latest['event'] == 'twitter.colour':
    colour = latest['params']['colour']
    if colour in ['red', 'green', 'blue', 'aqua', 'pink', 'christmas', 'ice']:
	trigger('lights.colours', {'theme':'horn.'+colour}, False)
    	inc_stat('mood', TWITTER_M_INC)
	inc_stat('energy', TWITTER_E_INC)
    	mqtt_pubevent(latest['event'], latest['params'], 'Someone has just suggested ' + colour + ' on twitter!')
