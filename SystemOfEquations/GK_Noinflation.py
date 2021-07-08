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
            'a': {  'f'   : lambda y, p : p['alpha'] *y['a'],
                    'type': 'differential',
                    'com' : 'Exogenous technical progress as an exponential'},
            'N': {  'f'   : lambda y, p : p['beta']*y['N'],   
                    'type': 'differential',
                    'com' : 'Exogenous population as an exponential'},
            'K': {  'f'   : lambda y, p : y['I'] - y['K']*p['delta'],
                    'type': 'differential',
                    'com' : 'Capital evolution from investment and depreciation'},
            'W': {  'f'   : lambda y, p : y['W'] * ( y['philips']  ),
                    'type': 'differential',
                    'com' : 'Wage evolution through philips curve'},
            'D': {  'f'   : lambda y, p : y['I'] - y['Pi'],
                    'type': 'differential',
                    'com' : 'Debt as Investment-Profit difference'},
            
            ### INTERMEDIARY
            'Y': {  'f'   : lambda y, p : y['K'] / p['nu'],
                    'type': 'intermediary',
                    'com' : 'Optimized-Leontiev Output'},
            'L': {  'f'   : lambda y, p : y['K'] / (y['a'] * p['nu']),
                    'type': 'intermediary',
                    'com' : 'Optimized-Leontiev Labor'},
            'Pi': {  'f'   : lambda y, p : y['Y'] - y['W']*y['L'] - p['r']*y['D'],
                    'type': 'intermediary',
                    'com' : 'Profit from Say law with labor and debt'},
            'lambda': {'f': lambda y, p : y['L'] / y['N'],
                    'type': 'intermediary',
                    'com' : 'employement from labor and population'},
            'omega': {'f' : lambda y, p :y['W'] * y['L'] / y['Y'],
                    'type': 'intermediary',
                    'com' : 'wage share from WL/Y'},
            'philips':{'f': lambda y, p :- p['phi0'] + p['phi1']/ (1-y['lambda'])**2 ,
                    'type': 'intermediary',
                    'com' : 'Philips curve with divergence'},
            'kappa': {'f' : lambda y, p : p['k0'] + p['k1'] * np.exp(p['k2']*y['Pi']/y['Y']),
                    'type': 'intermediary',
                    'com' : 'relative investment curve on profit typical Keen model'},
            'I':    {'f': lambda y, p :y['Y'] * y['kappa']   ,
                    'type': 'intermediary',
                    'com' : 'Investment typical Keen model'},   
            
            ### AUXILLIARY 
            'g': {  'f'   : lambda y, p : (1-y['omega']) / p['nu'] - p['delta'],
                    'type': 'auxilliary',
                    'com' : 'explicit instant growth definition'},
            'd': {  'f'   : lambda y, p : y['D'] / y['Y'],
                    'type': 'auxilliary',
                    'com' : 'rekatuve debt D/Y'},
            'pi': {  'f'   : lambda y, p : 1 - y['omega'] - p['r']*y['d'],
                    'type': 'auxilliary',
                    'com' : 'relative profit as 1-omega-rd'},   
            'i': {  'f'   : lambda y, p : y['Y']*0,
                    'type': 'auxilliary',
                    'com' : 'NO INFLATION HERE'},   
            }

        self.parameters = ['r','k0','k1','k2',     # investment-debt parameters
                           'alpha','delta','beta', # time-rate parameters
                           'nu',                   # UnEfficiency of capital
                           'phi0','phi1']          # Salary negociation

    def plotlitst_simple(self,r,p):
        '''Launch all plots that don't need further understanding'''
        #plts.GoodwinKeenTypical(r, p,)      # Typical 3-Dimension phase-plot
        #plts.omegalambdacycles (r, p,)       # 2-D omega-lambda phase portrait
        #plts.GraphesIntensive  (r, p)      
        #plts.GraphesExtensive  (r, p) 
