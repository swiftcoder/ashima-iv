
import sys

if sys.platform == 'darwin':
	from mac.ode import *
else:
	assert False, 'ODE not available for this platform'
