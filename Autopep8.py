# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 14:59:42 2021

@author: Paul Valcke
"""

import autopep8
import os 

files = [ f for f in os.listdir() if '.py' in f]

for filename in files : 
    original  = open(filename,'r')
    code = original.read()
    codeclean = autopep8.fix_code(code)
    
    new= open('N'+filename,'w')
    new.write(codeclean)
    new.close()