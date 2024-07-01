from .._config import config
from .._core_functions import _hub_set
import numpy as np
import copy
"""
This file contains the methods to set fields, values and dimensions in the Hub object.
All the methods are inside a class called setM, which is a child of the Hub class.
The file also have subfunctions that are used by the methods. They should not be read directly by users. 

Author
------
Paul Valcke

Date
----
Updated January 2024
"""


def _comparesubarray(M):
    """
    Check if a dimension in an N-dimensional array is a stack of identical subarrays.

    This function takes an N-dimensional array and checks each dimension to see if it is just a stack of identical 
    subarrays. It returns a list of boolean values, one for each dimension, where True indicates that the dimension is a 
    stack of identical subarrays.

    Parameters
    ----------
    M : array_like
        Input array of N dimensions.

    Returns
    -------
    Sameaxis : list of bool
        A list of boolean values indicating whether each dimension in the input array is a stack of identical subarrays.

    Author
    ------
    Paul Valcke

    Date
    ----
    OLD
    """
    M = np.array(M)
    Sameaxis = []
    dimensions = np.shape(M)
    for ii, d in enumerate(dimensions):

        Mrshp = M.reshape(-1, dimensions[ii])
        Dimtocompare = Mrshp.shape[0]

        Sameaxis.append(np.prod([np.array_equal(Mrshp[0, :],
                                                Mrshp[jj, :])
                                for jj in range(Dimtocompare)]) > 0)
    return Sameaxis


def _set_dimensions(self, verb=config.get_current('_VERB'), **kwargs):
    """
    Change the dimensions of the system.

    This function takes a set of keyword arguments, where each key is a dimension name and each value is the new value for the dimension. 
    It updates the dimensions in the data structure and returns the updated data structure.

    Parameters
    ----------
    verb : bool, optional
        If `True`, verbose output is enabled. Default is `_VERB`.
    **kwargs : dict
        The keyword arguments where each key is a dimension name and each value is the new value for the dimension.

    Returns
    -------
    self
        The updated data structure.

    Notes
    -----
    The function first gets the list of dimensions that need to be changed and the list of differential parameters. 
    Then it checks if changing the dimensions will cause any issues. If there's an issue, it prints a warning message.

    For each dimension, if the new value is a list, it sets the length of the list to the dimension and stores the list. 
    If the new value is a float or an int, it sets the value to the dimension and stores a list of integers from 0 to the value. If 'verb' is `True`, it prints the updated dimension and its sectors.

    Finally, it sets the shapes and values of the parameters and gets the arguments by reference.

    Author
    ------
    Paul Valcke

    Date
    ----
    OLD
    """
    # we scan all fields that will need to have their values changed
    setofdimensions = set(['nr', 'nx', 'dt', 'Tini', 'Tsim'] + list(self.get_dfields(eqtype=['size'])))
    diffparam = set(self.get_dfields(eqtype=['differential', None])) - set(['__ONE__', 'time']) - setofdimensions

    for kk in list(diffparam):
        V = self._dfields[kk]
        dimname = ['nx', 'nr'] + V['size']
        direct = 'initial' if V.get('eqtype', '') == 'differential' else 'value'
        ValidAxis = _comparesubarray(V[direct])

        for ii, axis in enumerate(ValidAxis):
            dim = dimname[ii]
            if dim in kwargs.keys() and not axis:
                print(f'ISSUE : YOU CHANGE {dim} while {kk} has specific values on it')
                break

    # Put the values of the axis in the system
    for kk, vv in kwargs.items():
        # If its on multisectoral, put the value
        if kk not in ['dt', 'Tsim']:
            if type(vv) is list:
                self._dfields[kk]['value'] = len(vv)
                self._dfields[kk]['list'] = vv
            elif type(vv) in [float, int]:
                self._dfields[kk]['value'] = vv
                self._dfields[kk]['list'] = list(np.arange(vv))
            if verb:
                print(f"Now {kk} has {self._dfields[kk]['value']} sectors with names {self._dfields[kk]['list']}")
        # Else, we just change values
        else:
            self._dfields[kk]['value'] = vv

    self._dfields = _hub_set.set_shapes_values(self._dfields, self._dmisc['dfunc_order'])
    self._dargs = _hub_set.get_dargs_by_reference(self._dfields, self._dmisc['dfunc_order'])
    return self


