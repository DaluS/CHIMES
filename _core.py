# -*- coding: utf-8 -*-

# %% Importations ###########

# built-in
import time


# Common
import numpy as np


# Library-specific
from utilities import _utils, _class_checks, _class_utility
from utilities import _solvers, _saveload
import _plots as plots


class Hub():
    """ Generic class
    """

    def __init__(self, model=None, preset=None):
        self.__dparam = {}
        self.__dmodel = dict.fromkeys(
            ['name', 'file', 'description', 'presets', 'preset']
        )
        self.__dmisc = dict.fromkeys(['dfunc_order', 'run', 'solver'])
        self.__dargs = {}
        if model is not None:
            self.load_model(model, preset=preset)

    # ##############################
    # %% Setting / getting parameters
    # ##############################

    def load_model(self, model=None, preset=None):
        """ Load a model from a model file """

        # ------------
        # check model

        if model is None:
            if self.__dmodel.get('name') is not None:
                model = self.__dmodel.get('name')
            else:
                model = False
        if model is False:
            msg = (
                "Select a model, see get_available_models()"
            )
            raise Exception(msg)

        # -------------
        # load

        (
            self.__dmodel,
            self.__dparam,
            self.__dmisc['dfunc_order'],
            self.__dargs,
        ) = _class_checks.load_model(model)

        # ------------
        # update from preset if relevant
        if preset is not None:
            self.load_preset(preset)

    def load_preset(self, preset=None):
        """ For the current model, load desired preset """
        _class_checks.update_from_preset(
            dparam=self.__dparam,
            dmodel=self.__dmodel,
            preset=preset,
        )

    def set_dparam(
        self,
        dparam=None,
        key=None, value=None,
    ):
        """ Set the dict of input parameters (dparam) or a single param

        dparam is the large dictionary that contains:
            - fixed-value parameters
            - functions of different types (equations)

        You can provide:
            - dparam as a dict
            - dparam as a str refering to an existing pre-defined model
            - only a key, value pair to change the value of a single parameter

        """

        # Check input: dparam xor (key, value)
        lc = [
            dparam is not None,
            key is not None and value is not None,
        ]
        if np.sum(lc) != 1:
            lstr = [
                '\t- {}: {}'.format(kk, vv)
                for kk, vv in [
                    ('dparam', dparam), ('key', key), ('value', value)
                ]
            ]
            msg = (
                "Please provide dparam xor (key, value)!\n"
                "You provided:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)

        # set dparam or update desired key
        if dparam is None:
            if key not in self.__dparam.keys():
                msg = (
                    "key {} is not identified!\n".format(key)
                    + "See get_dparam() method"
                )
                raise Exception(msg)
            dparam = dict(self.__dparam)
            dparam[key]['value'] = value

        # Update to check consistency
        (
            self.__dparam,
            self.__dmisc['dfunc_order'],
            self.__dargs,
        ) = _class_checks.check_dparam(dparam=dparam)

        # reset all variables
        self.reset()

    def get_dparam(self, verb=None, returnas=None, isfunc=None, **kwdargs):
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
            isfunc=isfunc,
            **kwdargs,
        )

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
        for k0 in self.get_dparam(eqtype=['ode', 'statevar'], returnas=list):
            if self.__dparam[k0]['eqtype'] == 'ode':
                self.__dparam[k0]['value'][0, :] = self.__dparam[k0]['initial']
                self.__dparam[k0]['value'][1:, :] = np.nan
            elif self.__dparam[k0]['eqtype'] == 'statevar':
                self.__dparam[k0]['value'][:, :] = np.nan

        # recompute inital value for statevar
        lstate = self.__dmisc['dfunc_order']['statevar']
        for k0 in lstate:
            # prepare dict of args
            kwdargs = {
                k1: v1[0, :]
                for k1, v1 in self.__dargs[k0].items()
            }
            # run function
            self.__dparam[k0]['value'][0, :] = (
                self.__dparam[k0]['func'](**kwdargs)
            )

        # set run to False
        self.__dmisc['run'] = False

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

    # ##############################
    #  Introspection
    # ##############################

    def __repr__(self):
        """ This is automatically called when only the instance is entered """
        col0 = [
            'model',
            'preset',
            'source',
            'nb. param (fixed)',
            'nb. param (func.)',
            'nb. ode',
            'nb. statevar',
            'run',
        ]
        ar0 = [
            self.__dmodel['name'],
            self.__dmodel['preset'],
            self.__dmodel['file'],
            len(self.get_dparam(returnas=list, eqtype=None)),
            len(self.get_dparam(returnas=list, eqtype='param')),
            len(self.get_dparam(returnas=list, eqtype='ode')),
            len(self.get_dparam(returnas=list, eqtype='statevar')),
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
        # Handling str repr

        # ----------
        # Numerical parameters
        col0 = ['Numerical param.', 'value', 'units', 'comment']
        ar0 = [
            [
                k0,
                _class_utility.paramfunc2str(dparam=self.__dparam, key=k0),
                v0['units'],
                v0['com'],
            ]
            for k0, v0 in self.get_dparam(
                returnas=dict,
                eqtype=[None, 'param'],
                group='Numerical',
            ).items()
        ]
        ar0.append(['run', str(self.__dmisc['run']), '', ''])

        # ----------
        # parameters
        col1 = ['Model param.', 'value', 'units', 'group', 'comment']
        ar1 = [
            [
                k0,
                _class_utility.paramfunc2str(dparam=self.__dparam, key=k0),
                str(v0['units']),
                v0['group'],
                v0['com'],
            ]
            for k0, v0 in self.get_dparam(
                returnas=dict,
                eqtype=[None, 'param'],
                group=('Numerical',),
            ).items()
        ]

        # ----------
        # functions
        col2 = [
            'function', 'source', 'initial', 'units', 'eqtype', 'comment',
        ]
        ar2 = [
            [
                k0,
                _class_utility.paramfunc2str(dparam=self.__dparam, key=k0),
                "{:.2e}".format(v0.get('value')[0, idx]),
                v0['units'],
                v0['eqtype'],
                v0['com'],
            ]
            for k0, v0 in self.get_dparam(
                returnas=dict,
                eqtype=['ode', 'statevar'],
            ).items()
        ]

        # --------------------------
        # Add solver and final value if has run
        if self.__dmisc['run'] is True:

            # add solver
            ar0.append(['solver', self.__dmisc['solver'], '', ''])

            # add column title
            col2.insert(3, 'final')

            # add final value to each variable
            ii = 0
            for k0, v0 in self.__dparam.items():
                if v0.get('eqtype') in ['ode', 'statevar']:
                    ar2[ii].insert(
                        3,
                        "{:.2e}".format(v0.get('value')[-1, idx]),
                    )
                    ii += 1

        # ----------
        # format output
        return _utils._get_summary(
            lar=[ar0, ar1, ar2],
            lcol=[col0, col1, col2],
            verb=True,
            returnas=False,
        )

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
        lode = self.__dmisc['dfunc_order']['ode']
        lstate = self.__dmisc['dfunc_order']['statevar']
        laux = []

        # ------------
        # start time loop

        try:
            if solver == 'eRK4-homemade':

                _solvers._eRK4_homemade(
                    dparam=self.__dparam,
                    lode=lode,
                    linter=lstate,
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
                    linter=lstate,
                    dargs=self.__dargs,
                    verb=verb,
                    rtol=rtol,
                    atol=atol,
                    max_time_step=max_time_step,
                    solver_scipy=solver_scipy,
                )
            self.__dmisc['run'] = True
            self.__dmisc['solver'] = solver

        except Exception as err:
            self.__dmisc['run'] = False
            raise err

    # ##############################
    #       Deep analysis methods
    # ##############################

    def FillCyclesForAll(self, ref=None):
        '''
        This function is a wrap-up on GetCycle to do it on all variables.

        For each variables, it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself
        '''

        for var, dic1 in self.__dparam.items():
            if 'func' in dic1.keys():
                if ref is None:
                    self.FillCycles(var, var)
                else:
                    self.FillCycles(var, ref)

    def FillCycles(self, var, ref='lambda'):
        '''
        it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself

        var : name of the variable we are working on
        ref : reference for the oscillations detections
        '''

        # Check if the run did occur

        # Get the new dictionnary to edit
        dic = self.__dparam[var]
        if 'cycles' not in dic.keys():
            dic['cycles'] = {'reference': ref}
            '''
'period_indexes': [],  # [[idx1,idx2],[idx2,idx3],] index of borders
# for each period
'period_T_intervals': [],  # [t[idx1,t[idx2]],..] time of borders
't_mean_cycle': [],  # [(t[idx1+t[idx2])/2.],..]
# time of the middle of the cycle
'period_T': [],  # duration of the cycle
'meanval': [],  # mean value during the interval
'stdval': [],   # standard deviation during the interval
'minval': [],   # minimal value in the interval
'maxval': [],   # maximal value in the interval
'reference': ref,  # the variable that has been used to detect cycle
}
            '''

        # check if reference has already calculated its period
        # the reference has cycle and this cycle has been calculated on itself
        dic1 = dic['cycles']
        ready = False
        if 'cycles' in self.__dparam[ref].keys():
            dic2 = self.__dparam[ref]['cycles']
            if (dic2['reference'] == ref and 'period_indexes' in dic2):
                # We can take the reference as the base
                ready = True
        # If there is no good reference
        # We calculate it and put
        if not ready:
            self.findCycles(ref)
            dic2 = self.__dparam[ref]['cycles']

        for key in ['period_indexes', 'period_T_intervals',
                    't_mean_cycle', 'period_T']:
            dic1[key] = dic2[key]

        tim = self.__dparam['time']['value']
        dic1['period_T_intervals'] = [[tim[idx[0], 0], tim[idx[1], 0]]
                                      for idx in dic1['period_indexes']]
        dic1['t_mean_cycle'] = [
            (t[0] + t[1]) / 2 for t in dic1['period_T_intervals']]
        dic1['period_T'] = [
            (t[1] - t[0]) for t in dic1['period_T_intervals']]

        # Fill for each the characteristics
        values = dic['value']
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

    def findCycles(self, refval):
        '''
        Detect all positions of local maximums and the time that is linked
        '''
        # initialisation
        periods = []
        id1 = 1

        self.__dparam[refval]['cycles'] = {}

        dic1 = self.__dparam[refval]['cycles']
        val = self.__dparam[refval]['value']

        # identification loop
        while id1 < len(val) - 2:
            if (val[id1] > val[id1 - 1] and
                    val[id1] > val[id1 + 1]):
                periods.append(1 * id1)
            id1 += 1

        # Fill the formalism
        self.__dparam[refval]['cycles']['period_indexes'] = [
            [periods[i], periods[i + 1]] for i in range(len(periods) - 1)
        ]
        tim = self.__dparam['time']['value']
        dic1 = self.__dparam[refval]['cycles']
        dic1['period_T_intervals'] = [[tim[idx[0]], tim[idx[1]]]
                                      for idx in dic1['period_indexes']]
        dic1['t_mean_cycle'] = [
            (t[0] + t[1]) / 2 for t in dic1['period_T_intervals']]
        dic1['period_T'] = [
            (t[1] - t[0]) for t in dic1['period_T_intervals']]
        dic1['reference'] = refval

        # ##############################
        #       plotting methods
        # ##############################

    def plot(self):
        """
        Launch all the basic plots
        """

    # ##############################
    #       data conversion
    # ##############################

    def _to_dict(self):
        """ Convert instance to dict """

        dout = {
            'dmodel': dict(self.__dmodel),
            'dparam': self.get_dparam(returnas=dict, verb=False),
            'dmisc': dict(self.__dmisc),
            'dargs': dict(self.__dargs),
        }
        return dout

    @classmethod
    def _from_dict(cls, dout=None):
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
        # reformat func from source
        for k0, v0 in dout['dparam'].items():
            if dout['dparam'][k0].get('func') is not None:
                dout['dparam'][k0]['func'] = eval(
                    f"lambda {dout['dparam'][k0]['source_kargs']}: "
                    f"{dout['dparam'][k0]['source_exp']}"
                )[0]

        # -------------------
        # create instance
        obj = cls()
        obj.__dmodel = dict(dout['dmodel'])
        obj.__dparam = {k0: dict(v0) for k0, v0 in dout['dparam'].items()}
        obj.__dmisc = dict(dout['dmisc'])
        obj.__dargs = dict(dout['dargs'])

        return obj

    # ##############################
    #       saving methods
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

        if name is None and self.dmodel['preset'] is not None:
            name = self.dmodel['preset']

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
