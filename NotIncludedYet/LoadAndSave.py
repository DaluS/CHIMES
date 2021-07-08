# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 14:49:18 2021

@author: Paul Valcke
"""

import shutil
from datetime import datetime
import os


def savedata(rootfold,t,Y_s,p,op):  
    date = str(datetime.now()).split(' ')[0]
    try : os.mkdir(rootfold+date)
    except BaseException : print('Folder of the day already created')
    Nfolder = os.listdir(rootfold+date+'/')
    Fold    = rootfold+date+'/Expe_'+str(len(Nfolder))
    os.mkdir(Fold)   
    #pickle.dump(t  ,      open(Fold+'/t.p'      ,"wb"))
    print("THIS SHOULD BE WRITTEN WITH THE RELEVANT VARIABLES AGAIN")
    
    codefolder = os.getcwd()
    shutil.copyfile(codefolder+'/FunctionsGoodwin.py'     ,Fold+'/FunctionsGoodwin.py' )
    shutil.copyfile(codefolder+'/Main.py'                 ,Fold+'/Main.py' )
    print('data saved in :',Fold)