def _set_fields(self, noreset=False, verb=config.get_current('_VERB'), **kwargs):
    """
    Set the fields of the parameters in the data structure.

    This function takes a set of keyword arguments, where each key is a parameter name and each value is the new value for the parameter. It updates the values in the data structure and returns the updated data structure.

    Parameters
    ----------
    noreset : bool, optional
        If `True`, the function does not reset the shapes and dimensions of the parameters. Default is `False`.
    verb : bool, optional
        If `True`, verbose output is enabled. Default is `_VERB`.
    **kwargs : dict
        The keyword arguments where each key is a parameter name and each value is the new value for the parameter.

    Returns
    -------
    self
        The updated data structure.
    """
    """
    # Get list of variables that might need a reshape
    # Exclude numerical parameters
    parametersandifferential = list(set(self.get_dfields(eqtype=['differential', None]))
                                    - set(['__ONE__', 'time'])
                                    - set(['nr', 'nx', 'dt', 'Tini', 'Tsim'] + list(self.get_dfields(eqtype=['size']))))

    # Determine where the value of each parameter is located
    # If the parameter is of type 'differential', its value is located in 'initial'
    # Otherwise, its value is located in 'value'
    direct = {k: 'initial' if self._dfields[k].get('eqtype', '') == 'differential'
              else 'value' for k in parametersandifferential}

    # Get the dimensions of each parameter
    dimname = {kk: [self._dfields[k2]['value'] for k2 in ['nx', 'nr'] + self._dfields[kk]['size']] for kk in parametersandifferential}

    # If 'noreset' is True, get the old value of each parameter from the current run
    # Otherwise, get the old value of each parameter from 'initial' or 'value'
    if noreset:
        it = self.dflags['run'][0]
        oldvalue = {}
        for kk in parametersandifferential:
            if direct[kk] == 'initial':
                oldvalue[kk] = self._dfields[kk]['value'][it, ...]
            else:
                oldvalue[kk] = self._dfields[kk]['value']
    else:
        oldvalue = {k: self._dfields[k][direct[k]] for k in parametersandifferential}  # Get the old value from 'initial' or 'value'
    """

    # Get list of variables that might need a reshape
    # Exclude numerical parameters
    parametersandifferential = list(set(self.get_dfields(eqtype=['differential', None]))
                                    - set(['__ONE__', 'time'])
                                    - set(['nr', 'nx', 'dt', 'Tini', 'Tsim'] + list(self.get_dfields(eqtype=['size']))))

    # Determine where the value of each parameter is located
    # If the parameter is of type 'differential', its value is located in 'initial'
    # Otherwise, its value is located in 'value'
    direct = {k: 'initial' if self._dfields[k].get('eqtype', '') == 'differential'
              else 'value' for k in parametersandifferential}

    # Get the dimensions of each parameter
    dimname = {kk: [self._dfields[k2]['value'] for k2 in ['nx', 'nr'] + self._dfields[kk]['size']] for kk in parametersandifferential}

    # If 'noreset' is True, get the old value of each parameter from the current run
    # Otherwise, get the old value of each parameter from 'initial' or 'value'
    if noreset:
        it = self.dflags['run'][0]
        self._dflags['noreset'][it]={}
        oldvalue = {}
        for kk in parametersandifferential:
            if direct[kk] == 'initial':
                oldvalue[kk] = self._dfields[kk]['value'][it, ...]
            else:
                oldvalue[kk] = self._dfields[kk]['value']
        
    else:
        oldvalue = {k: self._dfields[k][direct[k]] for k in parametersandifferential}



    newvalue = {}
    # Dissecate new value allocation
    for kk in parametersandifferential:
        if kk in kwargs.keys():
            v = kwargs[kk]
            OLDVAL = oldvalue[kk]
            # print(v,OLDVAL)
            if type(v) in [np.ndarray]:
                newvalue[kk] = _change_line(self, kk, v)
            elif type(v) in [list]:
                Ok = False
                try:
                    if np.prod([type(vv) in [float, int] for vv in v]):
                        newvalue[kk] = _change_line(self, kk, v)
                    elif np.shape(v) == np.shape(self._dfields[kk]['value'][0, 0, :, :]):
                        newvalue[kk] = _change_line(self, kk, v)
                    Ok = True
                except BaseException:
                    if verb:
                        print('issue on ', kk, v, 'strong interpreter used')
                if not Ok:
                    newvalue[kk] = __deep_set_fields(self, OLDVAL, v, kk)
            elif type(v) in [dict]:
                newvalue[kk] = __deep_set_fields(self, OLDVAL, v, kk)
            else:
                newvalue[kk] = kwargs[kk] + 0 * OLDVAL
        else:
            newvalue[kk] = oldvalue[kk]

    for k, v in newvalue.items():
        ifprint(verb, k, np.shape(v))
        if noreset:
            self._dflags['noreset'][it]={k:v}
            prev = self._dfields[k].get('shocks',{0:OLDVAL})
            self._dfields[k]['shocks']=prev
            self._dfields[k]['shocks'][it]=v
    # REINITIALIZE SHAPES AND DIMENSIONS
    if not noreset:
        for kk in parametersandifferential:
            if kk in kwargs.keys():
                self._dfields[kk][direct[kk]] = newvalue[kk]
        self._dfields = _hub_set.set_shapes_values(self._dfields, self._dmisc['dfunc_order'])
        self._dargs = _hub_set.get_dargs_by_reference(self._dfields, self._dmisc['dfunc_order'])
        self.reset()
    else:
        it = self.dflags['run'][0]
        for kk in parametersandifferential:
            if kk in kwargs.keys():
                if direct[kk] == 'initial':
                    self._dfields[kk]['value'][it, ...] = newvalue[kk]
                else:
                    self._dfields[kk]['value'] = newvalue[kk]
    return self


