# -*- coding: utf-8 -*-

# %% Importations ###########

# built-in
import copy


# Common
import numpy as np


# Library-specific
from .__config import _FROM_USER
from .__config import _DEFAULTSIZE
from .__config import _VERB
from ._utilities import _utils, _class_checks, _class_utility, _cn
from ._utilities import _class_set
from ._utilities import _Network
from ._utilities import _solvers, _saveload
from ._plots._plots import _DPLOT


class Hub():
    """
    MOST IMPORTANT OBJECT FOR THE USER.
    given a model name, it will load it and get its logics, presets and associated values.
    It will :
        * identify what are the parameters, the state variables, the differential variables
        * find their associated properties (definition, units, values)
        * find an order of calculation

    You then access to fields value modification, the structure and properties in the model,
    simulation, plots, deeper analysis...

    INPUTS :
    * model : STRING containing the model name
    * from_user : BOOLEAN if you want to use your file (True) or the one provided in pygemmes (False)
    * preset : DICTIONNARY name of the preset in the actual dictionnary of preset
    * dpreset : DICTOFDICTOFDIC a dictionnary of preset one can use (see model creation)
    * verb : BOOLEAN True for print in terminal

    model files are named _model_<model-name>.py

    A number of pre-defined models are available from the library,
        see pgm.get_available_models() to get a list

    All pre-defined model files are copied into your $HOME/.pygemmes/
        folder so you can:
            - edit them to change some parameters
            - create new model files that will be accessible to pygemmes
    You can use them using `from_user=True'
    """

    def __init__(
        self,
        model,
        from_user=_FROM_USER,
        preset=None,
        dpresets=None,
        verb=_VERB,
    ):

        # Initialize the hub main dictionnaries ###############################
        # Contains miscellaneous, practical informations
        self.__dmisc = {'run': False,
                        'dmulti': {},
                        'cycles': False,
                        'derivative': False,
                        }

        # Load model files ####################################################
        (
            self.__dmodel,  # Contains the model informations
            self.__dparam,  # Contains all the fields and their relative properties
            self.__dmisc['dfunc_order'],
            self.__dargs,  # Pointer for each field and function values
        ) = _class_set.load_model(
            model,
            from_user=from_user,
            verb=verb,
        )

        # Actualize the shape
        self.__dmisc['dmulti']['NxNr'] = (self.__dparam['nx']['value'],
                                           self.__dparam['nr']['value'])
        self.__dmisc['dmulti']['scalar']= []
        self.__dmisc['dmulti']['vector'] = []
        self.__dmisc['dmulti']['matrix'] = []
        for k,v in self.dparam.items():
            size = v.get('size',[_DEFAULTSIZE])
            if size[0]== _DEFAULTSIZE:
                self.__dmisc['dmulti']['scalar'].append(k)
            elif len(size)==1:
                self.__dmisc['dmulti']['vector'].append(k)
            else:
                self.__dmisc['dmulti']['matrix'].append(k)
        if len(self.__dmisc['dmulti']['vector']+self.__dmisc['dmulti']['matrix']):
            self.dmisc['multisectoral'] = True
        else:
            self.dmisc['multisectoral'] = False
        # update from preset if relevant ######################################
        if preset is not None:
            self.set_preset(preset=preset, dpresets=dpresets, verb=verb)
        else:
            self.reset()

    # ##############################
    # %% Setting / getting parameters
    # ##############################

    def set_preset(self, preset, dpresets=None, verb=False):
        """
        Simpler version of set_dparam with just preset
        """

        (self.__dparam,
         self.__dmisc['dmulti'],
         self.__dargs) = _class_checks.update_from_preset(
            dparam=self.__dparam,
            dmodel=self.__dmodel,
            preset=preset,
            dpresets=dpresets,
            verb=verb,
        )

        self.reset()

    def set_dparam(
        self,
        dparam=None,
        preset=None,
        dpresets=None,
        key=None,
        value=None,
        verb=False,
        **kwdargs,
    ):
        """ Set the dict of input parameters (dparam) or a single param

        dparam is the large dictionary that contains:
            - fixed-value parameters
            - functions of different types (equations)

        You can provide:
            - dparam as a dict
                => will re-initialize the parameters
            - preset as a str refering to an existing preset
                => will re-initialize the parameters
            - only a (key, value) pair to change an single existing parameter
                => will change a single existing parameter value
            - a dict of existing parameters, provided with the **kwdargs syntax
                => will change all desired existing parameter values

        Typical usage
        -------------
            >>> dparam = {'alpha': 0, 'beta': 1}
            >>> hub.set_dparam(dparam=dparam)

            >>> hub = pgm.Hub('GK-Reduced')
            >>> hub.set_dparam(preset='default')

            # The following 2 syntaxes are equivalent to set a single parameter
            >>> hub.set_dparam(key='alpha', value=0)    # syntax 1
            >>> hub.set_dparam(alpha=0.1)                 # syntax 2

            # The following syntax allows to change several existing parameters
            >>> dparam_changes = {'alpha': 0., 'delta': 0.}
            >>> hub.set_dparam(**dparam_changes)
        """

        if preset != None:
            print('WARNING : USE set_dpreset() this will be removed later')
            (self.__dparam,
             self.__dmisc['dfunc_order'],
             self.__dargs,
             ) = _class_checks.update_from_preset(
                dparam=self.__dparam,
                dmodel=self.__dmodel,
                preset=preset,
                dpresets=dpresets,
                verb=verb,
            )
        else:
            # Check input: dparam xor (key, value)
            lc = [
                dparam is not None,
                preset is not None,
                key is not None and value is not None,
                len(kwdargs) > 0,
            ]
            if np.sum(lc) != 1:
                lstr = [
                    '\t- {}: {}'.format(kk, vv)
                    for kk, vv in [
                        ('dparam', dparam),
                        ('preset', preset),
                        ('key', key), ('value', value),
                        ('kwdargs', kwdargs),
                    ]
                ]
                msg = (
                    "Provide dparam xor preset xor (key, value) xor kwdargs!\n"
                    "You provided:\n"
                    + "\n".join(lstr)
                )
                raise Exception(msg)

            # ----------------
            # set dparam or update desired key

            if preset is not None:
                if key is not None:
                    _class_checks._set_key_value(
                        dparam=self.__dparam,
                        key=key,
                        value=value,
                    )
                    dparam = self.__dparam

                elif len(kwdargs) > 0:
                    for kk, vv in kwdargs.items():
                        if not isinstance(vv, dict):
                            vv = {'value': vv, 'grid': False}
                        _class_checks._set_key_value(
                            dparam=self.__dparam,
                            key=kk,
                            value=vv['value'],
                        )
                    dparam = self.__dparam

                # ----------------
                # Update to check consistency

                (
                    self.__dparam,
                    self.__dmisc['dmulti'],
                    self.__dmisc['dfunc_order'],
                    self.__dargs,
                ) = _class_checks.check_dparam(
                    dparam=dparam,
                    verb=verb,
                )

            # reset all variables (keep only the first time step)
        self.reset()

    def get_dparam(self, condition=None, verb=None, returnas=dict, **kwdargs):
        """ Return a copy of the input parameters dict that you can filter

        Return as:
            - dict: dict
            - 'DataGFrame': a pandas DataFrame
            - np.ndarray: a dict of np.ndarrays
            - False: return nothing (useful of verb=True)

        verb:
            - True: pretty-print the chosen parameters
            - False: print nothing

        lcrit = ['key', 'dimension', 'units', 'type', 'group', 'eqtype','isneeded']

        """
        lcrit = ['key', 'dimension', 'units',
                 'type', 'group', 'eqtype', 'isneeded']
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
            condition=condition,
            **kwdargs,
        )

    def get_dparam_as_reverse_dict(
        self,
        crit=None,
        returnas=None,
        verb=None,
        **kwdargs,
    ):
        """ Return/prints a dict of units/eqtype... with a list of keys

        if crit = 'units', return a dict with:
            - keys: the unique possible values of field 'units'
            - values: for each unique unit, the corresponding list of keys

        lcrit = ['dimension', 'units', 'type', 'group', 'eqtype']

        Restrictions on the selection can be imposed by **kwdargs
        The selection is done using self.get_dparam() (single-sourced)
        """

        # -------------
        # check input

        if verb is None:
            verb = False
        if returnas is None:
            returnas = dict if verb is False else False

        lcrit = ['dimension', 'units', 'type', 'group', 'eqtype']
        if crit not in lcrit:
            msg = (
                f"Arg crit must be in: {lcrit}\n"
                f"Provided: {crit}"
            )
            raise Exception(msg)

        if crit in kwdargs.keys():
            msg = (
                "Conflict detected!:\n"
                f"{crit} is the sorting criterion => not usable for selection!"
            )
            raise Exception(msg)

        # -------------
        # create dict

        lunique = set([v0.get(crit) for v0 in self.__dparam.values()])
        dout = {
            k0: self.get_dparam(returnas=list, **{crit: k0, **kwdargs})
            for k0 in lunique
        }

        # -------------
        # print and/or return

        if verb is True:
            lstr = [f'\t- {k0}: {v0}' for k0, v0 in dout.items()]
            msg = (
                "The following selection has been identified:\n"
                + "\n".join(lstr)
            )
            print(msg)

        if returnas is dict:
            return dout

    # ##############################
    # %% Read-only properties
    # ##############################

    @property
    def dfunc_order(self):
        """ The ordered list of intermediary function names """
        return self.__dmisc['dfunc_order']

    @property
    def dmodel(self):
        """ The model identifiers """
        return self.__dmodel

    @property
    def dargs(self):
        return self.__dargs

    @property
    def dparam(self):
        return self.get_dparam(returnas=dict, verb=False)

    @property
    def dmisc(self):
        return self.__dmisc

    # ##############################
    # reset
    # ##############################

    def reset(self):
        """ Re-initializes all variables

        Only the first time step (initial values) is preserved
        All other time steps are set to nan
        """

        # reset ode variables
        for k0 in self.get_dparam(eqtype=['differential', 'statevar'], returnas=list):
            self.__dparam[k0]['value'][...] = np.nan

        # Reset initial for ode
        for k0 in self.get_dparam(eqtype=['differential'], returnas=list):
            self.__dparam[k0]['value'][0, ...] = self.__dparam[k0]['initial']

        # recompute initial value for function-parameters
        pstate = self.__dmisc['dfunc_order']['parameter']
        for k0 in pstate:
            dargs = {
                k1: self.__dparam[k1]['value']
                for k1 in self.__dparam[k0]['args'][None]
            }
            dargs.update({
                k1: self.__dparam[k1]['value']
                for k1 in self.__dparam[k0]['args']['parameter']
            })
            self.__dparam[k0]['value'] = self.__dparam[k0]['func'](**dargs)

        # recompute inital value for statevar
        lstate = self.__dmisc['dfunc_order']['statevar']
        for k0 in lstate:
            # prepare dict of args
            kwdargs = {
                k1: v1[0, ...]
                for k1, v1 in self.__dargs[k0].items()
            }
            # run function
            self.__dparam[k0]['value'][0, ...] = (
                self.__dparam[k0]['func'](**kwdargs)
            )

        # set run to False
        self.__dmisc['run'] = False

    def reinterpolate_dparam(self, N=100):
        """
        If the system has run, takes dparam and reinterpolate all values.
        Typical use is to have lighter plots

        DO NOT WORK WELL WITH GRID
        NEED A RESET BEFORE A RUN TO REALLOCATE SPACE

        Parameters
        ----------
        Npoints : TYPE, optional
            DESCRIPTION. The default is 100.
        """

        P = self.__dparam
        t = P['time']['value']
        for k in self.__dmisc['dfunc_order']['statevar']+self.__dmisc['dfunc_order']['differential']:
            v = P[k]['value']

            newval = np.zeros([N]+list(self.__dmisc['dmulti']['shape']))
            newt = np.linspace(t[0], t[-1], N)

            for i in range(np.shape(newval)[1]):
                newval[:, i] = np.interp(newt[:, i], t[:, i], v[:, i])
            self.__dparam[k]['value'] = newval

    # ##############################
    #  Introspection
    # ##############################

    def __repr__(self, verb=None):
        """ This is automatically called when only the instance is entered """

        if verb is None:
            verb = True

        col0 = [
            'model',
            'preset',
            'param (fix + func)',
            'differential',
            'statevar',
            'run',
            'source',
        ]

        ar0 = [
            self.__dmodel['name'],
            self.__dmodel['preset'],
            '{} + {}'.format(
                len(self.get_dparam(returnas=list, eqtype=None))-1,
                len(self.get_dparam(returnas=list, eqtype='parameter'))-1,
            ),
            len(self.get_dparam(returnas=list, eqtype='differential'))-1,
            len(self.get_dparam(returnas=list, eqtype='statevar')),
            self.__dmisc['run'],
            self.__dmodel['file'],
        ]
        if verb is True:
            return _utils._get_summary(
                lar=[ar0],
                lcol=[col0],
                verb=False,
                returnas=str,
            )
        else:
            return col0, ar0

    def get_summary(self, idx=(0, 0, 0)):
        """
        INTROSPECTION TOOL :
        Print a str summary of the model, with
        * Model description
        * Parameters, their properties and their values
        * ODE, their properties and their values
        * Statevar, their properties and their values

        For more precise elements, you can do introspection using hub.get_dparam()

        INPUT :
        * idx = index of the model you want the value to be shown when there are multiple models in parrallel
        """

        _FLAGS = ['run', 'cycles', 'derivative']
        _ORDERS = ['statevar', 'differential', 'parameters']

        print(50 * '#', 'SUMMARY', 50 * '#')
        print('Model       :', self.dmodel['name'])
        print('Description :', self.dmodel['description'])
        print('File        :', self.dmodel['file'])
        print(20 * '#', 'Fields', 20 * '#')
        for o in _ORDERS:
            print(o.ljust(15), str(len(self.dmisc['dfunc_order'][o])).zfill(3), self.dmisc['dfunc_order'][o])
        print(20 * '#', 'Presets', 20 * '#')
        for k, v in self.dmodel['presets'].items():
            print('    ', k.ljust(20), v['com'])
        print(20 * '#', 'Flags', 20 * '#')
        for f in _FLAGS:
            print(f.ljust(15) + ':', self.dmisc[f])
        print('\n')

        print(30*'#', 'Indexes :', idx, 30*'#')

        # ----------
        # Numerical parameters
        col1, ar1 = _class_utility._get_summary_numerical(self)

        # ----------
        # parameters
        col2, ar2 = _class_utility._get_summary_parameters(self, idx=idx)

        # ----------
        # functions ODE
        col3, ar3 = _class_utility._get_summary_functions(
            self, idx=idx, eqtype=['differential'], isneeded=True)

        # ----------
        # functions Statevar
        col4, ar4 = _class_utility._get_summary_functions(
            self, idx=idx, eqtype=['statevar'], isneeded=True)

        # ----------
        # functions ODE
        col5, ar5 = _class_utility._get_summary_functions(
            self, idx=idx, eqtype=['differential'], isneeded=False)

        # ----------
        # functions Statevar
        col6, ar6 = _class_utility._get_summary_functions(
            self, idx=idx, eqtype=['statevar'], isneeded=False)

        # ----------
        # format output
        return _utils._get_summary(
            lar=[ar0, ar1, ar2, ar3, ar4, ar5, ar6],
            lcol=[col0, col1, col2, col3, col4, col5, col6],
            verb=True,
            returnas=False,
        )

    def get_equations_description(self):
        '''
        Gives a full description of the model and its equations, closer to what one
        would expect in an article.
        get_Network to get the interactive version
        '''

        print('############# DIFFERENTIAL EQUATIONS ###########')
        for key in self.__dmisc['dfunc_order']['differential']:
            v = self.dparam[key]
            print('### ', key, ' ###########')
            print('Units        :', v['units'])
            print('Equation     :', f'd{key}/dt=', v['source_exp'].replace(
                'itself', key).replace('lamb', 'lambda'))
            print('definition   :', v['definition'])
            print('units        :', v['units'])
            print('Comment      :', v['com'])
            print('Dependencies :')
            for key2 in [v2 for v2 in v['kargs'] if v2 != 'itself']:
                v1 = self.dparam[key2]
                print('    ', key2, (8-len(key2))*' ',
                      v1['units'], (8-len(v1['units']))*' ', v1['definition'])
            print(' ')
        print('######### STATE VARIABLES EQUATIONS ###########')
        for key in self.__dmisc['dfunc_order']['statevar']:
            v = self.dparam[key]
            print('### ', key, ' ###########')
            print('Units        :', v['units'])
            print('Equation     :', f'{key}=', v['source_exp'].replace(
                'itself', key).replace('lamb', 'lambda'))
            print('definition   :', v['definition'])
            print('Comment      :', v['com'])
            print('Dependencies :')
            for key2 in [v2 for v2 in v['kargs'] if v2 != 'itself']:
                v1 = self.dparam[key2]
                print('    ', key2, (8-len(key2))*' ',
                      v1['units'], (8-len(v1['units']))*' ', v1['definition'])
            print(' ')
            print(' ')

    def get_Network(self,
                    filters=(),
                    auxilliary=False,
                    screensize=1080,
                    custom=True,
                    params=False):
        _Network.Network_pyvis(self,
                               filters=filters,
                               auxilliary=auxilliary,
                               screensize=screensize,
                               custom=custom,
                               plot_params=params)

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
        """ Run the simulation, with any of the solver existing in :
            - pgm.get_available_solvers(returnas=list)
            Verb will have the following behavior :
            - none no print of the step
            - 1 at every step
            - any float (like 1.1) the iteration is written at any of these value

        Compute each time step from the previous one using:
            - parameters
            - differentials (ode)
            - intermediary functions in specified func_order

        """
        # ------------
        # check inputs
        dverb = _class_checks._run_verb_check(verb=verb)

        # ------------
        # reset variables
        self.reset()

        # time vector
        nt = self.__dparam['nt']['value']

        # ------------
        # temporary dict of input
        lode = self.__dmisc['dfunc_order']['differential']
        lstate = self.__dmisc['dfunc_order']['statevar']
        # laux = []

        # ------------
        # start time loop

        try:
            solver = _solvers.solve(
                solver=solver,
                dparam=self.__dparam,
                dmulti=self.__dmisc['dmulti'],
                lode=lode,
                lstate=lstate,
                dargs=self.__dargs,
                nt=nt,
                rtol=rtol,
                atol=atol,
                max_time_step=max_time_step,
                dverb=dverb,
            )
            self.__dmisc['run'] = True
            self.__dmisc['solver'] = solver

        except Exception as err:
            self.__dmisc['run'] = False
            raise err

    # ##############################
    #       Deep analysis methods
    # ##############################

    def calculate_variation_rate(self, epsilon=0.0001):
        '''
        Calculate all derivatives :
            * time derivative
            * time log_derivative (variation rate)
            * partial_derivatives (gradient on the other variables)
            * partial_contribution (partial_derivatives time the respective time derivate)

        partial derivative is associating to field Y a dic as {X : dY/dX} for each statevar

        accessible in :
            dparam[key]['time_derivate']
            dparam[key]['time_log_derivate']
            dparam[key]['partial_derivatives']
            dparam[key]['partial_contribution']
        '''

        R = self.__dparam

        varlist = self.dmisc['dfunc_order']['statevar'] + \
            self.dmisc['dfunc_order']['differential']

        varlist.remove('time')

        for k in varlist:
            R[k]['time_derivate'] = np.gradient(
                R[k]['value'], axis=0)/R['dt']['value']
            R[k]['time_log_derivate'] = R[k]['time_derivate']/R[k]['value']

            if R[k]['eqtype'] == 'differential':
                R[k]['time_dderivate'] = np.gradient(
                    R[k]['time_derivate'], axis=0)/R['dt']['value']
            # SENSITIVITY CALCULATION
            func = R[k]['func']
            args = R[k]['args']['differential']+R[k]['args']['statevar']
            if 'itself' in R[k]['kargs']:
                args += k

            argsV = {k2: R[k2]['value'] for k2 in args}

            if 'lambda' in args:
                argsV['lamb'] = argsV['lambda']
                del argsV['lambda']
                args += ['lamb']
                args.remove('lambda')
            if k in args:
                argsV['itself'] = argsV[k]
                del argsV[k]
                args += ['itself']
                args.remove(k)

            R[k]['partial_derivatives'] = {}
            for k2 in args:
                argTemp = copy.deepcopy(argsV)
                argTemp[k2] += epsilon
                if k2 == 'lamb':
                    k2 = 'lambda'
                if k2 == 'itself':
                    k2 = k
                R[k]['partial_derivatives'][k2] = (
                    func(**argTemp)-func(**argsV))/epsilon

        # Contribution of partial derivatives
        for k in varlist:
            R[k]['partial_contribution'] = {k2: R[k]['partial_derivatives'][k2]
                                            * R[k2]['time_derivate']
                                            for k2 in R[k]['partial_derivatives'].keys()}
        self.__dmisc['derivative'] = True

    def calculate_Cycles(self, ref=None, n=10):
        '''
        This function is a wrap-up on GetCycle to do it on all variables.

        For each variables, it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself

        n : int, number of harmonics calculated in fourier decomposition
        '''

        leq = ['differential', 'statevar']
        fields = ['reference',
                  'period_indexes',
                  'period_T_intervals',
                  't_mean_cycle',
                  'period_T',
                  'meanval',
                  'medval',
                  'stdval',
                  'minval',
                  'maxval']
        Nsys = self.dmisc['dmulti']['shape'][0]

        for var, dic1 in self.get_dparam(returnas=dict, eqtype=leq).items():
            self.__dparam[var]['cycles'] = [{k: []
                                             for k in fields} for i in range(Nsys)]

        for var, dic1 in self.get_dparam(returnas=dict, eqtype=leq).items():
            for idx in range(Nsys):
                if ref is None:
                    self.__dparam[var]['cycles'][idx]['reference'] = var
                    self._FillCycles(var, var, idx, n=n)
                else:
                    self.__dparam[var]['cycles'][idx]['reference'] = ref
                    self._FillCycles(var, ref, idx, n=n)

        self.reverse_cycles_dic()
        self.__dmisc['cycles'] = True

    def _FillCycles(self, var, ref='lambda', id=0, n=10):
        '''
        it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself

        var : name of the variable we are working on
        ref : reference for the oscillations detections
        '''

        # Get the new dictionnary to edit
        dic = self.__dparam[var]
        dic1 = self.__dparam[var]['cycles'][id]

        # check if reference has already calculated its period
        # the reference has cycle and this cycle has been calculated on itself
        ready = False
        if 'cycles' in self.__dparam[ref].keys():
            dic2 = self.__dparam[ref]['cycles'][id]
            if (dic2['reference'] == ref and 'period_indexes' in dic2):
                # We can take the reference as the base
                ready = True
        # If there is no good reference
        # We calculate it and put
        if not ready:
            self._findCycles(ref, id)
            dic2 = self.__dparam[ref]['cycles'][id]

        for key in ['period_indexes', 'period_T_intervals',
                    't_mean_cycle', 'period_T']:
            dic1[key] = copy.deepcopy(dic2[key])

        tim = self.__dparam['time']['value']
        dic1['period_T_intervals'] = [[tim[idx[0], 0], tim[idx[1], 0]]
                                      for idx in dic1['period_indexes']]
        dic1['t_mean_cycle'] = [
            (t[0] + t[1]) / 2 for t in dic1['period_T_intervals']]
        dic1['period_T'] = [
            (t[1] - t[0]) for t in dic1['period_T_intervals']]
        dic1['frequency'] = [
            1/(t[1] - t[0]) for t in dic1['period_T_intervals']]

        # Fill for each the characteristics
        values = dic['value'][:, id]
        # print(var, dic1)
        dic1['meanval'] = [np.mean(values[idx[0]:idx[1]])
                           for idx in dic1['period_indexes']]
        dic1['medval'] = [np.median(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]
        dic1['stdval'] = [np.std(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]
        dic1['minval'] = [np.amin(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]
        dic1['maxval'] = [np.amax(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]

        # print([values[idx[0]:idx[1]] for idx in dic1['period_indexes']])

        Coeffs = [_cn(values[idx[0]:idx[1]], n)
                  for idx in dic1['period_indexes']]
        dic1['Coeffs'] = [Coeffs[i][1:]/Coeffs[i][1]
                          for i in range(len(Coeffs))]
        dic1['Harmonicity'] = [np.sum(Coeffs[i][1:]**2)/np.sum(Coeffs[i]**2)
                               for i in range(len(Coeffs))]

    def _findCycles(self, refval, idx=0):
        '''
        Detect all positions of local maximums and the time that is linked
        '''
        # initialisation
        periods = []
        id1 = 1

        dic1 = self.__dparam[refval]['cycles'][idx]
        val = self.__dparam[refval]['value'][:, idx]

        # identification loop
        while id1 < len(val) - 2:
            if (val[id1] > val[id1 - 1] and
                    val[id1] > val[id1 + 1]):
                periods.append(1 * id1)
            id1 += 1

        # Fill the formalism
        self.__dparam[refval]['cycles'][idx]['period_indexes'] = [
            [periods[i], periods[i + 1]] for i in range(len(periods) - 1)
        ]
        tim = self.__dparam['time']['value']
        dic1 = self.__dparam[refval]['cycles'][idx]
        dic1['period_T_intervals'] = [[tim[idx[0]], tim[idx[1]]]
                                      for idx in dic1['period_indexes']]
        dic1['t_mean_cycle'] = [
            (t[0] + t[1]) / 2 for t in dic1['period_T_intervals']]
        dic1['period_T'] = [
            (t[1] - t[0]) for t in dic1['period_T_intervals']]
        dic1['reference'] = refval

    def reverse_cycles_dic(self):
        leq = ['differential', 'statevar']
        for var, dic1 in self.get_dparam(returnas=dict, eqtype=leq).items():
            c = dic1['cycles']
            newcycles = {k: [] for k in c[0].keys()}
            for i in range(len(c)):
                for k in c[i].keys():
                    newcycles[k].append(c[i][k])

            self.__dparam[var]['cycles_bykey'] = copy.deepcopy(newcycles)

    # ##############################
    #       Multiple run stats
    # ##############################

    def calculate_StatSensitivity(self):
        '''
        When there are multiple run in parrallel, will associate to each variable
        a dict 'sensibility' in dparam, with statistical measures

        Do not use with grid=True
        '''
        R = self.__dparam
        keys = [k for k in R.keys() if R[k].get(
            'eqtype', 'parameter') != 'parameter']

        for ke in keys:
            R[ke]['sensitivity'] = {}

            val = R[ke]['value']

            V = R[ke]['sensitivity']
            V['mean'] = np.mean(val, axis=1)
            V['stdv'] = np.std(val, axis=1)
            V['min'] = np.amin(val, axis=1)
            V['max'] = np.amax(val, axis=1)
            V['median'] = np.median(val, axis=1)
        self.__dmisc['sensitivity'] = True

    # ##############################
    #       Convergence toward a point
    # ##############################
    def calculate_ConvergeRate(self, finalpoint):
        '''
        Will calculate how the evolution of the distance of each trajectory to
        the final point.
        Then, it fit the trajectory with an exponential, and return the rate
        of decrease of this exponential (the bigger the more stable).

        finalpoint has to be :
            { 'field1' : number1,
              'field2' : number2,
              'field3' : number3}
        '''
        # Final step studies ##################
        R = self.get_dparam(
            key=[k for k in finalpoint]+['time'], returnas=dict)
        Coords = [R[k]['value']-finalpoint[k] for k in finalpoint.keys()]
        dist = np.linalg.norm(Coords, axis=0)
        t = R['time']['value'][:, 0]

        # Fit using an exponential ############
        Nsys = self.dmisc['dmulti']['shape'][0]
        ConvergeRate = np.zeros(Nsys)
        for i in range(Nsys):
            if (np.isnan(np.sum(dist[:, i])) or np.isinf(np.sum(dist[:, i]))):
                ConvergeRate[i] = -np.inf
            else:
                fit = np.polyfit(t,
                                 np.log(dist[:, i]),
                                 1,
                                 w=np.sqrt(dist[:, i]))
                ConvergeRate[i] = -fit[0]
        return ConvergeRate

    # ##############################
    #       plotting methods
    # ##############################

    def plot_preset(self, preset=None):
        '''
        Automatically plot all functions that are defined in _plot.py, associated with the preset

        If a preset is loaded, you do not need to precise it when using the function
        If no preset is loaded, you can try to plot its associated plots by calling it.
        '''

        if preset is None:
            preset = self.dmodel['preset']
        tempd = self.dmodel['presets'][preset]['plots']

        for plot, funcplot in _DPLOT.items():
            for argl in tempd.get(plot, []):
                funcplot(self, **argl)

    def plot(
        self,
        mode=False,
        # for forcing a color / label
        color=None,
        label=None,
        # for figure creation
        dax=None,
        ncols=None,
        sharex=None,
        tit=None,
        wintit=None,
        dmargin=None,
        fs=None,
        dleg=None,
        show=None,
        # for selection of data
        idx=None,
        eqtype=None,
        **kwdargs,
    ):
        """
        Launch the basic plot: time traces
        """

        # -------------
        # check inputs

        idx = _class_checks._check_idx(
            idx=idx,
            nt=self.__dparam['nt']['value'],
            dmulti=self.__dmisc.get('dmulti'),
        )

        return _DPLOT['timetrace'](
            self,
            mode=mode,
            # for forcing a color / label
            color=color,
            label=label,
            # for figure creation
            dax=dax,
            ncols=ncols,
            sharex=sharex,
            tit=tit,
            wintit=wintit,
            dmargin=dmargin,
            fs=fs,
            dleg=dleg,
            show=show,
            # for selection of data
            idx=idx,
            eqtype=eqtype,
            **kwdargs,

        )

    # ##############################
    #       data conversion
    # ##############################

    def _to_dict(self):
        """ Convert instance to dict """

        dout = {
            'dmodel': copy.deepcopy(self.__dmodel),
            'dparam': self.get_dparam(returnas=dict, verb=False),
            'dmisc': copy.deepcopy(self.__dmisc),
            'dargs': copy.deepcopy(self.__dargs),
        }
        return dout

    @classmethod
    def _from_dict(cls, dout=None, model_file=None):
        """ Create an instance from a dict """

        # --------------
        # check inputs
        c0 = (
            isinstance(dout, dict)
            and sorted(dout.keys()) == ['dargs', 'dmisc', 'dmodel', 'dparam']
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
        # rebuild all functions from source, if necessary
        c0 = any([
            v0.get('source_kargs') is not None
            and not hasattr(v0.get('func'), '__call__')
            for k0, v0 in dout['dparam'].items()
        ])
        if c0:
            _saveload.rebuild_func_from_source(dout, model_file=model_file)

        # -------------------
        # create instance
        obj = cls()
        obj.__dmodel = dict(dout['dmodel'])
        obj.__dparam = {k0: dict(v0) for k0, v0 in dout['dparam'].items()}
        obj.__dmisc = dict(dout['dmisc'])
        obj.__dargs = dict(dout['dargs'])

        # update default args for functions
        _class_checks._update_func_default_kwdargs(
            lfunc=obj.get_dparam(returnas=list, eqtype=(None,)),
            dparam=obj.__dparam,
            dmulti=obj.__dmisc['dmulti'],
        )

        # re-pass dargs by reference
        obj.__dargs = _class_checks.get_dargs_by_reference(
            obj.__dparam,
            dfunc_order=obj.__dmisc['dfunc_order'],
        )

        return obj

    # ##############################
    #       saving methods
    # ##############################

    def save(self, path=None, name=None, fmt=None, verb=None, returnas=None):
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
            returnas=returnas,
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

    def __eq__(
        self,
        other,
        atol=None,
        rtol=None,
        verb=None,
        return_dfail=None,
    ):
        """ Automatically called when testing obj1 == obj2 """
        return _class_utility._equal(
            self, other,
            atol=atol,
            rtol=rtol,
            verb=verb,
            return_dfail=return_dfail,
        )
