
import sys

if sys.platform == 'darwin':
	from mac.ode import *
if sys.platform == 'win32':
	from win32.ode import *
	InitODE()
else:
	assert False, 'ODE not available for this platform'
