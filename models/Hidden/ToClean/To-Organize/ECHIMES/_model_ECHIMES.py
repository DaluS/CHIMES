'''
FULL ECHIMES !

THIS FILE IS THE COMBINATION OF ALL MODULES
'''

from pygemmes._models import Funcs, importmodel,mergemodel

### THE TRUE CORE


############ ELEMENTS THAT CAN BE ADDED #############################
#_LOGICS, _PRESETS= importmodel('__EMPTY__')
_LOGICS  ,_PRESETS    = importmodel('CHIMES0')
_LOGICSCES,_PRESETSCES= importmodel('CESextension')          ### ADDING AUXILLIARY AGGREGATES
_LOGICSAGG,_PRESETSAGG= importmodel('MultisectoralAggregates')          ### ADDING AUXILLIARY AGGREGATES
_LOGICSACC,_PRESETACC = importmodel('Accessibility')                   ### ADDING ACCESSIBILITY
#_LOGICSEXCHANGE, _PRESETEXCHANGE = importmodel('InternationalExchange') ### ADDING INTERNATIONAL EXCHANGE
#####################################################################

#_LOGICS={}
#_LOGICS = mergemodel(_LOGICS, _LOGICS0, verb=True)
#_LOGICS = mergemodel(_LOGICS, _LOGICSCES,verb=False)          
#_LOGICS = mergemodel(_LOGICS, _LOGICSACC,verb=False)
#_LOGICS = mergemodel(_LOGICS, _LOGICSAGG)
#_PRESETS=_PRESETS0

