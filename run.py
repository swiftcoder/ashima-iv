#! /usr/bin/env python -O 

import sys

# ugly hack to work around a py2app deficiency
# py2app can't find the included pyode module without this
sys.path.insert(0,'../Resources/lib/python2.5/lib-dynload')

from src import app

app.run()
