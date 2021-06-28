# -*- coding: utf-8 -*-



import _def_parameters
import _utils


class Solver():
    """ Generic class
    """

    _paramset = 'v0'


    def __init__(self):
        pass

    def update_dinput(self):

        # Update dynamical parameters                                  
        self.__dinput['Tstore']['value'] = self.__dinput['dt']['value']
        self.__dinput['Nt']['value'] = int(
            self.__dinput['Tmax']['value']/self.__dinput['dt']['value']
        )
        self.__dinput['Ns']['value'] = int(
            self.__dinput['Tmax']['value']/self.__dinput['Tstore']['value']
        ) + 1

    def set_dinput(self, dinput=None):

        if dinput is None:
            dinput = self._paramset

        if isinstance(dinput, str):
            # In this case, dinput is the name of a parameters preset
            self.__dinput = _def_parameters.get_params(paramset=dinput)

        self.update_dinput()

    def get_dinput(self, verb=None, returnas=None):
        """ Return a copy of the input parameters dict

        Return as:
            - False: do not return
            - dict: dict
            - str: message to be printed
            - 'DataGFrame': a pandas DataFrame
            - np.ndarray: a dict of np.ndarrays

        if verb = True the message is automatically printed

        """

        if verb is True or returnas is str:
            lcol = ['key', 'value', 'units', 'group', 'comment']
            lar = [
                tuple([
                    k0,
                    str(v0['value']),
                    str(v0['units']),
                    v0['group'],
                    v0['com'],
                ])
                for k0, v0 in self.__dinput.items()
            ]
            msg = _utils._get_summary(
                lar=[lar],
                lcol=[lcol],
                verb=verb,
                returnas=returnas,
            )
            if returnas is str:
                return msg
        elif returnas is dict:
            # return a copy of the dict
            return {k0: dict(v0) for k0, v0 in self.__dinput.items()}


    def initialize(self):
        pass













