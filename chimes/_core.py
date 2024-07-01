import types

# Library-specific
# from ._plots._plots import _DPLOT
from ._core_functions import _hub_set
from ._core_functions import setM, getM, calculateM, saveM
from ._config import config
# from .plots import Plots
from ._plot_class import Plots


class Hub(setM, getM, calculateM, saveM):
    """
    The `Hub` class is a central object for the user, providing an interface to interact with a given model.
    Given a model name, the `Hub` class loads the model file and retrieves its logics, presets, and associated values. 
    It performs tasks such as :
    * executing local models coupling operation in the `_model_MODELNAME.py` file, 
    * identifying parameters, state variables, and differential variables, 
    * finding their associated properties (definitions, units, values...), 
    * determining an order of calculation.

    Users can: 
    * access fields for value modification, 
    * the structure and properties in the model, 
    * perform simulations, 
    * create plots
    * conduct deeper analysis
    * save the model

    Parameters
    ----------
    model : str
        A string containing the model name. use chm.get_available_models() to see what is available
    preset : str, optional
        The name of the preset in the current dictionary of presets.
    dpresets : dict of dict of dict, optional
        A dictionary of presets that can be used (see model creation and set_dpreset).
    verb : bool, optional
        Set to True to enable print statements in the terminal. Default is defined by _VERB.

    Attributes
    ----------
    dflags : dict
        Dictionary of flags showing the system status.
    dfunc_order : list
        The ordered list of intermediary function names.
    dmodel : dict
        The model identifiers.
    dargs : dict
        Arguments for the model.
    dfields : dict
        Parameters for the model.
    dmisc : dict
        Contains miscellaneous, static practical informations.
    supplements : dict
        Additional information for the model.
    _DPLOT : dict
        Dictionary for plotting functions.

    Note
    ----
    The methods are described in other files than this class.
    """

    def __init__(
        self,
        model: str,
        preset: str = None,
        dpresets: dict = None,
        verb: bool = config.get_current('_VERB'),
        # from_user=_FROM_USER,
    ):
        _DEFAULTSIZE = config.get_current('_DEFAULTSIZE')
        from_user = False

        # ## USING EXTERNAL METHODS ############################################
        """
        Those methods are written in other files, and they are simply implemented here
        """

        methods_to_add = {}
        for Class in (setM, getM, calculateM, saveM):
            for method_name in dir(Class):
                # Exclude special methods and attributes
                if not method_name.startswith("__") and not callable(getattr(Class, method_name)):
                    method = getattr(Class, method_name)
                    methods_to_add[method_name] = method

        for name, method in methods_to_add.items():
            setattr(self, name, types.MethodType(method, self))

        # ## FLAGS DICTIONNARY #################################################
        """State of the system"""
        self._dflags = {
            'run': [0, 0],  # Is a numerical resolution done
            'cycles': False,  # Analysis: cycles detection
            'sensitivity': False,  # Analysis: sensitivity to initial conditions
            'derivative': False,  # Analysis: derivative and variable contributions
            'convergence': False,  # Analysis: convergence rate to equilibrium
            'multisectoral': False,  # Structure: multiple sectors/agents
            'multiregional': False,  # Structure: multiple regions in interaction 'nr'>1
            'Parrallel': False,  # Structure: multiple runs in parrallel      'nx'>1
            'reinterpolated': False,  # Structure: reinterpolated for less points
            'noreset':{},       # Structure: values changed in the middle of a run
        }

        # Contains miscellaneous, static practical informations
        self._dmisc = {'dmulti': {},   # Which variables has been imposed as multiple, and what size
                       'dfunc_order': {},   # Order in which fields are solved. Often used to get the field list
                       'model': model}      # Name of the model file

        # ## LOADING MODEL FILE ###############################################
        OUT = _hub_set.load_model(
            model,
            from_user=from_user,
            verb=verb,)

        self._dmodel = OUT[0]
        self._dfields = OUT[1]
        self._dmisc['dfunc_order'] = OUT[2]
        self._dargs = OUT[3]

        # Actualize the shape ##############################################
        self._dmisc['dmulti']['NxNr'] = (self._dfields['nx']['value'],
                                         self._dfields['nr']['value'])
        self._dmisc['dmulti']['scalar'] = []
        self._dmisc['dmulti']['vector'] = []
        self._dmisc['dmulti']['matrix'] = []

        for k, v in self._dfields.items():
            size = v.get('size', [_DEFAULTSIZE, _DEFAULTSIZE])
            if size == [_DEFAULTSIZE, _DEFAULTSIZE]:
                self._dmisc['dmulti']['scalar'].append(k)
            elif size[1] == _DEFAULTSIZE:
                self._dmisc['dmulti']['vector'].append(k)
            else:
                self._dmisc['dmulti']['matrix'].append(k)
        self._dflags['multisectoral'] = True if len(self._dmisc['dmulti']['vector'] + self._dmisc['dmulti']['matrix']) else False

        # activate presets if relevant ######################################
        if dpresets is not None:
            self.set_dpreset(dpresets, verb=False)
        if preset is not None:
            self.set_preset(preset, verb=False)
        else:
            self.reset()

        # name
        self._name = self._dmodel['name']

    # Read-only properties
    # ##############################
    @property
    def dflags(self):
        """dictionnary of flags showing what the system status"""
        return self._dflags

    @property
    def dfunc_order(self):
        """ The ordered list of intermediary function names """
        return self._dmisc['dfunc_order']

    @property
    def dmodel(self):
        """ The model identifiers """
        return self._dmodel

    @property
    def dargs(self):
        return self._dargs

    @property
    def name(self):
        return self._name

    @property
    def dfields(self):
        return self.get_dfields(returnas=dict, verb=False)

    @property
    def dmisc(self):
        return self._dmisc

    @property
    def supplements(self):
        return self.dmodel.get('supplements', {})

    @property
    def _DPLOT(self):
        return Plots

    def __repr__(self, verb=None):
        self._short()
        return ''

    # ##############################
    #       plotting methods
    # ##############################

    def plot_preset(self, preset=None, returnFig=False):
        '''
        Automatically plot all functions that are defined in _plot.py, associated with the preset

        If a preset is loaded, you do not need to precise it when using the function
        If no preset is loaded, you can try to plot its associated plots by calling it.
        '''

        # Load preset name if preset is loaded. If not it will remain None
        if preset is None:
            preset = self.dmodel['preset']

        F = []
        description = []

        if preset is not None:
            tempd = self.dmodel['presets'].get(preset, {'plots': {}})['plots']
            # print(preset,tempd)
            if type(tempd) is tuple:
                raise Exception('your plot dictionnary might have a comma at the end, please remove it !')
            for plotname in Plots.documentation['short description'].keys():
                for argl in tempd.get(plotname, []):
                    X = getattr(Plots, plotname)(self, returnFig=returnFig, **argl)
                    F.append(X)
                    description.append([plotname, argl])
                    print()
        if returnFig:
            return F, description

    def plot(
            self,
            filters_key=(),
            filters_units=(),
            filters_sector=(),
            separate_variables={},
            idx=0,
            Region=0,
            title='',
            tini=False,
            tend=False,
            lw=2, returnFig=False):
        '''
        generate one subfigure per set of units existing.

        There are three layers of filters, each of them has the same logic :
        if the filter is a tuple () it exclude the elements inside,
        if the filter is a list [] it includes the elements inside.

        Filters are the following :
        filters_units      : select the units you want
        filters_sector     : select the sector you want  ( '' is all monosetorial variables)
        filters_sector     : you can put sector names if you want them or not. '' corespond to all monosectoral variables
        separate_variables : key is a unit (y , y^{-1}... and value are keys from that units that will be shown on another graph,

        Region             : is, if there a multiple regions, the one you want to plot
        idx                : is the same for parrallel systems
        '''

        F = getattr(Plots, 'byunits')(
            hub=self,
            filters_key=filters_key,
            filters_units=filters_units,
            filters_sector=filters_sector,
            separate_variables=separate_variables,
            lw=lw,
            idx=idx,
            Region=Region,
            tini=tini,
            tend=tend,
            title=title,
            returnFig=returnFig)
        if returnFig:
            return F
