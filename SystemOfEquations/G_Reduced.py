# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 11:59:07 2021

@author: Paul Valcke
"""
import numpy as np

class MODEL():
    """
    MODEL : GOODWIN-KEEN NO INFLATION
    
    DESCRIPTION : Extensive variable dynamics of a simple Goodwin-Keen model.  
    
    LINKTOARTICLE : 
    """
    
    def __init__(self):            
        self.EQUATIONS = { 
            ### DYNAMICALLY-DEFINED ELEMENTS     
            'lambda': {  'f'   : lambda y, p : y['lambda']*(y['g'] -p['alpha'] -p['beta']) ,
                    'type': 'differential',
                    'com' : 'Employement dynamics'},
            'omega': {  'f'   : lambda y, p : y['omega']*y['phillips'],   
                    'type': 'differential',
                    'com' : 'Wage share dynamics'},
            
            ### INTERMEDIARY
            'pi'      : {  'f'   : lambda y, p : 1 - y['omega'] ,
                    'type': 'intermediary',
                    'com' : 'Profit from Say law with labor'},
            'phillips':{'f': lambda y, p :- p['phi0'] + p['phi1']/ (1-y['lambda'])**2 ,
                    'type': 'intermediary',
                    'com' : 'Philips curve with divergence'},
            'g':       {  'f'   : lambda y, p : (y['pi']) / p['nu'] - p['delta'],
                    'type': 'intermediary',
                    'com' : 'explicit instant growth definition'},
            
            ### AUXILLIARY 



            }

        self.parameters = ['alpha','delta','beta', # time-rate parameters
                           'nu',                   # UnEfficiency of capital
                           'phi0','phi1']          # Salary negociation

        self.OrderOfIntermediaryFuncs = ['pi','phillips','g']
    def plotlitst_simple(self,r,p):
        '''Launch all plots that don't need further understanding'''
        #plts.GoodwinKeenTypical(r, p,)      # Typical 3-Dimension phase-plot
        #plts.omegalambdacycles (r, p,)       # 2-D omega-lambda phase portrait
        #plts.GraphesIntensive  (r, p)      
        #plts.GraphesExtensive  (r, p) 
