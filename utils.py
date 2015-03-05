import random

def mood_to_text(key):

	options = {
		"asleep":[
			"Zzzzzzz",
			"Just having a little nap.",
		]
	}
	if key in options:
		return random.choice(options[key])
	else:
		return key
