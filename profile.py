#! /usr/bin/env python -O 

import cProfile as P
from src import app

P.run('app.run()', 'profile.txt')

import pstats

p = pstats.Stats('profile.txt')
p.sort_stats('cumulative').print_stats(35)
p.sort_stats('time').print_stats(35)
