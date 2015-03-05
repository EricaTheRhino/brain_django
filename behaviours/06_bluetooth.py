# coding: utf-8

latest = get_latest()

team = {
	'7C:11:BE:42:E1:46':'moj'
}

def greet_team_member(scripting, nick):
	if nick == 'moj':
		scripting.trigger('leftear.servo.waggle', {'angle':40}, True)

def recognise(scripting, address):
	global team
	global greet_team_member
	if address in team:
		greet_team_member(scripting, team[address])
	else:
		inc_stat('interest')

#if latest['event'] == 'environment.bluetooth.found':
#	recognise(scripting, latest['params']['address'])
