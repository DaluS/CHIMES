'''
FULL ECHIMES !

THIS FILE IS THE COMBINATION OF ALL MODULES
'''

from pygemmes._models import Funcs, importmodel,mergemodel
_LOGICSAGG,_PRESETSAGG= importmodel('MultisectoralAggregates')
_LOGICS0  ,_PRESETS0  = importmodel('CHIMES0')
_LOGICSEXCHANGE, _PRESETEXCHANGE = importmodel('InternationalExchange')
_LOGICS={}
_PRESETS={}
