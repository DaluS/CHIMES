# -*- coding: utf-8 -*-

'''
Core of the GEMMES resolution.
This program contains the class Hub which is the intermediary in all steps :
    * Initialisation
    * Load
    * Editing
    * Resolving
    * Analyzing
    * Plotting
    * Saving
'''

# %% Importations ###########


# Common
import numpy as np
import inspect

# Library-specific
from utilities import _utils, _class_checks, _class_utility
from utilities import _solvers, _saveload
import _plots as plots


class Hub():
    """
    Generic class to stock every data and method for the user to interact
    with.
    """

    _MODEL = 'GK'  # Default model to be loaded

    # ###################
    # %% Initialisation #
    # ###################
    def __init__(self, model='GK', loadLibrary=True):

        # The dictionary that will contains everything related to variables
        # and parameters
        self.__dparam = {}

        # A few informations that could be useful
        self.__dmisc = dict.fromkeys(['model',      # Model name
                                      'func_order',  # ordered list of statevar
                                      'run',        # Flag to check if run
                                      'solver',     # Name of the solver used
                                      'description',  # model string description
                                      'preset',     # Dictionnary of presets
                                      ])

        # PROCESS TO INITIALIZE THE SYSTEM
        if loadLibrary:
            # Get the general fields in self._DFIELDS
            self.Load_BasicLibrary()

        if model is not False:
            # Get the content of the model in self._DMODEL
            self.Load_ModelFiles(model)

        # Mixing both into the dic we will edit (__dparam)
        self.Dparam_from_dfields_and_dmodel()
        _class_checks.CheckDparam(self.__dparam)
        self.__dparam, _, self.__dmisc['func_order'] = \
            _class_checks.check_dparam(self.__dparam)
        self.CreateDargs()

    # ########################################
    # %% Setting  parameters at initialisation
    # ########################################

    def Load_BasicLibrary(self):
        '''
        Load the library in /models/_def_fields.py called _DFIELDS
        '''
        self._DFIELDS = _class_checks.loadlibrary()

    def Load_ModelFiles(self, MODNAME):
        '''
        Load the model in /models/_model_MODNAME.py
        '''

        # Load the file
        self._DMODEL = _class_checks.loadmodel(MODNAME)
        self.__dmisc['model'] = MODNAME
        self.__dmisc['func_order'] = self._DMODEL.get('func_order', '')
        self.__dmisc['description'] = self._DMODEL['description']
        self.__dmisc['preset'] = self._DMODEL['presets']
        self.__dmisc['sizeForced'] = []

        # Get new formalism
        self._DMODEL['dparam'] = _class_checks.ModelNewFormalism(
            self._DMODEL['dparam'])

        # Find the parameters
        self._DMODEL['dparam'], self.__dmisc['parameters'] = \
            _class_checks.FindParameters(self._DMODEL['dparam'])

    def Dparam_from_dfields_and_dmodel(self):
        '''
        Create __dparam based on _DFIELDS and _DMODEL

        This is done in three steps :
            * Loading _DMODEL['dparam'] as the basis
            * Calling complements for each key from the library
            (or invent them)
            * Calling the numerical group into dparam

            ! NUMERICAL GROUP FIELDS HAVE PRIORITY OVER MODEL FOR HE MOMENT
        '''
        Comments = ''

        # 1) Load _DMODEL['dparam']###########################
        for key, val in self._DMODEL['dparam'].items():
            self.__dparam[key] = dict(val)

        # 2) Complete through _DFIELD ##########################
        for key, val in self.__dparam.items():

            if key not in self._DFIELDS.keys():
                # 2.A) If there is nothing about the field in the library

                print(key, (15-len(key))*' ', 'Is autofilled from model')
                self.__dparam = _class_checks.FillasFields(key, self.__dparam)

            else:
                # 2.B) Completion with the library _DFIELDS

                dfieldkey = self._DFIELDS.get(key, {})

                # 2.B.1) insertion of all fields non-related
                # to functions/ode/parameters
                Listkeys = ['definition', 'com',
                            'units', 'type', 'symbol', 'group', 'eqtype']
                for basicKey in Listkeys:
                    if basicKey not in val.keys():
                        val[basicKey] = dfieldkey[basicKey]

                # 2.B.2) Instertion of function/ode/parameters specific fields
                if val['eqtype'] == 'ode':
                    # If it is an ODE, load the initial value
                    if (val['initial'] is not None and
                            'value' in dfieldkey.keys()):
                        Comments += key+' initial value taken from model \n'
                    elif (val['initial'] is None and
                            'value' not in dfieldkey.keys()):
                        raise Exception(
                            key+" no initial value in model nor field")
                    else:
                        val['initial'] = dfieldkey['value']

                # If it is a parameter, load the value
                if val['eqtype'] == 'parameters':
                    if ('value' in val.keys() and
                            'value' in dfieldkey.keys()):
                        Comments += key+' value taken from model \n'
                    elif ('value' not in val.keys() and
                            'value' not in dfieldkey.keys()):
                        raise Exception(
                            key+" no value in model nor field")
                    else:
                        val['value'] = dfieldkey['value']

                # If it is a function, just be sure that you copy everything
                # that is needed from the field !
                elif dfieldkey['eqtype'] == 'statevar':
                    for Newkey, newval in dfieldkey.items():
                        if Newkey not in val.items():
                            val[Newkey] = newval
                    val['kargs'] = inspect.getfullargspec(val['func']).args,

        # print(Comments)

        # 3) Load Numerical group ############################
        lknum = [
            k0 for k0, v0 in self._DFIELDS.items()
            if v0['group'] == 'Numerical'
        ]
        for k0 in lknum:
            if k0 not in self.__dparam.keys():
                self.__dparam[k0] = self._DFIELDS[k0]

        # 3.a) Add time vector if missing
        if 'time' not in self.__dparam.keys():
            self.__dparam['time'] = self._DFIELDS['time']

    def CreateDargs(self):
        '''
        Dargs contains all the values and variables for run execution
        '''
        self.__dargs = {}
        lode = self.get_dparam(eqtype='ode', returnas=list)
        linter = self.get_dparam(eqtype='statevar', returnas=list)
        laux = self.get_dparam(eqtype='auxiliary', returnas=list)

        self.__dargs = {
            k0: {
                k1: self.__dparam[k1]['value']
                for k1 in (
                    self.__dparam[k0]['args']['ode']
                    + self.__dparam[k0]['args']['statevar']
                    + self.__dparam[k0]['args']['auxiliary']
                )
                if k1 != 'lambda'
            }
            for k0 in lode + linter + laux
        }

        # Handle the lambda exception here to avoid test at every time step
        # if lambda exists and is a function
        c0 = (
            'lambda' in self.__dparam.keys()
            and self.__dparam['lambda'].get('func') is not None
        )
        # then handle the exception
        for k0, v0 in self.__dargs.items():
            if c0 and 'lambda' in self.__dparam[k0]['kargs']:
                self.__dargs[k0]['lamb'] = self.__dparam['lambda']['value']

        # reset all variables
        self.reset()

    def Change_Attributes(self, dictofChanges):
        '''
        Change a set of attributes in dparam.
        If necessary, change the number of system

        forcing mean giving an list of values with a well determined number of
        system. The system cannot be forced on multiple values

        The dictofchanges has to look like :

        { key : float,
          key : [min,max,type]} #type being either 'lin' or 'log'
          key : [val1...valn] #which force the system to be of size n
            }
        '''
        # 1.a) CHECK THE KEY OF CHANGES
        for key in dictofChanges.keys():
            # 1) Check that the change is allowed
            # the key exist
            if key not in self.__dparam.keys():
                raise Exception(key + ' Not in the model !')
            # 2) the key concern a function
            if self.__dparam[key]['eqtype'] == 'statevar':
                raise Exception(
                    key + ' Is a statevariable, you cannot force it')

        # 1.b) CHECK THE FORCING VALUE
        sizes = []
        size = self.__dparam['nx']['value']
        for val in dictofChanges.values():
            # If the change is explicitely multisystem
            if isinstance(val, list):
                # If the change is not a range
                if not (len(val) == 3 and type(val[-1]) is str):
                    sizes.append(len(val))
        sizes = list(set(sizes))
        if len(sizes) >= 2:
            raise Exception(
                "You are forcing two number of sectors at the same time")
        elif len(sizes) == 1:
            if sizes[0] != self.__dparam['nx']['value']:
                # Check if the size of the system had already been forced
                # And if this forcing is not changed
                for keyforcedbefore in self._dmisc['sizeForced']:
                    if keyforcedbefore not in dictofChanges.keys():
                        raise Exception(
                            keyforcedbefore + ' was already forced' +
                            'at a different size')
                size = sizes[0]

        # 1.c) CHECK THAT IF nx IS EXPLICITELY CHANGED IT IS CONSISTENT
        # WITH FORCING
        if 'nx' in dictofChanges.keys():
            if (size != self.__dparam['nx']['value'] and
                    size != dictofChanges['nx']):
                raise Exception(
                    'Forcing is detected on value'+str(size) +
                    'While you ask for'+str(dictofChanges['nx'])+'systems')
            else:
                size = dictofChanges['nx']

        # 2) Rewrite the change with new sizes
        if size != self.__dparam['nx']['value']:
            print('The system detected a new size :', size)
            NewdictofChanges = self.ChangeSystemsize(self, dictofChanges, size)
        else:
            NewdictofChanges = dict(dictofChanges)

            # 2) ADD THE UPDATES
        for key, var in NewdictofChanges.items():
            print(key, var)
            # Change the value or the initial
            if self.__dparam[key]['eqtype'] == 'ode':
                self.__dparam[key]['initial'] = var
            else:
                self.__dparam[key]['value'] = var

            # Add the forcing flag
            if isinstance(val, list):
                # If the change is not a range
                if not (len(val) == 3 and type(val[-1]) is str):
                    pass

        # reset everything
        self.reset()

    # ##############################
    # run simulation
    # ##############################

    def run(
        self,
        compute_auxiliary=None,
        solver=None,
        verb=None,
        rtol=None,
        atol=None,
        max_time_step=None,
    ):
        """ Run the simulation

        Compute each time step from the previous one using:
            - parameters
            - differentials (ode)
            - intermediary functions in specified func_order

        """
        # ------------
        # check inputs
        (
            verb, end, flush, timewait,
            compute_auxiliary, solver, solver_scipy,
        ) = _class_checks._run_check(
            verb=verb, compute_auxiliary=compute_auxiliary, solver=solver,
        )

        # ------------
        # reset variables
        self.reset()

        # time vector
        nt = self.__dparam['nt']['value']

        # ------------
        # temporary dict of input
        lode = self.get_dparam(eqtype='ode', returnas=list)
        linter = self.__dmisc['func_order']
        laux = self.get_dparam(eqtype='auxiliary', returnas=list)

        # ------------
        # start time loop
        if solver == 'eRK4-homemade':

            _solvers._eRK4_homemade(
                dparam=self.__dparam,
                lode=lode,
                linter=linter,
                laux=laux,
                dargs=self.__dargs,
                nt=nt,
                verb=verb,
                timewait=timewait,
                end=end,
                flush=flush,
                compute_auxiliary=compute_auxiliary,
            )

        elif 'scipy' in solver:
            sol = _solvers._solver_scipy(
                dparam=self.__dparam,
                lode=lode,
                linter=linter,
                dargs=self.__dargs,
                verb=verb,
                rtol=rtol,
                atol=atol,
                max_time_step=max_time_step,
                solver_scipy=solver_scipy,
            )

        self.__dmisc['run'] = True
        self.__dmisc['solver'] = solver

    # ##############################
    # %% plotting methods
    # ##############################

    def plot(self):
        """
        Launch all the basic plots
        """

        # plot per units


