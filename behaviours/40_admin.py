import random
latest = get_latest()

if latest['event'] == 'brain.admin.starving':
	dec_stat('fullness')
if latest['event'] == 'brain.admin.full':
	inc_stat('fullness')

if latest['event'] == 'brain.admin.asleep':
	dec_stat('energy')
if latest['event'] == 'brain.admin.awake':
	inc_stat('energy')

if latest['event'] == 'brain.admin.sad':
	dec_stat('mood')
if latest['event'] == 'brain.admin.happy':
	inc_stat('mood')

if latest['event'] == 'brain.admin.bored':
	dec_stat('interest')
if latest['event'] == 'brain.admin.interested':
	inc_stat('interest')
