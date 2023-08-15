# Importing the main library #################
import sys
path = "C:\\Users\\Paul Valcke\\Documents\\GitHub\\GEMMES"
sys.path.insert(0, path )
import pygemmes as pgm


hub=pgm.Hub('CausalModel')
hub.run()
#pgm.plots.XYZ(hub,'omega','employment','time',color='T')

pgm.plots.plotnyaxis(hub,[['omega','omegaeq'],['T']])