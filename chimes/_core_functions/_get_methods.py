from .._core_functions import _utils, _utils
import numpy as np
import pandas as pd
from .._core_functions import _Network
import inspect


class getM:
    """
    Get methods are Hub introspection, they allow to get information about the model, the fields, the parameters, the equations, etc...
    They should not modify the model, and are typically made to return dataframe, dictionnaries, or print information.
    Dataframe looks nice in ipynb ! 

    Author
    ------
    Paul Valcke

    Date
    ----
    """

    def __init__(self):
        pass

    def get_multisectoral(self):
        """
        Retrieve the multisectoral information: for each field, what is its dimensions

        Returns
        -------
        dict
            The multisectoral information.

        Author
        ------
        Paul Valcke

        Date
        ----
        2024/03/20
        """

        d0 = self.dmisc['dmulti']
        R = self.get_dfields()
        OUT = {}
        for cat, liste in d0.items():
            if cat != 'NxNr':
                for field in liste:
                    if R[field]['group'] != 'Numerical' and R[field].get('eqtype', '') != 'size':
                        OUT[field] = {'categorie': cat,
                                      'EQ type': R[field].get('eqtype', 'parameter'),
                                      'vector': R[field].get('size', ['__ONE__', '__ONE__'])[0].replace('__ONE__', ''),
                                      'matrix': R[field].get('size', ['__ONE__', '__ONE__'])[1].replace('__ONE__', ''), }
        return pd.DataFrame(OUT).transpose()

    def get_dimensions(self):
        """
        Retrieve the size of each dimension used in the model for multisectoral purposes

        Returns
        -------
        a dataframe that contains all the sizes of the dimensions used in the model

        Author
        ------
        Paul Valcke

        Date
        ----
        2024/03/20
        """

        R = self.get_dfields()
        OUT = {}
        Dims = [field for field in R.keys() if R[field].get('eqtype', '') == 'size']
        for d in Dims:
            OUT[d] = {'definition': R[d]['definition'], 'size': R[d]['value'], 'named list': R[d]['list'], 'Impact in the model': [
                k for k in R.keys() if R[k].get('size', ['__ONE__', '__ONE__'])[0] == d or R[k].get('size', ['__ONE__', '__ONE__'])[1] == d]}

        OUT['nx']['Impact in the model'] = 'All fields'
        OUT['nr']['Impact in the model'] = 'All fields'
        return pd.DataFrame(OUT).transpose()

    def get_presets(self, returnas=True):
        """
        Retrieve preset names and descriptions.

        Parameters
        ----------
        returnas : bool or str, optional
            Determines the format of the returned presets.
            If False, prints the presets.
            If 'list', returns a list of the presets.
            If 'dict', returns a dictionary of the presets.
            If True or 'dataframe', returns a DataFrame of the presets.
            Default is True.

        Returns
        -------
        None, list, dict, or pandas.DataFrame
            The presets in the specified format. If returnas is False, nothing is returned.

        Notes
        -----
        The function retrieves the presets from the '_dmodel' attribute. 
        It then formats the presets according to the 'returnas' parameter and returns or prints them.

        Author
        ------
        Paul Valcke

        Date
        ----
        OLD
        """
        if returnas is False:
            print('List of available presets :')
            for k, v in self._dmodel['presets'].items():
                print(k.ljust(30), v['com'])
        if returnas == 'list':
            return list(self._dmodel['presets'].keys())
        if returnas in [True, 'True', 'dataframe']:
            return pd.DataFrame({k: {'Description': v['com']} for k, v in self._dmodel['presets'].items()}).transpose().style.set_properties(**{'text-align': 'left'})
        else:
            return {k: v['com'] for k, v in self._dmodel['presets'].items()}

    def get_supplements(self, returnas=True):
        """
        Retrieve all supplements and their descriptions.

        Supplements can be used with: hub.supplements[Nameofthesupplement]

        Parameters
        ----------
        returnas : bool or str, optional
            Determines the format of the returned supplements.
            If False, prints the supplements.
            If 'list', returns a list of the supplements.
            If 'dict', returns a dictionary of the supplements.
            If True, returns a DataFrame of the supplements.
            Default is True.

        Returns
        -------
        None, list, dict, or pandas.DataFrame
            The supplements in the specified format. If returnas is False, nothing is returned.

        Notes
        -----
        The function retrieves the supplements from the 'dmodel' attribute. 
        It then formats the supplements according to the 'returnas' parameter and returns or prints them.

        Author
        ------
        Paul Valcke

        Date
        ----
        OLD
        """
        supp = self.dmodel.get('supplements', {})

        if returnas is True:
            d0 = {}
            for k, v in self.supplements.items():
                try:
                    d0[k] = {'documentation': v.__doc__,
                             'signature': inspect.signature(v)}
                except BaseException:
                    try:
                        d0[k] = {'documentation': v.__doc__,
                                 'signature': f'type: {help(v)}'}
                    except BaseException:
                        d0[k] = {'documentation': type(v),
                                 'signature': 'no signature'}
            return pd.DataFrame(d0).transpose().style.set_properties(**{'text-align': 'left'})
        if returnas is False:
            print('List of supplements material :')
            for k, v in supp.items():
                print(k.ljust(30), v.__doc__)  # ['com'])
        if returnas == list:
            return list(supp.keys())
        else:
            return {k: v.__doc__ for k, v in supp.items()}

    def get_dfields(self, condition=None, returnas=dict, verb=False, **kwdargs):
        """
        Return a subset of the input parameters dictionary that matches specified criteria.

        Parameters
        ----------
        condition : str, optional
            The condition to apply when selecting parameters. Can be 'all' or 'any'. 
            If 'all', only parameters that match all criteria will be selected. 
            If 'any', parameters that match any of the criteria will be selected. 
            Default is None, which means all parameters will be selected.
        returnas : type, optional
            The type to return the selected parameters as. Can be dict, np.ndarray, list, or 'DataFrame'. 
            If dict, returns a dictionary of the selected parameters. 
            If np.ndarray, returns a dictionary of np.ndarrays of the selected parameters. 
            If list, returns a list of the selected parameter keys. 
            If 'DataFrame', returns a pandas DataFrame of the selected parameters. 
            Default is dict.
        verb : bool, optional
            If True, pretty-prints the selected parameters. Default is False.
        **kwdargs : dict
            Additional criteria to use when selecting parameters. The keys should be parameter attributes 
            (e.g., 'key', 'dimension', 'units', 'type', 'group', 'eqtype', 'isneeded') and the values should be the desired values for those attributes.

        Returns
        -------
        dict, np.ndarray, list, or pandas.DataFrame
            The selected parameters in the specified format.

        Raises
        ------
        Exception
            If the condition is not 'all' or 'any', or if the returnas type is not recognized, an exception is raised.

        Notes
        -----
        The function first checks the condition and returnas arguments and raises an exception if they are not recognized. 
        It then selects the parameters from '_dfields' that match the specified criteria. 
        If verb is True, it pretty-prints the selected parameters. 
        Finally, it returns the selected parameters in the specified format.

        Author
        ------
        Didier Vezinet

        Date
        ----
        2021 August
        """
        lcrit = ['key', 'dimension', 'units',
                 'type', 'group', 'eqtype', 'isneeded']

        return _utils._get_dict_subset(
            indict=self._dfields,
            verb=False,
            returnas=dict,
            lcrit=lcrit,
            lprint=[],
            condition=condition,
            **kwdargs,
        )

    def get_dfields_as_reverse_dict(
        self,
        crit=None,
        returnas=None,
        verb=None,
        **kwdargs,
    ):
        """
        Return or print a dictionary of unique values for a specified criterion with corresponding parameter keys.
        Recommended for use with the 'dimension', 'units', 'type', 'group', or 'eqtype' criteria, when you want a susbet of fields. 

        Parameters
        ----------
        crit : str, optional
            The criterion to use when creating the dictionary. Can be 'dimension', 'units', 'type', 'group', or 'eqtype'. 
            The dictionary will have unique values for this criterion as keys and lists of corresponding parameter keys as values. 
            Default is None, which means all criteria will be used.
        returnas : type, optional
            The type to return the dictionary as. Can be dict or False. 
            If dict, returns the dictionary. 
            If False, does not return anything. 
            Default is dict if verb is False, otherwise False.
        verb : bool, optional
            If True, prints the dictionary. Default is False.
        **kwdargs : dict
            Additional criteria to use when selecting parameters. The keys should be parameter attributes 
            (e.g., 'key', 'dimension', 'units', 'type', 'group', 'eqtype', 'isneeded') and the values should be the desired values for those attributes.

        Returns
        -------
        dict or None
            The dictionary of unique criterion values and corresponding parameter keys, or None if returnas is False.

        Raises
        ------
        Exception
            If the crit argument is not recognized or if it conflicts with the kwdargs, an exception is raised.

        Notes
        -----
        The function first checks the crit and returnas arguments and raises an exception if they are not recognized or if there is a conflict. 
        It then creates a dictionary with unique values for the specified criterion as keys and lists of corresponding parameter keys as values. 
        If verb is True, it prints the dictionary. 
        Finally, it returns the dictionary if returnas is dict.

        Author
        ------
        Didier Vezinet

        Date
        ----
        2021 August
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

        lunique = set([v0.get(crit) for v0 in self._dfields.values()])
        dout = {
            k0: self.get_dfields(returnas=list, **{crit: k0, **kwdargs})
            for k0 in lunique
        }

        # -------------
        # print and/or return

        if verb is True:
            lstr = [f'\t- {k0}: {v0}' for k0, v0 in dout.items()]
            msg = (
                "The following selection has been identified:\n" + "\n".join(lstr)
            )
            print(msg)

        if returnas is dict:
            return dout

    def get_dvalues(self, idx=0, Region=0, params=False):
        """
        Returns a dictionary with values of variables.

        This function automatically scans for multisectoriality, regions, and parallel systems.
        Depending on these factors, it will change the format of values.

        Parameters
        ----------
        idx : bool or array-like, optional
            If True, uses all indices. If an array, uses the specified indices. Default is True.
        Region : bool or array-like, optional
            If True, uses all regions. If an array, uses the specified regions. Default is True.
        params : bool, optional
            If True, includes parameters in the returned dictionary. Default is False.

        Returns
        -------
        dict
            A dictionary where keys are variable names and values are variable values.

        Notes
        -----
        The function first gets the parameters dictionary. It then checks the idx and Region arguments and sets them to appropriate values.
        Depending on the presence of vector and matrix variables, it constructs the dictionary in a different way.
        If params is True, it adds parameters to the dictionary.

        Author
        ------
        Paul Valcke

        Date
        ----
        2023
        """
        R = self.get_dfields()

        idx = np.arange(self.dmisc['dmulti']['NxNr'][0]) if idx is True else idx
        Region = np.arange(self.dmisc['dmulti']['NxNr'][1]) if Region is True else Region

        if type(idx) in [list, np.ndarray]:
            idx = 0 if len(idx) == 1 else idx
        if type(Region) in [list, np.ndarray]:
            Region = 0 if len(Region) == 1 else Region

        statevars_and_diffs = self.dmisc['dfunc_order']['statevar'] + self.dmisc['dfunc_order']['differential']

        if len(self.dmisc['dmulti']['vector'] + self.dmisc['dmulti']['matrix']) < 1:
            D = {k: R[k]['value'][:, idx, Region, 0, 0] for k in statevars_and_diffs}
        elif len(self.dmisc['dmulti']['matrix']) == 0:
            D = {k: R[k]['value'][:, idx, Region, :, 0] for k in statevars_and_diffs}
        else:
            D = {k: R[k]['value'][:, idx, Region, :, :] for k in statevars_and_diffs}

        if params:
            for k in self.dmisc['dfunc_order']['parameters']:
                if not isinstance(R[k]['value'], (int, float)):
                    D[k] = R[k]['value'].reshape(-1)

        return D

    def get_summary(self, idx=0, Region=0, removesector=()):
        """
        INTROSPECTION TOOL :
        Print a str summary of the model, with
        * Model description
        * Parameters, their properties and their values
        * ODE, their properties and their values
        * Statevar, their properties and their values
        For more precise elements, you can do introspection using hub.get_dfields()
        INPUT :
        * idx = index of the model you want the value to be shown when there are multiple models in parrallel
        * region : name or index of the region you want to plot
        """

        # _FLAGS = ['run', 'cycles', 'derivative', 'multisectoral', 'solver']
        # _ORDERS = ['statevar', 'differential', 'parameters']

        # Vals = self._dfields

        print(60 * '#')
        print(20 * '#', 'SUMMARY'.center(18), 20 * '#')
        print(60 * '#')

        self._short()

        print('\n')
        print(60 * '#')
        print(20 * '#', 'fields'.center(18), 20 * '#')
        if self._dfields['nr']['value'] != 1:
            print(20 * '#', str('Region :' + str(self._dfields['nr']['list'][Region])).center(18), 20 * '#')
        if self._dfields['nx']['value'] != 1:
            print(20 * '#', str('Parr. sys numb:' + str(self._dfields['nx'].get('list', np.arange(self._dfields['nx']['value']))[idx])).center(18), 20 * '#')
        print(60 * '#')
        print(' ')
        # parameters
        col2, ar2 = _utils._get_summary_parameters(self, idx=idx, filtersector=removesector)
        # SCALAR ODE
        col3, ar3 = _utils._get_summary_functions_vector(
            self, idx=idx, Region=Region, eqtype=['differential'], filtersector=removesector)
        # SCALAR Statevar
        col4, ar4 = _utils._get_summary_functions_vector(
            self, idx=idx, Region=Region, eqtype=['statevar'], filtersector=removesector)

        print(''.join([a.ljust(15) for a in col2]))
        print(''.join([(len(a.ljust(15)) - 2) * '-' + '  ' for a in col2]))
        for a in ar2:
            print(''.join([str(aa).ljust(15) for aa in a]))
        print('')

        # ----------
        # format output
        _utils._get_summary(
            lar=[ar3, ar4],
            lcol=[col3, col4],
            verb=True,
            returnas=False,)

        print(30 * '=')
        # Print matrices
        _utils._print_matrix(self, idx=idx, Region=Region)

    def get_new_summary(self, firstlast=None) -> dict:
        """
        Generates a summary of the model.

        This method generates a summary of the model, including the model description, parameters, their properties and values, 
        ODEs, their properties and values, and state variables, their properties and values. The summary is returned as a dictionary 
        of pandas DataFrames.

        For more detailed information, you can use the `get_dfields` method.

        Parameters
        ----------
        firstlast : bool, optional
            If True, only the first and last values of each variable are included in the summary. If None, this is determined 
            based on whether the model has been run to completion. Default is None.

        Returns
        -------
        SUMMARY : dict
            A dictionary where each key is a category of information (e.g., 'Field Basic Properties', 'Parameters values') and 
            the value is a DataFrame containing that information.

        Author
        ------
        Paul Valcke

        Date
        ----
        2023
        """
        df0 = self.get_fieldsproperties()

        if firstlast is None:
            firstlast = self.dflags['run'][0] == self._dfields['nt']['value'] - 1

        dfp = self.get_dataframe(eqtype=None, t0=0, t1=self.dflags['run'][0])
        dfd = self.get_dataframe(eqtype='differential', t0=0, t1=self.dflags['run'][0], firstlast=firstlast)
        dfs = self.get_dataframe(eqtype='statevar', t0=0, t1=self.dflags['run'][0], firstlast=firstlast)

        SUMMARY = {
            'Field Basic Properties': df0,
            'Parameters values': dfp.transpose(),
            'State Variables values': dfs.transpose(),
            'Differential Variables values': dfd.transpose()
        }
        return SUMMARY

    def get_fieldsproperties(self) -> pd.DataFrame:
        """
        Retrieves the properties of the fields in the model.

        This method retrieves the properties of the fields in the model, such as their definitions, units, source expressions, 
        comments, groups, symbols, sizes, and equation types. It then formats these properties into a pandas DataFrame for easy viewing.

        Returns
        -------
        AllFields : pandas.DataFrame
            A DataFrame where each row represents a field in the model and each column represents a property of the field.

        Author
        ------
        Paul Valcke

        Date
        ----
        2023
        """
        categories = ['definition', 'units', 'source_exp', 'com', 'group', 'symbol', 'isneeded', 'size', 'eqtype']
        R = self.get_dfields()
        # Rpandas = {k0: {k: v for k, v in R[k0].items() if k in categories} for k0 in R.keys()}

        Rpandas = {k0: {k: R[k0][k] for k, v in R[k0].items() if k in categories} for k0 in R.keys()}
        for k0 in Rpandas.keys():
            if Rpandas[k0].get('eqtype', False) == 'differential':
                Rpandas[k0]['source_exp'] = 'd' + k0 + '/dt=' + Rpandas[k0]['source_exp']
            elif Rpandas[k0].get('eqtype', False) == 'statevar':
                Rpandas[k0]['source_exp'] = k0 + '=' + Rpandas[k0]['source_exp']
        AllFields = pd.DataFrame(Rpandas, index=categories).transpose()
        return AllFields.replace(np.nan, '')

        # for k0, properties in Rpandas.items():
        #   properties['source_exp'] = f'd{k0}/dt={properties["source_exp"]}' if properties.get('eqtype') == 'differential' else f'{k0}={properties["source_exp"]}'

        # AllFields = pd.DataFrame(Rpandas, index=categories).transpose().fillna('')
        # return AllFields

    def get_dataframe(self, eqtype=False, t0=False, t1=False, firstlast=False) -> pd.DataFrame:
        """
        Returns a DataFrame representation of the model's parameters.

        This method retrieves the parameters of the model and formats them into a pandas DataFrame for easy viewing and manipulation. 
        The DataFrame includes the field, value, time, parallel, region, Multi1, and Multi2 for each parameter.

        Parameters
        ----------
        eqtype : str, optional
            The type of equation to include in the DataFrame. If False, all types are included. Default is False.
        t0 : int or float, optional
            The start time for the DataFrame. If False, the start time is 0. Default is False.
        t1 : int or float, optional
            The end time for the DataFrame. If False, the end time is the last time step. Default is False.
        firstlast : bool, optional
            If True, only the first and last time steps are included in the DataFrame. Default is False.

        NOTES:
        ------
        This is not mature, should be written in a more elegant way.

        Returns
        -------
        df : pandas.DataFrame
            A DataFrame where each row represents a parameter and each column represents a property of the parameter.
        """
        # R0 = self.get_dfields()
        # R = R0 if eqtype is False else self.get_dfields(eqtype=eqtype)

        # Time ids
        # time = R0['time']['value'][:, 0, 0, 0, 0]
        # idt0, idt1 = 0, 1 if np.isnan(time[1]) else get_time_indices(self, time, t0, t1)

        # TimeId = np.array([0, -1]) if firstlast else get_time_id(self, idt1, time, idt0)

        # SectsX, SectsR, Time = R0['nx']['list'], R0['nr']['list'], R0['time']['value'][TimeId, 0, 0, 0, 0]

        # Onedict = get_onedict(self, R, R0, TimeId, SectsX, SectsR, Time)

        # drop = {k: len(set(v)) == 1 for k, v in Onedict.items()}

        # newdict = {k: v for k, v in Onedict.items() if not drop.get(k, False)}
        # newindex = [k for k, v in drop.items() if not v]

        # df = pd.DataFrame(newdict)
        # if len(newindex):
        #    df = df.set_index(newindex, drop=True)

        # return df.transpose()

        R0 = self.get_dfields()
        if eqtype is False:
            R = R0
        else:
            R = self.get_dfields(eqtype=eqtype)

        # Time ids
        time = R0['time']['value'][:, 0, 0, 0, 0]
        if np.isnan(time[1]):
            idt0 = 0
            idt1 = 1
        else:
            if type(t0) in [int, float]:
                idt0 = np.argmin(np.abs(time - t0))
            else:
                idt0 = 0

            if type(t1) in [int, float]:
                idt1 = np.argmin(np.abs(time - t1)) + 1
            else:
                idt1 = -1
        if firstlast:
            TimeId = np.array([0, -1])
        else:
            if idt1 == -1:
                idt1 = len(time) - 1
            TimeId = np.arange(idt0, idt1)

        SectsX = R0['nx']['list']
        SectsR = R0['nr']['list']
        Time = R0['time']['value'][TimeId, 0, 0, 0, 0]

        Onedict = {'field': [],
                   'value': [],
                   'time': [],
                   'parrallel': [],
                   'region': [],
                   'Multi1': [],
                   'Multi2': [],
                   }
        # Bigdict = {}
        for k in R.keys():
            if R[k].get('eqtype', None) not in ['parameter', 'parameters', None, 'size']:
                GRID = np.meshgrid(
                    R0[R[k]['size'][1]].get('list', ['mono']),
                    R0[R[k]['size'][0]].get('list', ['mono']),
                    SectsR,
                    SectsX,
                    Time
                )
            elif R0[k]['group'] != 'Numerical':
                GRID = np.meshgrid(
                    R0[R[k]['size'][1]].get('list', ['mono']),
                    R0[R[k]['size'][0]].get('list', ['mono']),
                    SectsR,
                    SectsX,
                    [0.]
                )
            else:
                GRID = np.meshgrid(
                    [''],
                    [''],
                    [''],
                    [''],
                    [0.]
                )
            Val = R[k]['value'][TimeId, ...] if R[k].get('eqtype', None) not in ['parameter', 'parameters', None, 'size'] else R[k]['value']
            if type(Val) in [float, int]:
                Val = np.array([Val])
            Val = Val.reshape(-1)
            Onedict['field'].extend([k for i in GRID[-1].reshape(-1)])
            Onedict['value'].extend(Val)
            Onedict['time'].extend(GRID[-1].reshape(-1))
            Onedict['parrallel'].extend(GRID[-2].reshape(-1))
            Onedict['region'].extend(GRID[-3].reshape(-1))
            Onedict['Multi1'].extend(GRID[-4].reshape(-1))
            Onedict['Multi2'].extend(GRID[-5].reshape(-1))

        drop = {'parrallel': True if len(set(Onedict['parrallel'])) == 1 else False,
                'region': True if len(set(Onedict['region'])) == 1 else False,
                'Multi1': True if len(set(Onedict['Multi1'])) == 1 else False,
                'Multi2': True if len(set(Onedict['Multi2'])) == 1 else False,
                'time': True if len(set(Onedict['time'])) == 1 else False, }

        newdict = {k: v for k, v in Onedict.items() if not drop.get(k, False)}
        newindex = [k for k, v in drop.items() if not v]
        # print(drop)
        if len(newindex):
            # print('newindex',newindex)
            # print('drop',drop)
            # print('newdict',newdict.keys())
            # print()
            df = pd.DataFrame(newdict)
            df = df.set_index(newindex, drop=True)
            # try:
            #    df=df.unstack()
            # except BaseException:
            #    print('could not unstack !')
        else:
            df = pd.DataFrame(newdict)
        return df.transpose()

    def get_Network(self,
                    filters=(),
                    auxilliary=False,
                    redirect=False,
                    screensize=1000,
                    screenheight=None,
                    screenwidth=None,
                    custom=True,
                    params=True,
                    returnFig=True):
        """
        Generate an interactive HTML file showing how variables are linked with their appropriate units.

        Parameters
        ----------
        hub : object
            The model object you want to visualize.
        filters : list or tuple, optional
            If list, only the fields kept. If tuple, fields removed. Default is ().
        auxilliary : bool, optional
            If False, variables that are not necessary for a run will not be shown. Default is False.
        screensize : int, optional
            The size of the screen for the visualization. Default is 600.
        screenwidth: int, optional
            The width of the screen. Set to control width and height separately, takes precedence over screensize. Default is None
        screenheight: int, optional
            The height of the screen. Set to control width and height separately, takes precedence over screensize. Default is None
        custom : bool, optional
            If True, allows for custom settings. Default is False.
        redirect : bool, optional
            If True, removed variables will transfer their dependency to the one they are linked to. Default is False.
        plot_params : bool, optional
            If True, parameters will be plotted. Default is True.
        returnFig : bool, optional
            If True, the function will return the figure object. Default is True.

        Returns
        -------
        fig : object
            The figure object of the network. Only returned if returnFig is True.

        Author
        ------
        Paul Valcke

        Date
        ----
        2023
        """
        return _Network.Network_pyvis(self,
                                      filters=filters,
                                      redirect=redirect,
                                      auxilliary=auxilliary,
                                      screensize=screensize,
                                      screenheight=screenheight,
                                      screenwidth=screenwidth,
                                      custom=custom,
                                      plot_params=params,
                                      returnFig=returnFig)

    def Extract_preset(self, t=-1) -> dict:
        """
        Create a dictionary containing all field values at the instant t.

        By default, it takes the value at the latest instant. You can save it and use it with set_fields in a new run!

        Parameters
        ----------
        t : float, optional
            The time at which to extract the field values. If -1, extracts the values at the latest time. Default is -1.

        Returns
        -------
        dict
            A dictionary where keys are field names and values are field values at the specified time.

        Examples
        --------
            hub.run()                            # Do a simulation
            hub.set_fields(hub.Extract_preset()) # Set the fields to the latest values

            hub.run()
            hub2=hub.copy()
            hub2.set_fields(hub.Extract_presets(t=50)) # Set the fields to the values at t=50
            hub2.set_fields(alpha=0) # Change one value
            hub2.run()

        Notes
        -----
        The function first gets the time vector. It then finds the index of the closest time to t, or uses the last index if t is -1.
        It gets the field values at the specified time and stores them in a dictionary. The format of the values depends on the field type.
        Tini is not changed explicitely, you have to do it manually if you want to change it.

        Author
        ------
        Paul Valcke

        Date
        ----
        2023
        """

        # Getting time vector
        T = self.get_dfields(key=['time'])
        vectime = T['time']['value'][:, 0, 0, 0]

        # Extracting values
        if t != -1:
            idt = np.argmin(np.abs(vectime - t)) - 1
        else:
            idt = -1
        R = self.get_dfields(key=('time', '__ONE__'))

        presetdict = {}
        for k, v in R.items():
            type = v.get('eqtype', None)
            if type in ['differential']:
                presetdict[k] = v['value'][idt, :, :, :] * 1.
            elif type in ['parameters', None]:
                presetdict[k] = v['value']
            elif type in ['size']:
                presetdict[k] = v.get('list', v['value'])
        return presetdict

    def _short(self) -> None:
        """
        Prints a summary of the hub object.

        This function is used as the __repr__ method for the hub object. It prints the model name, description, and file, 
        the number and names of state variables, differentials, and parameters, the presets and their comments, 
        the flags and their values, the time vector variables and their values and definitions, 
        and the size variables and their values and definitions.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        The function first prints the model information. It then prints the number and names of state variables, differentials, and parameters, 
        excluding certain reserved names. It prints the presets and their comments, the flags and their values, 
        the time vector variables and their values and definitions, and the size variables and their values and definitions.

        Author
        ------
        Paul Valcke

        Date
        ----
        2022
        """
        _ORDERS = ['statevar', 'differential', 'parameters']

        Vals = self._dfields

        print(f"Model       : {self.dmodel['name']}")
        print(self.dmodel['description'])
        print(f"File        : {self.dmodel['file']}")

        excluded_fields = ['t', '__ONE__', 'Tsim', 'Tini', 'dt', 'nt', 'nr', 'nx']

        print(f"{20 * '#'} Fields {20 * '#'}")
        for o in _ORDERS:
            fields = [z for z in self.dmisc['dfunc_order'][o] if z not in excluded_fields]
            print(f"{o.ljust(15)} {str(len(fields)).zfill(3)} {fields}")

        print(f"{20 * '#'} Presets {20 * '#'}")
        for k, v in self.dmodel['presets'].items():
            print(f"     {k.center(18)} : {v['com']}")

        print(f"{20 * '#'} Flags {20 * '#'}")
        for f, v in self._dflags.items():
            print(f"{f.ljust(15)}: {v}")

        print(f"{20 * '#'} Time vector {20 * '#'}")
        for k, v in Vals.items():
            if k in ['Tsim', 'Tini', 'dt', 'nt']:
                print(f"{k.ljust(20)}{str(v['value']).ljust(20)}{v['definition']}")

        print(f"{20 * '#'} Dimensions {20 * '#'}")
        sub = self.get_dfields(returnas=dict, eqtype=['size'],)
        for k in list(sub.keys()):
            v = Vals[k]
            print(f"{k.ljust(20)}{str(v['value']).ljust(20)}{v['definition']}")
