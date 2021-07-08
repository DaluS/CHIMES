# -*- coding: utf-8 -*-
"""
Here we define the parameters and set of equation for a model of type 'GK'

All parameters can have value:
    - None: set to the default value found in _def_fields.py
    - scalar: int or float
    - list or np.ndarray used for benchmarks
    - function (callable): in that can it will be treated as a variable
                            the function will be called at each time step

"""


_DPARAM = {

    # ---------
    # Fixed-value parameters
    'r': None,
    'k0': None,
    'k1': None,
    'k2': None,
    'alpha': None,
    'delta': None,
    'beta': None,
    'nu': None,

    # ---------
    # functions

    # former variables
    'a': {
        'value': lambda alpha=0, a=0: alpha * a,
        'com': 'Exogenous technical progress as an exponential',
        'eqtype': 'differential',
    },
    'N': {
        'value': lambda beta=0, N=0: beta*N,
        'com': 'Exogenous population as an exponential',
        'eqtype': 'differential',
    },
    'K': {
        'value': lambda I=0, K=0, delta=0: I - K*delta,
        'com' : 'Capital evolution from investment and depreciation',
        'eqtype': 'differential',
    },
    'W': {
        'value': lambda W=0, philips=0: W * philips,
        'com': 'Wage evolution through philips curve',
        'type': 'differential',
    },
    'D': {
        'value': lambda I=0, Pi=0: I - Pi,
        'com' : 'Debt as Investment-Profit difference',
        'type': 'differential',
    },

    # Intermediary computed but not stored
    'Y': {
        'value': lambda K=0, nu=0: K / nu,
        'type': 'intermediary',
    },
    'L': {
        'value': lambda K=0, a=0, nu=0: K / (a * nu),
        'type': 'intermediary',
    },
    'Pi': {
        'value': lambda Y=0, W=0, L=0, r=0, D=0: Y - W*L - r*D,
        'type': 'intermediary',
    },
    'lambda': {
        'value': lambda L=0, N=0: L / N,
        'type': 'intermediary',
    },
    'omega': {
        'value': lambda W=0, L=0, Y=0: W * L / Y,
        'type': 'intermediary',
    },
    'philips': {
        'value': lambda phi0=0,  phi1=0, lamb=0: -phi0 + phi1 / (1-lamb)**2,
        'type': 'intermediary',
    },
    'kappa': {
        'value': lambda k0=0, k1=0, k2=0, Pi=0, Y=0: k0 + k1 * np.exp(k2*Pi/Y),
        'type': 'intermediary',
    },
    'I': {
        'value': lambda Y=0, kappa=0: Y * kappa,
        'type': 'intermediary',
    },

    # auxiliary, not computed, but can be retrieved at the end
    'g': {
        'value': lambda omega=0, nu=0, delta=0: (1-omega) / nu - delta,
        'type': 'auxilliary',
    },
    'd': {
        'value': lambda D=0, Y=0: D / Y,
        'type': 'auxilliary',
    },
    'pi': {
        'value': lambda omega=0, r=0, d=0: 1 - omega - r*d,
        'type': 'auxilliary',
    },
    'i': {
        'value': lambda Y=0: Y*0,
        'type': 'auxilliary',
    },
    'phi0': {
        'value': lambda phinull=0: phinul / (1- phinul**2),
        'type': 'auxilliary',
    },
    'phi1': {
        'value': lambda phinull=0: phinul**3 / (1- phinul**2),
        'type': 'auxilliary',
    },
}


# #############################################################################
# #############################################################################
#                       Add set of pre-defined parameter values
# #############################################################################


