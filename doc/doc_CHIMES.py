import pygemmes as pgm
import numpy as np
plt.close('all')

'''
pgm.get_available_models('CHIMES',details=True)
hub=pgm.Hub('CHIMES',preset='Bi-sectoral')
hub.run()
dict=hub.Extract_preset()
dict['u'][:,:,1,:]=0.1
del dict['nx'],dict['nr'],dict['Nprod']
hub.set_dparam(**dict)
hub.run()
'''

presets = ['Bi-sectoral','GoodwinPURE']
hub=pgm.Hub('CHIMES',preset=presets[0])
#hub.get_summary(removesector=('.','Consumption'))
#hub.get_summary(removesector=('.','Capital'))
#hub.get_summary(removesector=('Consumption','Capital'))

#hub.set_dparam(**{'Tmax':20})
hub.run()
R=hub.get_dparam()
sectors = R['Nprod']['list']
for sector in sectors :
    pgm.plots.plotnyaxis(hub, y=[[['inflation', sector],
                                  ['inflationMarkup', sector],
                                  ['inflationdotV', sector], ],
                                 [['dotV',sector]],
                                 [['c',sector],
                                  ['p',sector]],
                                 [['pi',sector],
                                  ['kappa',sector]],
                                 [['employmentlocal',sector],
                                  ['u',sector],
                                  ]],)
    pgm.plots.repartition(hub,
                          ['pi','omega','xi','gamma','rd','reloverinvest','reldotv'],
                          sign= [1,1,1,1,1,1,-1],
                          sector=sector,
                          title=f'Expected relative budget $\pi$ for sector {sector} ')
    pgm.plots.repartition(hub,['TakenbyY','TakenbyI','C','dotV'],
                          ref='Y',
                          sector=sector,
                          title=f'Physical Fluxes for sector {sector}')
    pgm.plots.repartition(hub,['Wage','TransactInter','TransactI','Consumption','Interests'],
                          ref='dotD',
                          sector=sector,
                          title=f'Monetary Fluxes for sector {sector}')



## Inflation, employment, use
pgm.plots.plotnyaxis(hub, y=[['philips'],
                             ['ibasket']+[['inflation',sector] for sector in sectors],
                             ['employment']+[['employmentlocal',sector] for sector in sectors] ,
                             ['uAGG'] + [['u', sector] for sector in sectors]
                             ],)
pgm.plots.plotnyaxis(hub, y=[['gammaAGG']+[['gamma',sector] for sector in sectors] ,
                             ['xiAGG'] + [['xi', sector] for sector in sectors],
                             ['piAGG'] + [['pi', sector] for sector in sectors],
                             ['omegaAGG'] + [['omega', sector] for sector in sectors],
                             ['rdAGG'] + [['rd', sector] for sector in sectors]
                             ],)
pgm.plots.plotnyaxis(hub, y=[['DAGG']+[['D',sector] for sector in sectors] ,
                             [['K', sector] for sector in sectors],
                             ['IAGG']+[['I',sector] for sector in sectors],
                             ['CAGG'],
                             ['GDPnomY']+[['pY',sector] for sector in sectors],
                             ],)

pgm.plots.plot3D(hub,
                 x='omegaAGG',
                 y='employment',
                 z='rdAGG',
                 color='time')
for sector in sectors :
    pgm.plots.plot3D(hub,
                     x=['omega',sector],
                     y=['employmentlocal',sector],
                     z=['rd',sector],
                     color='time')

dict={
'Tmax':80,
'Nprod': ['Consumption','Capital'],
'nx':1,

'alpha' : 0.02,
'n'     : 0.025,
'phinull':0.1,

'gammai':0,
'r':0.03,
'a':1,
'N':1,
'Dh':0,
'w':0.8,

'sigma':[1,1],
'K': [2.2,0.6],
'D':[0,0],
'u':[.90,.90],
'p':[1.5,3],
'V':[100,150],
'z':[1,1],
'k0': 1.3,

'Cpond':[1,0],

'mu0':[1.3,2],
'delta':0.05,
'deltah':0.05,
'eta':0.3,
'chi':[1,1],
'b':1,
'nu':3,

## MATRICES
'Gamma': [[0.1 ,0.015],
          [0.015 ,0.1]],
#'Xi': [['Consumption','Capital','Consumption','Capital'],
#       ['Consumption','Capital','Capital','Consumption'],[0,.5,1,0]],
'Xi': [[0.01,.5],[1,0.02]],
'rho': np.eye(2),
}



hub=pgm.Hub('CHIMES')
hub.set_dparam(**dict,verb=False)
hub.get_summary()
hub.run()
#hub.reinterpolate_dparam(N=200)
#hub.calculate_Cycles()
#hub.calculate_StatSensitivity()

'''
pgm.plots.plotbyunits(hub,
                            filters_key=('kappa','w','basket'),
                            filters_units=('$.y^{-1}',),#,'$.units^{-1}','','y^{-1}'],
                            filters_sector=(),
                            separate_variables={'':['pi','xi','gamma','rd','omega']})
'''

#pgm.plots.plotnyaxis(hub,y=[[['K','Consumption'],['K',"Capital"],['V','Consumption']],['employment']])



'''
# Repartition relative pi
pgm.plots.repartition(hub,['xi','gamma','omega','pi','rd','reldotv','reloverinvest'],sector='Consumption',title='')
pgm.plots.repartition(hub,['TakenbyY','TakenbyI','C','dotV'],ref='Y',sector='Consumption',dashboundary=False,title='')

# Repartition of physical fluxes
pgm.plots.repartition(hub,['xi','gamma','omega','pi','rd','reldotv','reloverinvest'],sector='Capital',title='')
pgm.plots.repartition(hub,['TakenbyY','TakenbyI','C','dotV'],ref='Y',sector='Capital',dashboundary=False,title='')
'''
# Repartition of monetary fluxes
for sector in ['Consumption','Capital']:
    pgm.plots.plotnyaxis(hub, y=[[['inflation', sector],
                                  ['inflationMarkup', sector],
                                  ['inflationdotV', sector], ],
                                 [['c',sector],
                                  ['p',sector]],
                                 [['employmentlocal',sector],
                                  ['u',sector],
                                  ]],)

    pgm.plots.plotnyaxis(hub, y=[[['kappa', sector],
                                  ['K', "Capital"],
                                  ['V', 'Consumption']],
                                 ['employment'], ])
    pgm.plots.repartition(hub,['pi','xi','gamma','omega','rd','reloverinvest','reldotv'],sector=sector,title='Expected relative budget $\pi$ ')
    pgm.plots.repartition(hub,['TakenbyY','TakenbyI','C','dotV'],ref='Y',sector=sector,dashboundary=False,title=sector)
    pgm.plots.repartition(hub,['TransactI','TransactInter','Consumption','Interests','Wage'],ref='dotD',sector=sector,dashboundary=False,title=sector)

pgm.plots.plotnyaxis(hub, y=[[['inflation', sector],
                              ['inflationMarkup', sector],
                              ['inflationdotV', sector], ],
                             [['c',sector],
                              ['p',sector]],
                             [['employmentlocal',sector],
                              ['u',sector],
                              ]],)