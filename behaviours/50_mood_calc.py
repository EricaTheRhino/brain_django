# coding: utf-8

import random
import time
import math
import operator
from collections import defaultdict
latest = get_latest()

now = time.time()

# Based on the various inputs, etc, work out the new moods.

atoms = get_mood_atoms()
set_moods(atoms)


#trigger('horn.colours', {'theme':'hues', 'rate':(get_stat('energy')/Decimal(6.0)), 'time':10000})

#if curr == 'grumpy':
#	trigger('horn.colours', {'theme':'fire', 'time':500})
#elif curr == 'sad':
#	trigger('horn.colours', {'theme':'ice', 'time':500})
#else:
#	trigger('horn.colours', {'theme':'hues', 'time':500})

