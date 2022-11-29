'''
FULL ECHIMES !

THIS FILE IS THE COMBINATION OF ALL MODULES
'''

from pygemmes._models import Funcs, importmodel,mergemodel

### THE TRUE CORE
_LOGICS0  ,_PRESETS0  = importmodel('CHIMES0')

############ ELEMENTS THAT CAN BE ADDED #############################
_LOGICSAGG,_PRESETSAGG= importmodel('MultisectoralAggregates')          ### ADDING AUXILLIARY AGGREGATES
_LOGICSACC,_PRESETACC = importmodel('Accessibility ')                   ### ADDING ACCESSIBILITY
_LOGICSEXCHANGE, _PRESETEXCHANGE = importmodel('InternationalExchange') ### ADDING INTERNATIONAL EXCHANGE
#####################################################################
_LOGICS={}
_PRESETS={}
