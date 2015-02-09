# http://cyrille.rossant.net/profiling-and-optimizing-python-code/
import pstats
pstats.Stats('profile_out1.txt').strip_dirs().sort_stats('cumulative').print_stats()