def _change_line(self, kk, v):
    """
    Change the line of a parameter in the data structure.

    This function takes a parameter name and a new value, and returns a new value that has the same shape as the original value in the data structure.

    Parameters
    ----------
    kk : str
        The name of the parameter to be changed.
    v : array_like
        The new value for the parameter.

    Returns
    -------
    ndarray
        The new value for the parameter, reshaped to have the same shape as the original value in the data structure.

    Notes
    -----
    The function first checks the size of the parameter in the data structure.
    If the first dimension is '__ONE__', it adds new dimensions to the end of 'v' until 'v' has 4 dimensions.
    If the second dimension is '__ONE__', it adds new dimensions to the beginning and the end of 'v' to make 'v' a 4D array with the third dimension corresponding to 'v'.
    Otherwise, it adds new dimensions to the beginning of 'v' to make 'v' a 4D array with the third and fourth dimensions corresponding to 'v'.

    Author
    ------
    Paul Valcke

    Date
    ----
    OLD
    """
    if self._dfields[kk]['size'][0] == '__ONE__':
        newv = np.array(v)
        while len(np.shape(newv)) < 4:
            newv = newv[:, np.newaxis] + 0
    elif self._dfields[kk]['size'][1] == '__ONE__':
        newv = np.array(v)
        newv = newv[np.newaxis, np.newaxis, :, np.newaxis] + 0
    else:
        newv = np.array(v)
        newv = newv[np.newaxis, np.newaxis, :, :] + 0
    return newv


