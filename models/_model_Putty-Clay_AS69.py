# -*- coding: utf-8 -*-
"""
Here we define the parameters and set of equation for a model of type 'Putty-Clay'

All parameters can have value:
    - None: set to the default value found in _def_fields.py
    - scalar: int or float
    - list or np.ndarray used for benchmarks
    - function (callable): in that can it will be treated as a variable
                            the function will be called at each time step

"""


import numpy as np

n_kl = 101
kl_ratios = 10**np.linspace(3, 8, n_kl)

# ---------------------------
# user-defined function order (optional)

_FUNC_ORDER = None

_DESCRIPTION = """
    DESCRIPTION: Model with wages uniquely determined by unemployment, but with
        technologies with varying capital-labor ratio, fixed at creation time
    TYPICAL BEHAVIOUR: Decaying oscillations around a Solow point (?)
    LINKTOARTICLE: Akerlof, G. A. and Stiglitz, J. E., 1969. 'Capital, Wages
        and Structural Unemployment', The Economic Journal, Vol. 79, No. 314
        http://www.jstor.org/stable/2230168
    """

_PRESETS = {}
# ---------------------------
# user-defined model
# contains parameters and functions of various types


def del_t_labor_density(I=0, I_distribution=np.ones(n_kl), delta=0,
                        kl_ratios=np.arange(1, n_kl + 1), itself=np.zeros(n_kl)):
    return I * I_distribution / kl_ratios - delta * itself


def minimum_profitable_kl_ratio_index(productivity_fn=np.arange(n_kl), w=0):
    return np.nonzero(productivity_fn >= w)[0][0]


def profit_maximising_kl_ratio(productivity_fn=np.arange(n_kl), w=0,
                               kl_ratios=np.arange(1, n_kl + 1)):
    return kl_ratios[np.argmax((productivity_fn - w) / kl_ratios)]


def lognormal_distribution(kl_optimum=1, kl_sigma=1,
                           kl_ratios=np.arange(1, n_kl + 1)):
    gaussian = (np.exp(-0.5 * np.log(kl_ratios / kl_optimum)**2 / kl_sigma**2)
                / kl_ratios)
    weighted_sum = (gaussian[:-1] * np.diff(kl_ratios)).sum()
    return np.pad(gaussian[:-1], (0, 1)) / weighted_sum


def total_production(id_kl_min=0, productivity_fn=np.arange(n_kl),
                     labor_density=np.ones(n_kl),
                     kl_ratios=np.arange(1, n_kl + 1)):
    if np.isscalar(id_kl_min):
        return (productivity_fn[id_kl_min:-1] * labor_density[id_kl_min:-1]
                * np.diff(kl_ratios[id_kl_min:])).sum()
    ltp = [(productivity_fn[i:-1] * ld[i:-1] * np.diff(kl_ratios[i:])).sum()
           for i, ld in zip(id_kl_min.astype(int), labor_density)]
    return np.array(ltp)


def total_labor(id_kl_min=0, labor_density=np.ones(n_kl),
                kl_ratios=np.arange(1, n_kl + 1)):
    if np.isscalar(id_kl_min):
        return (labor_density[id_kl_min:-1] * np.diff(kl_ratios)).sum()
    ltl = [(ld[i:-1] * np.diff(kl_ratios[i:])).sum()
           for i, ld in zip(id_kl_min.astype(int), labor_density)]
    return np.array(ltl)


_DPARAM = {
    # ---------
    # exogenous parameters
    # can also have a time variation (just replace by a function of time)
    # useful for studying the model's reaction to an exogenous shock
    'delta': 0.05,
    'beta': 0.,
    'tau': 0.5,
    's_p': 1,
    's_w': 0,
    'kl_sigma': 0.1,
    'kl_ratios': kl_ratios,

    # ---------
    # endogeneous functions

    # differential equations (ode)
    'N': {
        'func': lambda beta=0, itself=0: beta * itself,
        'initial': 6e6,
        'eqtype': 'ode',
    },
    'w': {
        'func': lambda L=0, N=1, itself=0, tau=1: (1e4 * L / (N - L) - itself) / tau,
        'initial': 5e4,
        'eqtype': 'ode',
    },
    # differential equations (pde)
    'labor_density': {
        'func': del_t_labor_density,
        'initial': 5 / (10**0.05 - 1) * np.where(np.abs(kl_ratios / 1e6 - 1) < 0.025, 1, 0),
        'eqtype': 'pde',
    },

    # Intermediary functions (endogenous, computation intermediates)
    'productivity_fn': {
        'func': lambda kl_ratios=np.arange(n_kl): 100 * kl_ratios**0.5,
        'eqtype': 'intermediary',
    },
    'id_kl_min': {
        'func': minimum_profitable_kl_ratio_index,
        'eqtype': 'intermediary',
    },
    'kl_optimum': {
        'func': profit_maximising_kl_ratio,
        'eqtype': 'intermediary',
    },
    'I_distribution': {
        'func': lognormal_distribution,
        'eqtype': 'intermediary',
    },
    'GDP': {
        'func': total_production,
        'eqtype': 'intermediary',
    },
    'L': {
        'func': total_labor,
        'eqtype': 'intermediary',
    },
    'Pi': {
        'func': lambda GDP=0, w=0, L=0: GDP - w * L,
        'eqtype': 'intermediary',
    },
    'I': {
        'func': lambda s_p=1, s_w=0, Pi=0, w=0, L=0: s_p * Pi + s_w * w * L,
        'eqtype': 'intermediary',
    },

    # auxiliary, not used for computation but for interpretation
    # => typically computed at the end after the computation
    'lambda': {
        'func': lambda L=0, N=1: L / N,
        'eqtype': 'auxiliary',
    },
    'omega': {
        'func': lambda w=0, L=0, GDP=1: w * L / GDP,
        'eqtype': 'auxiliary',
    }
}
