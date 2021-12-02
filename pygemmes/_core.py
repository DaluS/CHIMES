# -*- coding: utf-8 -*-

# %% Importations ###########

# built-in
import copy
import time


# Common
import numpy as np


# Library-specific
from ._utilities import _utils, _class_checks, _class_utility
from ._utilities import _solvers, _saveload
from ._plots import _plot_timetraces


class Hub():
    """
    Generic class to stock every data and method for the user to interac with
    """

    def __init__(self, model=None, preset=None, dpresets=None, verb=None):

        # Initialize the models
        self.__dparam = {}
        self.__dmodel = dict.fromkeys(
            ['name', 'file', 'description', 'presets', 'preset']
        )
        self.__dmisc = dict.fromkeys(
            ['dmulti', 'dfunc_order', 'run', 'solver']
        )
        self.__dargs = {}
        if model is not None:
            self.load_model(model, preset=preset, dpresets=dpresets, verb=verb)

    # ##############################
    # %% Setting / getting parameters
    # ##############################

    def load_model(self, model=None, preset=None, dpresets=None, verb=None):
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
            self.__dmisc['dmulti'],
            self.__dmisc['dfunc_order'],
            self.__dargs,
        ) = _class_checks.load_model(
            model,
            dmulti=self.__dmisc['dmulti'],
            verb=verb,
        )

        # ------------
        # update from preset if relevant
        if preset is not None:
            self.load_preset(preset, dpresets=dpresets, verb=verb)
        else:
            self.reset()

    def load_preset(self, preset=None, grid=None, dpresets=None, verb=None):
        """ For the current model, load desired preset """
        (
            self.__dparam,
            self.__dmisc['dmulti'],
            self.__dmisc['dfunc_order'],
            self.__dargs,
        ) = _class_checks.update_from_preset(
            dparam=self.__dparam,
            dmodel=self.__dmodel,
            dmulti=self.__dmisc['dmulti'],
            preset=preset,
            dpresets=dpresets,
            verb=verb,
        )
        self.reset()

    def set_dparam(
        self,
        dparam=None,
        key=None,
        value=None,
        grid=None,
        verb=None,
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

        # ----------------
        # check input

        if grid is None:
            grid = self.__dmisc['dmulti'].get('grid')

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

        # ----------------
        # set dparam or update desired key

        if dparam is None:
            _class_checks._set_key_value(
                dparam=self.__dparam,
                key=key,
                value=value,
                grid=grid,
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
            dmulti=self.__dmisc['dmulti'],
            verb=verb,
        )

        # reset all variables
        self.reset()

    def get_dparam(self, condition=None, verb=None, returnas=None, **kwdargs):
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
        lcrit = ['key', 'dimension', 'units', 'type', 'group', 'eqtype']
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
        for k0 in self.get_dparam(eqtype=['ode', 'statevar'], returnas=list):
            self.__dparam[k0]['value'][...] = np.nan

        # Reset initial for ode
        for k0 in self.get_dparam(eqtype=['ode'], returnas=list):
            self.__dparam[k0]['value'][0, ...] = self.__dparam[k0]['initial']

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

    def __repr__(self, verb=None):
        """ This is automatically called when only the instance is entered """

        if verb is None:
            verb = True

        col0 = [
            'model',
            'preset',
            'param (fix + func)',
            'ode',
            'statevar',
            'run',
            'source',
        ]
        ar0 = [
            self.__dmodel['name'],
            self.__dmodel['preset'],
            '{} + {}'.format(
                len(self.get_dparam(returnas=list, eqtype=None)),
                len(self.get_dparam(returnas=list, eqtype='param')),
            ),
            len(self.get_dparam(returnas=list, eqtype='ode')),
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

    def get_summary(self, idx=None):
        """
        Print a str summary of the solver

        """
        # ----------
        # check inputs

        idx = _class_checks._check_idx(
            idx=idx,
            nt=self.__dparam['nt']['value'],
            dmulti=self.__dmisc['dmulti'],
        )
        # ----------
        # starting with headr from __repr__
        col0, ar0 = self.__repr__(verb=False)

        # ----------
        # Numerical parameters
        col1, ar1 = _class_utility._get_summary_numerical(self)

        # ----------
        # parameters
        col2, ar2 = _class_utility._get_summary_parameters(self, idx=idx)

        # ----------
        # functions
        col3, ar3 = _class_utility._get_summary_functions(self, idx=idx)

        # ----------
        # format output
        return _utils._get_summary(
            lar=[ar0, ar1, ar2, ar3],
            lcol=[col0, col1, col2, col3],
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
        dverb = _class_checks._run_verb_check(verb=verb)

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

    def FillCyclesForAll(self, ref=None):
        '''
        This function is a wrap-up on GetCycle to do it on all variables.

        For each variables, it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself
        '''

        leq = ['ode', 'statevar']
        for var, dic1 in self.get_dparam(returnas=dict, eqtype=leq).items():
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
        print(var)
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

    def plot(
        self,
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

        return _plot_timetraces.plot_timetraces(
            self,
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