def __deep_set_fields(self, OLDVAL, inpt, name):
    """
    Deeply set fields in a complex data structure.
    Hopefully you do not have to arrive here. 

    This function is used when a non-trivial construction of variable value is required.
    It updates the values in the data structure based on the input and returns a new data structure with the updated values.
    then transforms the region names into numbers, and finally updates the values in the original data structure.

    Parameters
    ----------
    OLDVAL : array_like
        The original data structure before the value change.
    inpt : dict or list
        The input data structure that contains the new values to be set.
        If it's a dict, the keys are the names of the fields to be updated and the values are the new values.
        If it's a list, it contains the names of the fields to be updated and the new values in a specific format.
    name : str
        The name of the field to be updated.

    Returns
    -------
    array_like
        A new data structure with the updated values.

    Raises
    ------
    Exception
        If the type of 'inpt' is not dict or list, or if there's inconsistency in the dimensions of the input values.

    Notes
    -----
    then transforms the region names into numbers, and finally updates the values in the original data structure.

    Author
    ------
    Paul Valcke

    Date
    ----
    OLD
    """

    # Initialize the dictionary that will store the decomposed input data structure.
    fullinfos = {}

    # If 'inpt' is a dict, it's easier to translate.
    if type(inpt) is dict:
        for k, v in inpt.items():
            # print(k,v,type(v))
            fullinfos[k] = v if type(v) is list else [v]

    # If 'inpt' is a list, decompose it.
    elif type(inpt) is list:
        # Decompose the list based on the type of the field to be updated.
        # The decomposed list will be stored in 'fullinfos'.
        # The details of the decomposition process are implemented in the '__decompose_scalist' function.
        if name in self.dmisc['dmulti']['scalar']:
            fullinfos = __decompose_scalist(fullinfos, inpt)

        elif name in self.dmisc['dmulti']['vector']:
            # check if the first elements are indexes for sector
            if type(inpt[0]) is list:  # Check if its a list of sector
                if inpt[0][0] in ['nx', 'nr']:
                    fullinfos[inpt[0][0]] = inpt[0][1:]
                else:
                    fullinfos['first'] = inpt[0]
                fullinfos = __decompose_scalist(fullinfos, inpt[1:])
            elif inpt[0] in self._dfields[self._dfields[name]['size']]['list']:  # Check if it's a sector name
                fullinfos['first'] = [inpt[0]]
                fullinfos = __decompose_scalist(fullinfos, inpt[1:])
            else:
                fullinfos = __decompose_scalist(fullinfos, inpt)

        elif name in self.dmisc['dmulti']['matrix']:
            # FIRST AXIS
            Found0, Found1 = False, False
            if (type(inpt[0]) is list and len(inpt) > 1):  # Check if its a list of sector
                fullinfos['first'] = inpt[0]
                Found0 = True
            elif inpt[0] in self._dfields[self._dfields[name]['size']]['list']:  # Check if it's a sector name
                fullinfos['first'] = [inpt[0]]
                Found0 = True
            if (Found0 and len(inpt) > 2):
                if type(inpt[1]) is list:  # Check if its a list of sector
                    fullinfos['second'] = inpt[1]
                    Found1 = True
                elif inpt[1] in self._dfields[self._dfields[name]['size']]['list']:  # Check if it's a sector name
                    fullinfos['second'] = [inpt[1]]
                    Found1 = True
            if not Found0:
                fullinfos = __decompose_scalist(fullinfos, inpt[2:])
            if (Found0 and not Found1):
                fullinfos = __decompose_scalist(fullinfos, inpt[1:])
            if Found1:
                fullinfos = __decompose_scalist(fullinfos, inpt[2:])
    else:
        # If the type of 'inpt' is not dict or list, raise an exception.
        raise Exception(f'We have no idea what category of size {name} is')

    print(fullinfos)

    # Transform region name into numbers
    for k in fullinfos.keys():  # For each axis
        if k not in ['value', 'first', 'second']:
            for ii, r in enumerate(fullinfos[k]):  # for each element
                if type(r) is str:
                    fullinfos[k][ii] = self._dfields[k]['list'].index(r)
        elif k in ['first', 'second']:
            for ii, r in enumerate(fullinfos[k]):  # for each element
                if type(r) is str:
                    ax = self._dfields[name]['size'][0 if k == 'first' else 1]
                    fullinfos[k][ii] = self._dfields[ax]['list'].index(r)

    print(fullinfos)

    # If 'fullinfos['value']' is not a list, convert it to a list.
    # Then convert it to a numpy array.
    if not bool(np.shape(fullinfos['value'])):
        fullinfos['value'] = [fullinfos['value']]
    fullinfos['value'] = np.array(fullinfos['value'])

    print(fullinfos)

    # Create a copy of 'OLDVAL' and convert it to float.
    newval = np.copy(OLDVAL).astype(float)

    # Check the consistency of the dimensions of the input values.
    # If there's inconsistency, raise an exception.
    # transform scalar keys into non-scalar if needed
    lens = [int(np.prod(np.shape(v))) for k, v in fullinfos.items()]
    check = [v != np.amax(lens) for v in lens if v != 1]
    if np.sum(check):
        raise Exception(f'INCONSISTENCY IN {name} dimensions !\n lens={lens} ')
    else:
        nx0 = np.arange(self._dfields['nx']['value']) if 'nx' not in fullinfos.keys() else [0]
        nr0 = np.arange(self._dfields['nr']['value']) if 'nr' not in fullinfos.keys() else [0]
        d10 = np.arange(self._dfields[self._dfields[name]['size'][0]]['value'])[:] if 'first' not in fullinfos.keys() else [0]
        d20 = np.arange(self._dfields[self._dfields[name]['size'][1]]['value'])[:] if 'second' not in fullinfos.keys() else [0]
        nx, nr, d1, d2 = np.meshgrid(nx0, nr0, d10, d20)
        nx = nx.reshape(-1)
        nr = nr.reshape(-1)
        d1 = d1.reshape(-1)
        d2 = d2.reshape(-1)
        for ii in range(len(nx)):
            newval[fullinfos.get('nx', nx[ii]),
                   fullinfos.get('nr', nr[ii]),
                   fullinfos.get('first', d1[ii]),
                   fullinfos.get('second', d2[ii])] = fullinfos['value']
    return newval


