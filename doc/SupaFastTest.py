# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 17:50:35 2022

@author: Paul Valcke
"""

import pygemmes as pgm
import matplotlib.pyplot as pl

##########
pgm.get_available_solvers()
pgm.get_available_models(details=True, verb=True)
pgm.get_available_output()
pgm.get_available_dfields()
pgm.get_available_articles()
###########

hub = pgm.Hub('GK',)
hub
pgm.Generate_network_logics('GK')
hub.equations_description()
hub.dmodel  # Gives the content of the model file
hub.dmisc  # gives multiple informations on the run and the variables
hub.get_summary()
hub.run(verb=0)  # solver=listofsolver[0],verb=1.1)
hub.FillCyclesForAll(ref='lambda')
R = hub.get_dparam(returnas=dict)
groupsoffields = hub.get_dparam_as_reverse_dict(crit='units', eqtype=['ode', 'statevar'])

###############

hub = pgm.Hub('GK',)

hub.set_dparam(**{'alpha': [0, 0.01, 0.02, 0.03]})
hub.set_dparam(alpha=[0, 0.01, 0.02, 0.03])
hub.run()

#############
hub = pgm.Hub('GK', preset='default')
hub.run()
hub.reinterpolate_dparam(1000)
hub.plot_preset()
hub.plot()

#############

SensitivityDic = {
    'alpha': {'mu': .02,
              'sigma': .12,
              'type': 'log'},
    'k2': {'mu': 20,
           'sigma': .12,
           'type': 'log'},
    'mu': {'mu': 1.3,
           'sigma': .12,
           'type': 'log'},
}


presetSimple = pgm.GenerateIndividualSensitivity(
    'alpha', 0.02, .2, disttype='log', N=10)
presetCoupled = pgm.GenerateCoupledSensitivity(SensitivityDic, N=10, grid=False)

_DPRESETS = {'SensitivitySimple': {'fields': presetSimple, 'com': ''},
             'SensitivityCoupled': {'fields': presetCoupled, 'com': ''},
             }
hub = pgm.Hub('GK', preset='SensitivityCoupled', dpresets=_DPRESETS)
hub.run(verb=1.1)
hub.CalculateStatSensitivity()
dax = hub.plot(mode='sensitivity')

#############

lsolvers = [
    'eRK4-homemade',
    'eRK4-scipy',  # 'eRK8-scipy', 'eRK2-scipy',
]
dmodel = pgm.get_available_models(
    returnas=dict,
    from_user=False,
)
for model in dmodel.keys():
    lpresets = [None] + dmodel[model]['presets']
    for preset in lpresets:
        print(model, preset)
        hub = pgm.Hub(
            model,
            preset=preset,
            from_user=False,
            verb=False
        )
        hub.set_dparam(Tmax=10, verb=False)
        hub.run()

print('DONE !')
