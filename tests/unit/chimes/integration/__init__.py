import os
import sys

PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJ = os.path.join(os.path.dirname(PATH_HERE), '../')

sys.path.insert(0, PATH_PROJ)

# Integration test are oftne using multiple elements from the library at the same time