def __decompose_scalist(fullinfos, inpt):
    """
    Decompose the input list and update the 'fullinfos' dictionary with the axes shape and content.

    Parameters
    ----------
    fullinfos : dict
        The dictionary to be updated with the axes shape and content.
    inpt : list
        The input list to be decomposed. The last element is considered as the 'value'.
        The other elements define the axes. Each element can be a string or a list where the first element is a string.

    Returns
    -------
    dict
        The updated 'fullinfos' dictionary.

    Notes
    -----
    If an element of 'inpt' is a string, it's considered as a name of an axis and the corresponding value in 'fullinfos'
    is a range of indices up to the length of the last element of 'inpt'.
    If an element of 'inpt' is a list, the first element of the list is considered as a name of an axis and the remaining
    elements are the corresponding values in 'fullinfos'.

    Author
    ------
    Paul Valcke

    Date
    ----
    OLD
    """

    # If 'inpt' has only one element, there's no axes information to decompose.
    if len(inpt) == 1:
        pass

    # If 'inpt' has two elements, decompose the first one.
    elif len(inpt) == 2:
        # If the first element is a string, use it as a key in 'fullinfos' and create a range of indices as its value.
        if type(inpt[0]) is str:
            fullinfos[inpt[0]] = np.arange(len(inpt[-1]))
        # If the first element is a list, use its first element as a key in 'fullinfos' and the remaining elements as its value.
        else:
            fullinfos[inpt[0][0]] = inpt[0][1:]

    # If 'inpt' has more than two elements, decompose all elements except the last one.
    elif len(inpt) > 2:
        for subl in inpt[:-1]:
            # If 'subl' is a string, use it as a key in 'fullinfos' and create a range of indices as its value.
            if type(subl) is str:
                fullinfos[subl] = np.arange(len(inpt[-1]))
            # If 'subl' is a list, use its first element as a key in 'fullinfos' and the remaining elements as its value.
            else:
                fullinfos[subl[0]] = subl[1:]

    # If 'inpt' has no elements, print an error message.
    else:
        print('The system do not understand your input')

    # The last element of 'inpt' is considered as the 'value'.
    fullinfos['value'] = inpt[-1]

    return fullinfos


