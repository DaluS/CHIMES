import numpy as np
from .._core_functions._distribution_generator import generate_dic_distribution as _generate_dic_distribution
from .._config import config  # _SOLVER
from .._core_functions import _solvers
from .._core_functions import _hub_check
from ..plots.compare_hubs import compare_hubs
from typing import Union

import copy

"""
This file contains the methods to do calculations on the Hub object.

Author
------
Paul Valcke

Date
----
Updated January 2024
"""


def _cn(y, n):
    '''
    calculate cn fourier coefficients for one cycle, not normalized
    '''
    return np.array([np.abs(np.mean(y * np.exp(-1j * 2 * i * np.pi * np.linspace(0, 1, len(y))))) for i in range(n)])


class calculateM:
    def __init__(self):
        pass

    def run_sensitivity(self,
                        keys='__ALL__',
                        std=0.01,
                        stdmode='relative',
                        distribution: str = 'lognormal',
                        N: int = 10,
                        combined_run=True,
                        Noutput=500,
                        verb: bool = False
                        ) -> dict:
        """
        Computes runs in parallel, with parameter/initial values taken from a distribution. 
        The distributions are centered around the hub values, with their width controlled by `std`.
        The output is a dictionary of Hub, the key being the field that is taken in its distribution. 

        Parameters
        ----------
        keys : str or list or tuple or dict, optional
            All fields (parameters/differential) that are going to have a distribution associated to their value. 
            If `__ALL__`, all fields are covered. If key is a list of str, all the fields inside are included. 
            If key is a tuple of str, all the fields inside are excluded. 
            If keys is a dictionary with numerical values, the value is read as individual std parameter for each key.
            Default is '__ALL__'.
        std : float, optional
            Variation size for each field. Default is 0.01.
        stdmode : str, optional
            If `relative`, the distribution is `x -> x*(1+noise)`, in which noise has a standard deviation of std and a mean of zero.
            If not, the distribution is `x -> x+noise`, in which noise has a standard deviation of std and a mean of zero.
            Default is 'relative'.
        distribution : str, optional
            The shape of the distribution (normal, uniform, lognormal). Default is 'lognormal'.
        N : int, optional
            Number of sampling done for each key. Default is 10.
        combined_run : bool or str, optional
            If 'independant', it is moving one parameter and looking at its effects sequentially.
            If 'additive', it is moving all parameters at the same time, and do not run anything else.
            If True, it is doing both. Default is True.
        Noutput : int, optional
            Reinterpolate the output to Noutput points for smaller output size files. Default is 500.
        verb : bool, optional
            Verbose of the function. Default is False.

        Returns
        -------
        dict
            A dictionary of Hub, the key being the field that is taken in its distribution.

        NOTES
        -----
        - The distribution is centered around the hub values, with their width controlled by `std`.
        - The output is a dictionary of Hub, the key being the field that is taken in its distribution.
        - The calculations are sequential for each key, so it can take time if there is a lot of key.
        - An improvement would be to create one giant hub then cut it in splices


        Raises
        ------
        Exception
            If the keys could not be read.

        Author
        ------
        Paul Valcke

        Date
        ----
        Updated January 2024
        """

        # KEEPING THE STATE OF THE SYSTEM
        Base0 = self.Extract_preset(t=0)  # The state of the system
        Base0 = {k: v for k, v in Base0.items() if k in self.dmisc['dfunc_order']['differential'] +
                 list(set(self.dmisc['dfunc_order']['parameters']) - set(['Tsim', 'Tini', 'dt', 'nx', 'nr', 'Nprod', '__ONE__']))}

        # SELECTING WHICH FIELDS SHOULD BE EXPLORED
        if keys == '__ALL__':
            Base = Base0
        elif type(keys) is str:
            Base = {keys: Base0[keys]}
        elif type(keys) is list:
            Base = {k: v for k, v in Base0.items() if k in keys}
        elif type(keys) is tuple:
            Base = {k: v for k, v in Base0.items() if k not in keys}
        elif type(keys) is dict:
            Base = {k: v for k, v in Base0.items() if k in keys.keys()}
        else:
            raise Exception(f'Keys could not be read ! {keys}')
        if verb:
            print('Fields considered :', Base)

        # MANAGING MULTIPLE RELATIVE STD
        if type(std) in [int, float]:
            std = {k: std * v if stdmode == 'relative' else std for k, v in Base.items()}
        if keys is dict:
            std = {k: std[k] * v if stdmode == 'relative' else std[k] for k, v in Base.items()}
        if verb:
            print('Variances considered :', std)

        # GENERATING THE DISTRIBUTIONS
        Newdict = {k: {'mu': v,
                       'sigma': std[k],
                       'type': distribution
                       } for k, v in Base.items()}

        Globalset = _generate_dic_distribution(Newdict, dictpreset={}, N=N)
        if verb:
            print('Data sent:')
            for k, v in Globalset.items():
                if k != 'nx':
                    print(k, v.reshape(-1))

        dHub = {}
        # Studying combination
        if combined_run in [True, 'additive']:
            # Calculating the Global sensitivity
            dHub['_COMBINED_'] = self.copy()
            dHub['_COMBINED_'].set_fields(**Base, verb=False)
            dHub['_COMBINED_'].set_fields(**Globalset, verb=False)
            dHub['_COMBINED_'].run(NtimeOutput=Noutput, verb=verb)
            dHub['_COMBINED_'].calculate_StatSensitivity()

        # Sequential parameter
        if combined_run in [True, 'independant']:
            for k, v in Globalset.items():
                if k != 'nx':
                    if verb:
                        print('On variable', k)

                    dHub[k] = self.copy()
                    dHub[k].set_fields(**Base, verb=False)
                    dHub[k].set_fields('nx', N, verb=False)
                    dHub[k].set_fields(k, v, verb=False)
                    dHub[k].run(NtimeOutput=Noutput, verb=verb)
                    dHub[k].calculate_StatSensitivity()
        """
        else: 
            FullHub = self.copy()
            FullHub.set_fields(**{'nx': N*(len(Globalset.keys())+1),
                                  })
            for i,k in enumerate(Globalset.keys()):
                FullHub.set_fields(**{k:})
        """
        return dHub

    def calculate_StatSensitivity(self):
        """
        Calculate statistical measures for each variable when there are multiple runs in parallel.

        This method will associate to each variable a dict 'sensitivity' in dfields, with statistical measures.
        The statistical measures are: mean, stdv, min, max, median.

        The elements are not available in get_dfields(), with the architecture [key]['sensitivity'][region_number][time][statistic].

        Notes
        -----
        It's not an very elegant implementation, and should be rewritten someday when exploring deeply multisectoral systems

        Author
        ------
        Paul Valcke

        Date
        ----
        Updated January 2024
        """

        # Define the equation types
        leq = ['differential', 'statevar']

        # Get the parameters
        R0 = self.get_dfields()
        R = self.get_dfields(returnas=dict, eqtype=leq)

        # Loop over the keys in the parameters
        for ke in R.keys():
            self._dfields[ke]['sensitivity'] = [
                {
                    kx: {
                        'mean': np.mean(val, axis=1),
                        'stdv': np.std(val, axis=1),
                        'min': np.amin(val, axis=1),
                        'max': np.amax(val, axis=1),
                        'median': np.median(val, axis=1)
                    }
                    for ii, kx in enumerate(R0[R0[ke]['size'][0]].get('list', [0]))
                    for val in [R[ke]['value'][:, :, kr, ii, 0]]
                }
                for kr in range(R0['nr']['value'])
            ]

        # Set the 'sensitivity' flag to True
        self._dflags['sensitivity'] = True

    def calculate_ConvergeRate(self, finalpoint: dict, Region=0):
        """
        Calculate the convergence rate of each trajectory to a final point.

        This function calculates the evolution of the distance of each trajectory to
        the final point. It then fits the trajectory with an exponential and returns
        the rate of decrease of this exponential (the bigger the more stable).

        While close the the equilibrium, it's natural that the trajectories are exponential, 
        it's not the case further from equilibrium. 
        Also, the norm is here a raw addition. An equivalent function with dimension ponderation could help in certain cases.

        Parameters
        ----------
        finalpoint : dict
            The final point to which the trajectories are converging. It should be
            in the format:
                { 'field1' : number1,
                'field2' : ['sectorname',number2],
                'field3' : number3}
        Region : int, optional
            The region of interest. Default is 0.

        Returns
        -------
        ConvergeRate : ndarray
            The convergence rate for each system.

        Notes
        -----
        The function calculates the distance of each trajectory to the final point
        and fits it with an exponential. The rate of decrease of this exponential
        is then returned.

        Author
        ------
        Paul Valcke

        Date
        ----
        Updated January 2024
        """
        # Final step studies ##################
        R = self.get_dfields(
            key=[k for k in finalpoint] + ['time'], returnas=dict)

        # Take into account multisectoriality
        sector = {k: 0 for k in finalpoint.keys()}
        for k, v in finalpoint.items():
            if type(v) is list:
                sector[k] = v[1]
                finalpoint[k] = v[0]

        Coords = [R[k]['value'][:, :, Region, sector[k], 0] - finalpoint[k] for k in finalpoint.keys()]
        dist = np.linalg.norm(Coords, axis=0)
        t = R['time']['value'][:, 0, 0, 0, 0]

        # Fit using an exponential ############
        Nsys = np.shape(dist)[1]
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

    def calculate_Cycles(self, ref=None, n=10):
        """
        Calculate the cycles properties for all variables.

        For each variable, it calculates the cycles properties. The reference variable
        on which the time of cycles is determined by default the variable detects cycles in itself.
        The fields which are calculated are : 
            ['reference', 'period_indexes', 'period_T_intervals', 't_mean_cycle',
                'period_T', 'meanval', 'medval', 'stdval', 'minval', 'maxval']


        Parameters
        ----------
        ref : str, optional
            The reference variable on which the time of cycles is determined.
            By default the variable detects cycles in itself.
        n : int, optional
            Number of harmonics calculated in Fourier decomposition. Default is 10.

        Notes
        -----
        The function updates the 'cycles' field of the `_dfields` attribute with the calculated cycles properties,
        and then sets the 'cycles' flag of the `_dflags` attribute to True.

        Author
        ------
        Paul Valcke

        Date
        ----
        OLD
        """

        # Define the equation types and fields
        leq = ['differential', 'statevar']
        fields = ['reference', 'period_indexes', 'period_T_intervals', 't_mean_cycle',
                  'period_T', 'meanval', 'medval', 'stdval', 'minval', 'maxval']

        # Get the parameters and calculate the cycles properties for each variable
        for var, dic1 in self.get_dfields(returnas=dict, eqtype=leq).items():
            tempval = np.reshape(dic1['value'], (np.shape(dic1['value'])[0], -1))
            self._dfields[var]['cycles'] = [{k: [] for k in fields} for _ in range(np.shape(tempval)[1])]

        # Update the 'cycles' field of the variable in the parameters
        for var, dic1 in self.get_dfields(returnas=dict, eqtype=leq).items():
            tempval = np.reshape(dic1['value'], (np.shape(dic1['value'])[0], -1))
            for idx in range(np.shape(tempval)[1]):
                self._dfields[var]['cycles'][idx]['reference'] = ref if ref else var
                self._FillCycles(var, tempval[:, idx], ref if ref else var, idx, n=n)

        # Reverse the cycles dictionary and set the 'cycles' flag to True
        self._reverse_cycles_dic()
        self._dflags['cycles'] = True

    def _FillCycles(self, var, tempval, ref='employment', id=0, n=10):
        '''
        it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself

        var : name of the variable we are working on
        ref : reference for the oscillations detections
        '''

        # Get the new dictionnary to edit
        dic = self._dfields[var]
        dic1 = self._dfields[var]['cycles'][id]

        # check if reference has already calculated its period
        # the reference has cycle and this cycle has been calculated on itself
        ready = False
        if 'cycles' in self._dfields[ref].keys():
            dic2 = self._dfields[ref]['cycles'][id]
            if (dic2['reference'] == ref and len(dic2.get('period_indexes', [])) >= 1):
                # We can take the reference as the base
                ready = True
        # If there is no good reference
        # We calculate it and put
        if not ready:
            self._findCycles(ref, tempval, id)
            dic2 = self._dfields[ref]['cycles'][id]

        for key in ['period_indexes', 'period_T_intervals',
                    't_mean_cycle', 'period_T']:
            dic1[key] = copy.copy(dic2[key])

        tim = self._dfields['time']['value'][:, 0, 0, 0]
        dic1['period_T_intervals'] = [[tim[idx[0], 0], tim[idx[1], 0]]
                                      for idx in dic1['period_indexes']]
        dic1['t_mean_cycle'] = [
            (t[0] + t[1]) / 2 for t in dic1['period_T_intervals']]
        dic1['period_T'] = [
            (t[1] - t[0]) for t in dic1['period_T_intervals']]
        dic1['frequency'] = [
            1 / (t[1] - t[0]) for t in dic1['period_T_intervals']]

        # Fill for each the characteristics
        values = tempval
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
        dic1['Coeffs'] = [Coeffs[i][1:] / Coeffs[i][1]
                          for i in range(len(Coeffs))]
        dic1['Harmonicity'] = [np.sum(Coeffs[i][1:]**2) / np.sum(Coeffs[i]**2)
                               for i in range(len(Coeffs))]

    def _findCycles(self, refval, tempval, idx=0):
        '''
        Detect all positions of local maximums and the time that is linked
        '''
        # initialisation
        periods = []
        id1 = 1

        dic1 = self._dfields[refval]['cycles'][idx]
        val = tempval

        # identification loop
        while id1 < len(val) - 2:
            if (val[id1] > val[id1 - 1] and val[id1] > val[id1 + 1]):
                if np.abs(val[id1] - val[id1 - 1]):
                    periods.append(1 * id1)
            id1 += 1

        # Fill the formalism
        self._dfields[refval]['cycles'][idx]['period_indexes'] = [
            [periods[i], periods[i + 1] + 1] for i in range(len(periods) - 1)
        ]
        tim = self._dfields['time']['value']
        dic1 = self._dfields[refval]['cycles'][idx]
        dic1['period_T_intervals'] = [[tim[idx[0]], tim[idx[1]]]
                                      for idx in dic1['period_indexes']]
        dic1['t_mean_cycle'] = [
            (t[0] + t[1]) / 2 for t in dic1['period_T_intervals']]
        dic1['period_T'] = [
            (t[1] - t[0]) for t in dic1['period_T_intervals']]
        dic1['reference'] = refval

    def _reverse_cycles_dic(self):
        leq = ['differential', 'statevar']
        for var, dic1 in self.get_dfields(returnas=dict, eqtype=leq).items():
            c = dic1['cycles']
            newcycles = {k: [] for k in c[0].keys()}
            for i in range(len(c)):
                for k in c[i].keys():
                    newcycles[k].append(c[i][k])

            self._dfields[var]['cycles_bykey'] = copy.deepcopy(newcycles)

    def reset(self):
        """
        Reinitialize all calculated values, keeping only the loaded model file and parameters/initial conditions.

        This function performs the following steps:
        1) Resets differential equations and state variables to NaN.
        2) Resets initial values for differential equations to their initial conditions.
        3) Recomputes initial values for function-parameters and state variables.
        4) Reinitializes flags to their default states.

        Notes
        -----
        The function updates the 'value' field of the `_dfields` attribute for each differential equation, state variable, and function-parameter.
        It also updates the 'run', 'sensitivity', 'convergence', 'multiregional', 'Parrallel', and 'cycles' flags of the `_dflags` attribute.
        If an error occurs during the re-computation of the initial value for a state variable, an exception is raised with a detailed error message.

        Author
        ------
        Paul Valcke

        Date
        ----
        OLD
        """

        # reset ode variables
        for k0 in self.get_dfields(eqtype=['differential', 'statevar'], returnas=list):
            self._dfields[k0]['value'][...] = np.nan

        # Reset initial for ode
        for k0 in self.get_dfields(eqtype=['differential'], returnas=list):
            self._dfields[k0]['value'][0, ...] = self._dfields[k0]['initial']
        self._dfields['time']['value'][0, ...] = self._dfields['Tini']['value']

        # recompute initial value for function-parameters
        pstate = self._dmisc['dfunc_order']['parameter']
        for k0 in pstate:
            dargs = {
                k1: self._dfields[k1]['value']
                for k1 in self._dfields[k0]['args'][None]
            }
            dargs.update({
                k1: self._dfields[k1]['value']
                for k1 in self._dfields[k0]['args']['parameter']
            })
            self._dfields[k0]['value'] = self._dfields[k0]['func'](**dargs)

        # recompute inital value for statevar
        lstate = self._dmisc['dfunc_order']['statevar']
        ERROR = ''
        for k0 in lstate:
            kwdargs = {
                k1: v1[0, ...] if k1 in self._dmisc['dfunc_order']['statevar'] + self._dmisc['dfunc_order']['differential'] else v1
                for k1, v1 in self._dargs[k0].items()
            }
            try:

                # run function
                self._dfields[k0]['value'][0, ...] = (
                    self._dfields[k0]['func'](**kwdargs)
                )

            except BaseException as Err:
                ERROR += f'You have a problem on your object sizes for {k0} (shape of kwargs:)\n {[(k,np.shape(v)) for k,v in kwdargs.items()]} \n {Err}\n'
        if len(ERROR):
            for k0 in lstate:
                print(k0, np.shape( self._dfields[k0]['value']))
            for k0 in pstate:
                print(k0, np.shape( self._dfields[k0]['value']))
            raise Exception('\n' + ERROR + '\nALLOCATION CANNOT BE DONE,CHECK YOUR MODEL FILE !')

        # set run to False
        self._dflags['sensitivity'] = False
        self._dflags['convergence'] = False
        # self._dflags['multisectoral'] = False
        self._dflags['multiregional'] = True if self._dfields['nr']['value'] > 1 else False
        self._dflags['Parrallel'] = True if self._dfields['nx']['value'] > 1 else False
        self._dflags['cycles'] = False
        self._dflags['run'] = [0, 0]
        self._dflags['reinterpolated'] = False

    def run_uncertainty(
        self,
        uncertainty: float = 1,
        distribution: str = 'normal',
        N: int = 10,
        NtimeOutput: int = False,
        verb=0.1,
    ):
        """
        Run a simulation with uncertainty to assess system robustness. 
        Use it typically to assess the range of your simulation you can claim accurate given exact informations.

        This function is a mix between sensitivity analysis and a regular run. It creates N systems in parallel, 
        so `nx` must be 1 to begin with. It generates variations based on a specified distribution and runs the simulation.

        Parameters
        ----------
        uncertainty : float, optional
            Percentage of variation for each field. Default is 1 (1%).
        distribution : str, optional
            Type of distribution for generating variations. Default is 'normal'.
        N : int, optional
            Number of simulations to run. Default is 10.
        NtimeOutput : int, optional
            Number of time points for output. Default is False.
        verb : float, optional
            Verbosity level for run logging. Default is 0.1.

        Notes
        -----
        The function first checks the value of `nx` and raises an exception if it's not 1. It then saves the state of the system 
        and generates the distributions for the variations. It sets the fields with the generated distributions and runs the simulation. 
        Finally, it calculates the statistical sensitivity.

        Author
        ------
        Paul Valcke

        Date
        ----
        OLD
        """
        R = self.get_dfields()
        if R['nx']['value'] not in [1, N]:
            raise Exception("Error: you can't do parrallel run with uncertainty !")

        # KEEPING THE STATE OF THE SYSTEM
        Base = self.Extract_preset(t=0)  # The state of the system
        Base = {k: v for k, v in Base.items() if k in self.dmisc['dfunc_order']['differential'] +
                list(set(self.dmisc['dfunc_order']['parameters']) - set(['Tsim', 'Tini', 'dt', 'nx', 'nr', 'Nprod', '__ONE__']))}

        # GENERATING THE DISTRIBUTIONS
        Newdict = {k: {'mu': v,
                       'sigma': uncertainty * 0.01 * v,
                       'type': distribution,
                       } for k, v in Base.items()}
        self.set_fields(**_generate_dic_distribution(Newdict, dictpreset={}, N=N), verb=False)
        self.run(NtimeOutput=NtimeOutput, verb=verb)
        self.calculate_StatSensitivity()

    def run(
        self,
        NtimeOutput=False,
        NstepsInput=False,
        verb=0.1,
        ComputeStatevarEnd=False,
        solver=config.get_current('_SOLVER'),
        steps=False,
    ):
        """
        Run the simulation using an explicit RK4 (by default, can be changed). 

        This function computes each time step from the previous one using parameters, differentials equations, 
        and intermediary functions in specified func_order.

        Parameters
        ----------
        NtimeOutput : bool, optional
            If True, reinterpolate the simulation for detailed output. Default is False.
        NstepsInput : bool, optional
            If True, modify dt to achieve NstepsInput for simulating Tsim years. Default is False.
        verb : float, optional
            Verbosity level for logging. Default is 0.1.
        ComputeStatevarEnd : bool, optional
            If True, recompute all state variables at the end. Default is False.
        solver : str, optional
            Solver method, either 'rk1' or 'rk4'. Default is 'rk4'.
        steps : bool, optional
            Number of steps to run the simulation. Default is False.

        Notes
        -----
        The function first checks the solver name and raises an exception if it's not 'rk1' or 'rk4'. 
        If NstepsInput is True, it sets the 'dt' field to the value of 'Tsim' divided by NstepsInput. 
        It then checks the inputs and resets the variables if necessary. 
        It starts the time loop and runs the solver. 
        If an error occurs during the solver run, it sets the 'run' flag to [0, 0.] and raises the error.

        Author
        ------
        Paul Valcke
        Original : Didier Vezinet

        Date
        ----
        OLD
        """
        # Special run for reluncertainty
        if solver not in ['rk1', 'rk4']:
            raise Exception(f'solver name {solver} unknown ! Try rk1 or rk4')

        if NstepsInput:
            self.set_fields('dt', self.dfields['Tsim']['value'] / NstepsInput, verb=verb)

        # check inputs
        dverb = _hub_check._run_verb_check(verb=verb)

        if self.dflags['run'][0] >= self.dfields['nt']['value']-1:
            print('Already run: reset and run')
            self._dflags['run'] = [0, 0.]
            self.set_fields(**{}, verb=False)
            self.reset()

        # reset variables
        if (not steps and self.dflags['run'][0] == 0):
            self.set_fields(**{}, verb=False)
            self.reset()
            steps = self.dfields['nt']['value']
            stepini = 0
        elif not steps:
            steps = self.dfields['nt']['value']
            stepini = self._dflags['run'][0]
        else:
            steps = self._dflags['run'][0] + steps + 1
            stepini = self._dflags['run'][0]
        steps = np.min((steps, self.dfields['nt']['value']))

        # start time loop
        try:
            nt, tmax = _solvers.solve(
                dfields=self._dfields,
                dmisc=self._dmisc,
                stepini=stepini,
                stepend=steps,
                dverb=dverb,
                ComputeStatevarEnd=ComputeStatevarEnd,
                solver=solver,
            )

            self._dflags['run'] = [nt - 1, tmax]
            self._dmisc['solver'] = solver

            if (steps == nt and NtimeOutput):
                self.reinterpolate_dfields(NtimeOutput)

        except Exception as err:
            self._dflags['run'] = [0, 0.]
            raise err

    def reinterpolate_dfields(self, N=100):
        """
        Reinterpolate all values in `dfields` if the system has run.

        This function is typically used to generate lighter plots. It takes the current state of the system and reinterpolates 
        all values in `dfields` to a new number of points. The function requires a reset before a run to reallocate space.

        Parameters
        ----------
        N : int, optional
            The number of points to reinterpolate to. Default is 100.

        Returns
        -------
        None

        Notes
        -----
        The function first gets the current time and state variables from `dfields`. It then loops over each state variable and 
        differential equation, reinterpolating the values to the new number of points. The reinterpolated values are reshaped 
        to match the original shape and stored back in `dfields`. Finally, the 'run' flag and 'nt' and 'dt' fields in `dfields` 
        are updated to reflect the new number of points.

        Author
        ------
        Paul Valcke
        Original : Didier Vezinet

        Date
        ----
        OLD
        """
        P = self._dfields
        t = P['time']['value']
        for k in self._dmisc['dfunc_order']['statevar'] \
                + self._dmisc['dfunc_order']['differential']:
            v = P[k]['value']
            prevshape = np.shape(v)
            v2 = v.reshape(P['nt']['value'], -1)
            newval = np.zeros([N, np.shape(v2)[1]])
            newt = np.linspace(t[0, 0, 0, 0], t[-1, 0, 0, 0], N)
            for i in range(np.shape(newval)[1]):
                newval[:, i] = np.interp(newt[:, 0], t[:, 0, 0, 0, 0], v2[:, i])
            newshape = [N] + list(prevshape[1:])
            self._dfields[k]['value'] = newval.reshape(newshape)

        self.dflags['run'][0] = N - 1
        self.dflags['reinterpolated'] = True
        self.dfields['nt']['value'] = N
        self.dfields['dt']['value'] = self.dfields['Tsim']['value'] / N

    def compare_presets(self,
                        variables: Union[list, tuple],
                        **kwargs):
        '''
        Will run all preset of `modelname`, then plot all variables in `variables`, using `Plots.compare_hubs`.
        the kwargs are directly transfered to compare_hubs`
        '''

        dhub = {}
        lpreset = self.get_presets(returnas=dict)

        for preset in lpreset:
            dhub[preset] = self.copy()
            dhub[preset].set_preset(preset)
            dhub[preset].set_name(preset)
            dhub[preset].run()

        compare_hubs(list(dhub.values()),
                     variables=variables,
                     returnFig=True
                     ** kwargs)
