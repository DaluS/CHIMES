# -*- coding: utf-8 -*-
"""
Welcome in pyGEMMES as a developper !

This is a readme on how to produce a model that the code will be able to execute.

A model needs three Things :
    _ A description
    _ An ensemble of logics
    _ An ensemble of preset

The system will fill everything you don't by himself (and through _def_fields), so it is very recommended to :
    * Look at what is inside the library ( `_core._class_checks.models.PrintDFIELDS()`)
    * Look at already-existing models (`_core._class_checks.models.describe_ALL_available_models()`) to get inspiration (or copy-paste it in a new file then modify it)

IF THE LOGIC IS DIFFERENT IT IS NOT THE SAME MODEL, DO NOT EDIT MODELS OF OTHER PEOPLE.
"""

# ############################################################################
"""
    ABSTRACT : A few words about this model
    TYPICAL BEHAVIOR : What you would expect from this model
    LINKTOARTICLE : A link to a typical article / file that has been published on this model
    """

_DESCRIPTION = """
    ABSTRACT : A physically irrelevant model just for the sake of the formalism
    TYPICAL BEHAVIOR : Good question. I assume saturation toward a positive value
    LINKTOARTICLE : I hope no one published that thing
    """


# ############################################################################
'''
The structure of logics is the following :
    * _LOGICS is a dictionary
    * It contains dictionaries, each of them is a specific category of logical link :
        a) 'ode' which contains Ordinary differential equations
        b) 'statevar' which contains State Variable (fully defined by the state of the ode variables, and other state variables)
        c) 'parameters' which contains parameters that are not defined in `_def_fields.py` that you want too add
    * Every field that you add here will have the priority over `_def_fields` (the default library)
    * If something is not in the library and you want to add it while working on your model, add it here in its category. The system will handle it. Only add to the library once your model is finished.
    * If a field name is already taken in the library, DO NOT OVERLOAD it. Use a different name (so that models are not inconsistent with each others)
    * When you defined a new field it needs AT LEAST :
        * 'logic' (either a lambda function, a function call, or just a numerical value)
        * 'com' which is a comment about what you are doing through that equation and hypothesis behind.
    * The system can be fed with the following aditional elements for each field :
        * 'initial' in the case of an ode, it will overload this value (necessary if field is not in `_def_fields`)
        * 'units' the units written in a latex writing. for example "150 units.humans^{-1}.years^{-1}" ( space delineator between multiplier and units, . between units, ^{ } for exponent)
        * 'definition' which is the definition of the variable.
        * symbol, the latex symbol of the variable

        Typically, these three elements are taken from _def_fields so fill only add them when it's needed.

    To write a logic :
        * the simplest way is to use lambda functions ( lambda x,y : x+y for example). You can in the code do `def function(x,y): return x+y` and say 'logic' : function(x,y)
        * The name you put for the variables are important ! it will be read by the code for autocompletion ( order of resolution, who is calling who...)
        * if you need to call variable `lambda`, use `lamb`, the system will understand
        * if a variable logic needs its own value (only in ODE), use `itself` as the name of the variable
        * you need to give a value in it, just for a symbolic execution. You can put any number as long as you do not divide by zero with the set of value you put.

        For example if X is an ode with logic `lambda itself=0,lamb=1 : itself/lamb` the system will solve dX/dt = X(t)/lambda(t)
'''


def func(firstvar, param1, param2):
    '''
    This is a big function so we can put it on multiple lines
    '''
    intermediarystep = firstvar**param1
    return intermediarystep - param2


_LOGICS = {
    # All variables determined by ordinary differential equations
    'ode': {
        'firstvar': {
            'logic': lambda secondvar=0: secondvar,
            'com': 'I am the ODE that define the evolution of firstvar',
            'initial': 0,
            'def': 'The secret variable of the universe',
            'units': '42 y^{24}.dollars^[-1}'
        },
    },
    # All variables Full determined by the state of the system
    'statevar': {
        'secondvar': {
            'logic': func(firstvar=0, param1=1, param2=1),
            'com': 'I am a state variable fully defined by firstvar',
            'symbol': '$\Omega$'
        },
    },
    'parameters': {
        'param1': {
            'logic': 2,
            'com': 'I am a parameter of value 2',
        },
        'param2': {
            'logic': 1,
            'com': 'I am a parameter of value 1',
        },
    }
}


# ###########################################################################
'''
_PRESETS is a dictionnary(1) of dictionary(2), each dictionnary(2) being a preset.
A preset contains three things :
    * His name (the key of the dictionnary)
    * 'fields': that contains all the values that should be tested in the shape { key1 : numericalvalue, key2 : numericalvalues }
    * 'com' is a str to tell the user what he should expect from this model

    if a value is not in fields, it wont be changed
'''
_PRESETS = {
    'A first set': {
        'fields': {
            'firstvar': 5,  # it will modify the initial condition
            'param2': 3,  # it will modify the parameter value
        },
        'com': "a different set of parameters. no idea of the result"
    },
    'a second set': {
        'fields': {
            'param2': 2,  # it will modify the parameter value
        },
        'com': "a different set of parameters, physically irrelevant"
    },
}
