# -*- coding: utf-8 -*-

def VariableDictionnary(result) : 
    """
    Contains additional informations for each variables 

    VarDictype : name of each variable, unit, intensive or extensive 
    OrganizedVar : list of variables that lookalike
    """
    VarDictype = {
        ### EXTENSIVE VARIBLES 
        'Y' : {'name':'Output', 
               'type':'extensive',
               'unit':'technological unit'},
        'Pi': {'name':'$\Pi$ absolute profit', 
               'type':'extensive',
               'unit':'technological unit'},
        'W' : {'name':'Salary', 
               'type':'extensive',
               'unit':'Money per human'},
        'L' : {'name':'Labor', 
               'type':'extensive',
               'unit':'Humans'},
        'D' : {'name':'Total debt', 
               'type':'extensive',
               'unit':'Money'},
        'N' : {'name':'Population', 
               'type':'extensive',
               'unit':'Humans'},
        'P' : {'name':'Price', 
               'type':'extensive',
               'unit':'Money'},
        'K' : {'name':'Kapital', 
               'type':'extensive',
               'unit':'technological unit'},
        'I' : {'name':'Investment', 
               'type':'extensive',
               'unit':'technological unit'},
        'a' : {'name':'productivity', 
               'type':'extensive',
               'unit':'Technological unit per human'},       
        ### Typical rate of time
        'philips' : {'name':'Wage inflation rate', 
                     'type':'extensive',
                     'unit':'$t^{-1}$'},
        'g'     : {'name':'Output growth', 
                   'type':'extensive',
                   'unit':'$t^{-1}$'}, 
        'i'     : {'name':'inflation', 
                   'type':'extensive',
                   'unit':'$t^{-1}$'},        
        
        ### INTENSIVE VARIABLES     

        'lambda': {'name':'employement rate', 
                   'type':'intensive',
                   'unit':'no'},
        'omega' : {'name':'wage share', 
                   'type':'intensive',
                   'unit':'no'}, 
        'pi'    : {'name':'relative profit', 
                   'type':'intensive',
                   'unit':'no'},
        'kappa' : {'name':'relative investment to GDP', 
                   'type':'intensive',
                   'unit':'no'},
        'd'     : {'name':'Relative debt', 
                   'type':'intensive',
                   'unit':'no'},
        }

    Result_keys = result.keys()
    VarDicType_keys = list(VarDictype.keys())
    for key in VarDicType_keys:
        if key not in Result_keys:
            del VarDictype[key]

    OrganizedVar = {
        'intensive'          : [f for f in VarDictype if VarDictype[f]['type']=='extensive'],
        'extensive'          : [f for f in VarDictype if VarDictype[f]['type']=='intensive'],
        'rate'               : [f for f in VarDictype if VarDictype[f]['unit']=='$t^{-1}$'],
        'Money'              : [f for f in VarDictype if VarDictype[f]['unit']=='Money'],
        'Technological unit' : [f for f in VarDictype if VarDictype[f]['unit']=='technological unit'],
        'Humans'             : [f for f in VarDictype if VarDictype[f]['unit']=='Humans']
        }
    


    return VarDictype,OrganizedVar
                             