class setM:
    '''
    Class that contains all the methods to set fields, values and dimensions in the Hub object.


    Author
    ------
    Paul Valcke

    Date
    ----
    OLD    
    '''

    def __init__(self):
        super().__init__()
        # pass

    def copy(self):
        """Do a deep copy of the hub"""
        return copy.deepcopy(self)

    def set_name(self,
                 name: str):
        """
        Set a name for the hub
        """
        if type(name) != str:
            raise Exception(f'The name type is invalid ! Please use a string. you gave {name}')
        self._name = name

    def set_dpreset(self,
                    input,
                    preset=None,
                    verb=config.get_current('_VERB')):
        """
        Modify the dictionary of presets that can be loaded directly.

        The structure is the same as in model files. See the TUTORIAL model file for reference.

        Parameters
        ----------
        input : dict
            A dictionary with the following structure:
            {
                'name1': {
                    'fields': {
                        'key1': 'value1',
                        'key2': 'value2',
                        ...
                    },
                    'com': 'Message',
                    'plots': {
                        'plotname1': [{'kwargs1'}, {'kwargs2'}, ...],
                        'plotname2': [{'kwargs1'}, {'kwargs2'}, ...]
                    }
                },
                ...
            }
        preset : str, optional
            If provided, the function will load the preset with this name after modifying the dictionary.
        verb : bool, default=_VERB
            If `True`, verbose output is enabled.

        Returns
        -------
        str
            Error message if the input is not valid.

        Notes
        -----
        The function updates the 'presets' field of the `_dmodel` attribute with the input value,
        and then loads the preset if a preset name is provided.

        Examples
        --------
        >>> hub.dpreset(input_dict, preset='preset_name')

        Author
        ------
        Paul Valcke

        Date
        ----
        OLD
        """
        if type(input) is not dict:
            return 'Type of the input is wrong !'
        for kk, vv in input.items():
            if type(vv) is not dict:
                return 'input must be a dict of dict !'
            for keys in ['fields', 'com', 'plots']:
                if keys not in vv.keys():
                    return f'{keys} missing from the preset {kk}'
            for keys2 in vv.keys():
                if keys2 not in ['fields', 'com', 'plots']:
                    print(f'{keys2} in {kk} is not a field taken into account')

        if verb:
            print('OVERRIDE presets in dpreset')
        self._dmodel['presets'] = input

        if preset:
            self.set_preset(preset)

    def set_preset(self, input, verb=config.get_current('_VERB')):
        """
        Load a preset that is already defined in dpreset.

        This can either be defined in the model file or added by the user with set_dpreset.
        The preset must be a string. Use hub.get_available_presets() to get a list of available presets.

        Parameters
        ----------
        input : str
            The name of the preset to load.
        verb : bool, default=_VERB
            If `True`, verbose output is enabled.

        Raises
        ------
        Exception
            If `input` is not a valid preset name.

        Notes
        -----
        The function updates the 'preset' field of the `_dmodel` attribute with the input value,
        and then sets the fields of the object according to the preset.

        Examples
        --------
        >>> hub.get_presets() # return you the list of presets
        >>> hub.preset('preset_name')

        Author
        ------
        Paul Valcke

        Date
        ----
        OLD
        """
        if input not in self._dmodel['presets'].keys():
            raise Exception(f"{input} is not a valid preset name ! the preset name must be in {list(self._dmodel['presets'].keys())}")
        else:
            self._dmodel['preset'] = input
            self.set_fields(self, verb=verb, **self._dmodel['presets'][input]['fields'])
            self.dflags['preset'] = input

    def set_fields(self,
                   key: str = None,
                   value=None,
                   verb=config.get_current('_VERB'),
                   noreset: bool = False,
                   **kwargs):
        """
        Change the fields values in the Hub. 
        It can be the tensor dimensions or the values of the parameters.
        This method is written in a way that can accept a lot of different inputs, see the examples for more. 
        The function can also be used to create shock, discontinuity and user retroactions, when you do partial run

        Parameters
        ----------
        key: str
            See Notes
        value: any:     
            See Notes
        verb : bool, default= config value
            If `True`, verbose output is enabled.
        noreset : bool, default=False
            If `True`, the system will change values of the next iteration after a partial run.
        **kwargs : dict
            A dictionary of field names and new values. Used if `key` is `None`.

        Notes
        -----
        You can change:
        1. dimensions
            * 'Tsim' duration of the simulated time
            * 'dt'   duration of one timestep
            * 'nx'   number of systems in parallel
            * 'nr'   number of regions
            * number of sectors in a multisector object (typically 'Nprod','Nagents')
            If you bring a list of strings for a dimension (nx,nr,Nprod,Nagents...), the system will name the elements and allocate the right size.

        2. Parameter and differential equation initial values.
            If using 'noreset' after a partial run, the system will change values of the next iteration.
            You cannot change a state variable, but you can change what its value is deduced from.

        3. Do not change a same dimension twice without resetting the system


        Examples
        --------
        # Changing values when the structure is a scalar (no parrallel, no regions, no multisector/agents)
        To change only one field, you can do "set_dfields(key,values)"
        To change multiple fields at once you can do "set_dfields(**dict)" with dict={key1:values1, key2:... }

        # Setting dimensions
        * hub.set_fields('nr',['France','Germany','China']) will create 3 named regions
        * hub.set_fields('nr',54) will create 54 regions with their number as index
        * hub.set_fields('Nprod',100) will generate 100 productive sectors
        * hub.set_fields('Nprod',['Consumption','Capital','Mine','Energy','Food']) will generate 5 named sectors

        ## Setting values
        illustrations on a field 'alpha'
        * hub.set_fields('alpha',0)                                 #will put 0 for all the axes of alpha (parrallel, regions,multisector...)
        * hub.set_fields('alpha',[0.1,0.2])                         #will put 0.1 in the first parrallel system, 0.2 in the second
        * hub.set_fields('alpha',[['nr','France'],0.5])             #will put 0.5 in all parrallel systems, for the region named "France"
        * hub.set_fields('alpha',[['nr','France'],['nx',1],0.5])               #will put 0.5 in the parrallel 1, region "France"
        * hub.set_fields('alpha',[['nr',0],['nx',0,4],[0.5,0.2]])              #region 0, value 0.5 in parrallel 0, 0.2 in parrallel 4
        * hub.set_fields('alpha',[['nr','France','USA'],['nx',1],0.5])         #parrallel 1, 0.5 both in France and USA
        * hub.set_fields('alpha',{'nr':['France','USA'], 'nx':1, 'value':0.5}) #will do the same !

        if 'Z' is a multisectoral element as a vector of dimension 2
        * hub.set_fields('Z',[0,1])                         #will put [0,1] for all parrallel all regions
        * hub.set_fields('Z',[['nr',0],[0,1]])              #will put [0,1] for all parrallel in region 0
        * hub.set_fields('Z',[['nr',0,1],[0,1]])            #will put [0,1] for all parrallel in region 0 and 1
        * hub.set_fields('Z',[['nx',0],['nr',0,1],[0,1]])   #will put [0,1] for parrallel system 0, in region 0 and 1

        if 'M' is a matric of dimension 2,2
        * hub.set_fields('Z',[[0,1],[1,0]]) will put [[0,1],[1,0]] for all parrallel all regions
        * hub.set_fields('Z',np.eye(2)) will put [[1,0],[0,1]] for all parrallel all regions})
        * hub.set_fields(**{'MATRIX': {'first':['energy','capital'],
                                    'second':['mine','consumption'],
                                    'nr':0,
                                    'value':[0.5,0.22]}})
        * hub.set_fields(**{'MATRIX': [['energy','capital'],['mine','consumption'],['nr',0],[0.5,0.22]]})
        * hub.set_fields(**{'MATRIX': [['energy','capital'],['mine','consumption'],[0.5,0.22]]})
        * hub.set_fields(**{'MATRIX': [['energy','capital'],0.22]})

        Multiple changes:
        dictchange={
                'Tsim':40,
                'Nprod': ['Consumption','Capital'],
                'nx':10,
                'alpha':np.linspace(0,0.02,10),
                'n':0.025,
                'phinull':0.1
                }
        hub.set_fields(**dictchange)

        Author
        ------
        Paul Valcke

        Date
        ----
        2023-09-01    
        """
        # Take minimal changes
        if (key is not None and value is not None):
            kwargs[key] = value

        # DECOMPOSE INTO SIZE AND VALUES #######
        setofdimensions = set(['nr', 'nx', 'dt', 'Tsim'] + list(self.get_dfields(eqtype=['size'])))
        diffparam = set(self.get_dfields(eqtype=['differential', None])) - set(['__ONE__', 'time']) - setofdimensions

        dimtochange = {kk: vv for kk, vv in kwargs.items() if kk in list(setofdimensions)}
        fieldtochange = {kk: vv for kk, vv in kwargs.items() if kk in list(diffparam)}
        wrongfields = [kk for kk in kwargs.keys() if kk not in list(dimtochange.keys()) + list(fieldtochange.keys())]

        # Check if dimensions are changed
        Rdim = self.get_dfields(keys=dimtochange.keys())
        ignored = [k for k, v in dimtochange.items() if (v == Rdim[k]['value'] or v == Rdim.get('list', []))]
        for k in ignored:
            wrongfields.append(k)
            del dimtochange[k]

        if (noreset and len(dimtochange)):
            raise Exception(f'ERROR: you cannot change dimensions in the middle of a run!. you asked for: {dimtochange}')

        if verb:
            print('')
            if len(list(dimtochange.keys())):
                print(f'Changing Dimensions: {list(dimtochange.keys())}')
            if len(list(fieldtochange.keys())):
                print(f'Changing Fields: {list(fieldtochange.keys())}')
            if len(list(wrongfields)):
                print(f'Changes Ignored:{wrongfields}')

        # SEND IT TO THE PIPE ###################
        if len(dimtochange  .keys()):
            _set_dimensions(self, verb, **dimtochange)
        _set_fields(self, noreset, verb, **fieldtochange)
