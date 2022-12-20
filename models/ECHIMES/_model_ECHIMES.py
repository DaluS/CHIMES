'''
FULL ECHIMES !
THIS FILE IS THE COMBINATION OF ALL MODULES
'''

from pygemmes._models import Funcs, importmodel,mergemodel

############ ELEMENTS THAT CAN BE ADDED #############################
_LOGICS, _PRESETS= importmodel('__EMPTY__')
_LOGICS  ,_PRESETS  = importmodel('CHIMES0')
_LOGICSAGG,_PRESETSAGG= importmodel('MultisectoralAggregates')          ### ADDING AUXILLIARY AGGREGATES
_LOGICSACCES,_PRESETACCES = importmodel('Accessibility')                   ### ADDING ACCESSIBILITY
_LOGICSEXCHANGE, _PRESETEXCHANGE = importmodel('InternationalExchange') ### ADDING INTERNATIONAL EXCHANGE
#####################################################################

#_LOGICS = mergemodel(_LOGICS, _LOGICS0, verb=True)
#_LOGICS = mergemodel(_LOGICS, _LOGICSACCES,verb=False)
_LOGICS = mergemodel(_LOGICS, _LOGICSAGG)
#_PRESETS=_PRESETS0