# ############################################################################
# %%#################### EVERYTHING THAT IS ALREADY WORKING WELL #############
# ############################################################################

    # ##############################
    # %% Analysis methods for cycles
    # ##############################
    def InitiateCyclesDictionnary(self):
        '''
        Create the structure that will contains
        '''
        for var, dic1 in self.__dparam.items():
            if 'func' in dic1.keys():
                dic1['cycles'] = {
                    'period_indexes':  # [[idx1,idx2],[idx2,idx3],] borders
                    [self.__dparam['nx']['value']*[None]],
                    'period_T_intervals':  # [t[idx1,t[idx2]],..] borders time
                    [self.__dparam['nx']['value']*[None]],
                    't_mean_cycle':  # time of the middle of the cycle
                    [self.__dparam['nx']['value']*[None]],
                    'period_T':  # duration of the cycle
                    [self.__dparam['nx']['value']*[None]],
                    'meanval':  # mean value during the interval
                    [self.__dparam['nx']['value']*[None]],
                    'stdval':  # standard deviation during the interval
                    [self.__dparam['nx']['value']*[None]],
                    'minval':  # minimal value in the interval
                    [self.__dparam['nx']['value']*[None]],
                    'medval':  # minimal value in the interval
                    [self.__dparam['nx']['value']*[None]],
                    'maxval':  # maximal value in the interval
                    [self.__dparam['nx']['value']*[None]],
                    'reference':  # the variable that has been used to detect
                    [self.__dparam['nx']['value']*[None]],
                }

    def FillCyclesForAllVar(self, idx='all', ref=None):
        '''
        This function is a wrap-up on GetCycle to do it on all variables.

        For each variables, it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself
        '''
        self.InitiateCyclesDictionnary()

        if idx == 'all':
            idxV = range(self.__dparam['nx']['value'])
        elif type(idx) is list:
            idxV = idx
        else:
            idxV = [idx*1]

        if self.__dmisc['run']:
            for idx in idxV:
                for var, dic1 in self.__dparam.items():
                    if 'func' in dic1.keys():
                        if ref is None:
                            self.FillCycles(var, var, idx=0)
                        else:
                            self.FillCycles(var, ref, idx=0)
        else:
            print('Cycle Detection impossible : system did not run')

    def FillCycles(self, var, ref='lambda', idx=0):
        '''
        it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself

        var: name of the variable we are working on
        ref: reference for the oscillations detections
        '''

        # Get the new dictionnary to edit
        dic = self.__dparam[var]
        if 'cycles' not in dic:
            self.InitiateCyclesDictionnary()

        # check if reference has already calculated its period
        # the reference has cycle and this cycle has been calculated on itself
        dic1 = dic['cycles']
        Ready = False
        dic2 = self.__dparam[ref]['cycles']
        if (dic2['reference'][idx] == ref and
                dic2['period_indexes'][idx] is not None):
            # We can take the reference as the base
            Ready = True
        # If there is no good reference
        # We calculate it and put
        if not Ready:
            self.findCycles(ref, idx)
            dic2 = self.__dparam[ref]['cycles']

        for key in ['period_indexes', 'period_T_intervals',
                    't_mean_cycle', 'period_T']:
            dic1[key][idx] = dic2[key][idx]

        tim = self.__dparam['time']['value'][:, idx]
        dic1['period_T_intervals'][idx] = [[tim[ids[0]], tim[ids[1]]]
                                           for ids in dic1['period_indexes'][idx]]
        dic1['t_mean_cycle'][idx] = [
            (t[0]+t[1])/2 for t in dic1['period_T_intervals'][idx]]
        dic1['period_T'][idx] = [
            (t[1]-t[0]) for t in dic1['period_T_intervals'][idx]]

        # Fill for each the characteristics
        values = dic['value'][:, idx]
        dic1['meanval'][idx] = [np.mean(values[ids[0]: ids[1]])
                                for ids in dic1['period_indexes'][idx]]
        dic1['medval'][idx] = [np.median(values[ids[0]: ids[1]])
                               for ids in dic1['period_indexes'][idx]]
        dic1['stdval'][idx] = [np.std(values[ids[0]: ids[1]])
                               for ids in dic1['period_indexes'][idx]]
        dic1['minval'][idx] = [np.amin(values[ids[0]: ids[1]])
                               for ids in dic1['period_indexes'][idx]]
        dic1['maxval'][idx] = [np.amax(values[ids[0]: ids[1]])
                               for ids in dic1['period_indexes'][idx]]

    def findCycles(self, refval, idx):
        '''
        Detect all positions of local maximums and the time that is linked
        '''
        # initialisation
        Periods = []
        id1 = 1

        dic1 = self.__dparam[refval]['cycles']
        val = self.__dparam[refval]['value'][:, idx]
        tim = self.__dparam['time']['value'][:, idx]
        # identification loop
        while id1 < len(val)-2:
            if (val[id1] > val[id1-1] and
                    val[id1] > val[id1+1]):
                Periods.append(1*id1)
            id1 += 1

        # Fill the formalism
        self.__dparam[refval]['cycles']['period_indexes'][idx] = [
            [Periods[i], Periods[i+1]] for i in range(len(Periods)-1)
        ]

        indexes = dic1['period_indexes'][idx]
        dic1 = self.__dparam[refval]['cycles']
        dic1['period_T_intervals'][idx] = [[tim[ids[0]], tim[ids[1]]]
                                           for ids in indexes]
        dic1['t_mean_cycle'][idx] = [
            (t[0]+t[1])/2 for t in dic1['period_T_intervals'][idx]]
        dic1['period_T'][idx] = [
            (t[1]-t[0]) for t in dic1['period_T_intervals'][idx]]
        dic1['reference'][idx] = refval
    # ##############################
    # reset
    # ##############################

    def reset(self):
        """ Re-initializes all variables

        Only the first time step (initial values) is preserved
        All other time steps are set to nan
        """

        # reset ode variables
        for k0 in self.lfunc:
            if k0 == 'time':
                self.__dparam[k0]['value'][0] = self.__dparam[k0]['initial']
                self.__dparam[k0]['value'][1:] = np.nan
            elif self.__dparam[k0]['eqtype'] == 'ode':
                self.__dparam[k0]['value'][0, :] = self.__dparam[k0]['initial']
                self.__dparam[k0]['value'][1:, :] = np.nan
            elif self.__dparam[k0]['eqtype'] == 'statevar':
                self.__dparam[k0]['value'][:, :] = np.nan

        # reset intermediary variables and auxiliary variables
        laux = self.get_dparam(eqtype='auxiliary', returnas=list)
        linter_aux = self.__dmisc['func_order'] + laux
        for k0 in linter_aux:
            # prepare dict of args
            kwdargs = {
                k1: v1[0, :]
                for k1, v1 in self.__dargs[k0].items()
            }
            # run function
            self.__dparam[k0]['value'][0, :] = (
                self.__dparam[k0]['func'](**kwdargs)
            )
            # set other time steps to nan
            self.__dparam[k0]['value'][1:, :] = np.nan

        # set run to False
        self.__dmisc['run'] = False

    # ##############################
    # %% Read-only properties
    # ##############################

    @ property
    def lfunc(self):
        """ List of parameters names that are actually functions """
        return [
            k0 for k0, v0 in self.__dparam.items()
            if v0.get('eqtype') is not None
        ]

    @ property
    def func_order(self):
        """ The ordered list of intermediary function names """
        return self.__dmisc['func_order']

    @ property
    def model(self):
        """ The model identifier """
        return self.__dmisc['model']

    @ property
    def dargs(self):
        return self.__dargs

    @ property
    def dmisc(self):
        return self.__dmisc

    @ property
    def dparam(self):
        return self.get_dparam(returnas=dict, verb=False)

    # ##############################
    # %%    data conversion
    # ##############################

    def _to_dict(self):
        """ Convert instance to dict """

        dout = {
            'dparam': self.get_dparam(returnas=dict, verb=False),
            'dmisc': dict(self.__dmisc),
            'dargs': dict(self.__dargs),
        }
        return dout

    @ classmethod
    def _from_dict(cls, dout=None):
        """ Create an instance from a dict """

        # --------------
        # check inputs
        c0 = (
            isinstance(dout, dict)
            and sorted(dout.keys()) == ['dargs', 'dmisc', 'dparam']
            and all([isinstance(dd, dict) for dd in dout.values()])
        )
        if not c0:
            msg = (
                "Arg dout must be a dict of the form:\n"
                "{'dargs': dict, 'dmisc': dict, 'dparams': dict}\n"
                f"You provided:\n{dout}"
            )
            raise Exception(msg)

        # -------------
        # reformat func from source
        for k0, v0 in dout['dparam'].items():
            if dout['dparam'][k0].get('func') is not None:
                dout['dparam'][k0]['func'] = eval(
                    f"lambda {dout['dparam'][k0]['source_kargs']}: "
                    f"{dout['dparam'][k0]['source_exp']}"
                )[0]

        # -------------------
        # create instance
        obj = cls(model=False)
        obj.__dparam = {k0: dict(v0) for k0, v0 in dout['dparam'].items()}
        obj.__dmisc = dict(dout['dmisc'])
        obj.__dargs = dict(dout['dargs'])

        return obj

    # ##############################
    # %%    saving methods
    # ##############################

    def save(self, path=None, name=None, fmt=None, verb=None):
        """ Save the instance

        Saved files are stored in path/fullname.ext
        The extension (ext) depends on the format (fmt) chosen for saving
        The file full name (fullname) is the concatenation of a base default
        name and a user-defined name.
            ex.: Output_MODELNAME_USERDEFINEDNAME.ext
        where MODELNAME is the model's name

        By default path is set to 'output/', but the user can overload it

        """

        return _saveload.save(
            self,
            path=path,
            name=name,
            fmt=fmt,
            verb=verb,
        )

    # ##############################
    #       replication methods
    # ##############################

    def copy(self):
        """ Return a copy of the instance """

        dout = self._to_dict()
        return self.__class__._from_dict(dout=dout)

    # ##############################
    #       comparison methods
    # ##############################

    def __eq__(self, other, verb=None, return_dfail=None):
        """ Automatically called when testing obj1 == obj2 """
        return _class_utility._equal(
            self, other,
            verb=verb,
            return_dfail=return_dfail,
        )

    # ##############################
    # %% Introspection
    # ##############################

    def __repr__(self):
        """ This is automatically called when only the instance is entered """
        col0 = ['model', 'nb. model param', 'nb. functions', 'run']
        ar0 = [
            self.__dmisc['model'],
            # list(self.__dmisc['model'].values())[0],
            len([
                k0 for k0, v0 in self.__dparam.items()
                if v0.get('func') is None
            ]),
            len(self.lfunc),
            self.__dmisc['run'],
        ]
        return _utils._get_summary(
            lar=[ar0],
            lcol=[col0],
            verb=False,
            returnas=str,
        )

    def get_summary(self, idx=0):
        """
        Print a str summary of the solver

        """

        # ----------
        # Numerical parameters
        col0 = ['Numerical param.', 'value', 'units', 'definition', 'comment']
        ar0 = [
            tuple([
                k0,
                str(v0['value']),
                str(v0['units']),
                v0.get('definition', ' '),
                v0.get('com', ' ')
            ])
            for k0, v0 in self.__dparam.items() if
            (v0['group'] == 'Numerical' and k0 != 'time')
        ]

        # ----------
        # parameters
        col1 = ['Model param.', 'value', 'units', 'group',
                'definition', 'comment']
        ar1 = [
            tuple([
                k0,
                str(v0['value']),
                str(v0['units']),
                v0['group'],
                v0.get('definition', ' '),
                v0.get('com', ' ')
            ])
            for k0, v0 in self.__dparam.items()
            if v0['group'] != 'Numerical'
            and v0.get('func') is None
        ]

        # ----------
        # functions
        if self.__dmisc['run']:
            col2 = ['function', 'source', 'initial',
                    'final', 'units', 'eqtype',
                    'definition', 'comment']
            ar2 = [
                tuple([
                    k0,
                    v0['source_exp'],
                    "{:.2e}".format(v0.get('value')[0, idx]),
                    "{:.2e}".format(v0.get('value')[-1, idx]),
                    str(v0['units']),
                    v0['eqtype'].replace('intermediary', 'inter').replace(
                        'auxiliary', 'aux',
                    ),
                    v0.get('definition', ' '),
                    v0.get('com', ' '),
                ])
                for k0, v0 in self.__dparam.items()
                if v0.get('func') is not None
            ]
        else:
            col2 = ['function', 'source', 'initial',
                    'units', 'eqtype', 'definition', 'comment']
            ar2 = [
                tuple([
                    k0,
                    v0['source_exp'],
                    "{:.2e}".format(v0.get('value')[0, idx]),
                    str(v0['units']),
                    v0['eqtype'].replace('intermediary', 'inter').replace(
                        'auxiliary', 'aux',
                    ),
                    v0.get('definition', ' '),
                    v0.get('com', ' '),
                ])
                for k0, v0 in self.__dparam.items()
                if v0.get('func') is not None
            ]
        # ----------
        # format output
        return _utils._get_summary(
            lar=[ar0, ar1, ar2],
            lcol=[col0, col1, col2],
            verb=True,
            returnas=False,
        )

    # ##############################
    # variables
    # ##############################

    def get_variables_compact(self, eqtype=None):
        """ Return a compact numpy arrays containing all variable

        Return
            - compact np.ndarray of all variables
            - list of variable names, in the same order
            - array of indices
        """
        # check inputs
        leqtype = ['ode', 'intermediary', 'auxiliary']
        if eqtype is None:
            eqtype = ['ode', 'intermediary']
        if isinstance(eqtype, str):
            eqtype = [eqtype]
            if any([ss not in leqtype for ss in eqtype]):
                msg = (
                    f"eqtype must be in {leqtype}\n"
                    f"You provided: {eqtype}"
                )
                raise Exception(msg)

        # list of keys of variables
        keys = np.array([
            k0 for k0, v0 in self.__dparam.items()
            if v0.get('eqtype') in leqtype
        ], dtype=str)

        # get compact variable array
        variables = np.swapaxes([
            self.__dparam[k0]['value'] for k0 in keys
        ], 0, 1)

        return keys, variables

    def get_dparam(self, verb=None, returnas=None, **kwdargs):
        """ Return a copy of the input parameters dict

        Return as:
            - dict: dict
            - 'DataGFrame': a pandas DataFrame
            - np.ndarray: a dict of np.ndarrays
            - False: return nothing (useful of verb=True)

        verb:
            - True: pretty-print the chosen parameters
            - False: print nothing
        """
        lcrit = ['dimension', 'units', 'type', 'group', 'eqtype']
        lprint = [
            'parameter', 'value', 'units', 'dimension', 'symbol',
            'type', 'eqtype', 'group', 'comment',
        ]

        return _class_utility._get_dict_subset(
            indict=self.__dparam,
            verb=verb,
            returnas=returnas,
            lcrit=lcrit,
            lprint=lprint,
            **kwdargs,
        )

    def get_presets(self, returnas=False,):
        '''
        Will print the presets, or give the list, or the full dictionnary
        '''
        if returnas is False:
            print(self.__dmisc['preset'])
        if returnas == list:
            return self.__dmisc['preset'].keys()
        if returnas == dict:
            return self.__dmisc['preset']

    def set_preset(self, name, verb=False):
        if name not in self.__dmisc['preset'].keys():
            raise Exception(name+' is not a known preset')

        preset = self.__dmisc['preset'][name]
        self.Change_Attributes(preset['fields'])
        self.Plot = preset['plots']
        if verb:
            print('Preset', name, 'loaded')
            print(preset['com'])
