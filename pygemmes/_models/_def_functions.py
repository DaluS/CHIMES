# -*- coding: utf-8 -*-
"""
Contains all the functions that can be share between models.
To use them write first :

from pygemmes._models import Funcs

then call a function using for example :
    Funcs.productivity.exogenous

If you want the equation to be readable in network view/ get_summary, use lambda function
In all other cases, use definition functions

This way, changing a brick can be compared easily !
When two brick do not target the same field but goes together (for example Y and L in a produciton function)
Then they are in a subclass.

itself is still used in a case of an ode calling itself,
lamb is still used as a substitute to lambda
"""

import numpy as np


class Funcs:
    class Phillips:
        """
        The Phillips function is linking the relative wage share increase rate to the
        employement.
        The phenomena behind is a class struggle
        """

        exp = {
            'func': lambda lamb=0, phiexp0=0, phiexp1=0, phiexp2=0: phiexp0 + phiexp1 * np.exp(phiexp2 * lamb),
            'com': 'Exponential fit'
        }

        div = {
            'func': lambda lamb=0, phi0=0, phi1=0: -phi0 + phi1 / (1 - lamb)**2,
            'com': 'diverging fit (force omega \leq 1)'
        }

        lin = {
            'func': lambda lamb=0, philinConst=0, philinSlope=0: philinConst + philinSlope * lamb,
            'com': 'linear'
        }

    class Kappa:
        """
        The kappa function is linking the relative profit to the share of GDP a firm
        will invest in new productive capital

        It is taking into account both the willingness of bankers to gives loans, and
        the will of the firm to ask for such loan
        """

        lin = {
            'func': lambda pi=0, kappalinConst=0, kappalinSlope=0: kappalinConst + kappalinConst * pi,
            'com': 'lin param curve'
        }
        exp = {
            'func': lambda pi=0, k0=0, k1=0, k2=0: k0 + k1 * np.exp(k2 * pi),
            'com': 'exp param curve'
        }
        ifromkappa = {
            'func': lambda GDP=0, kappa=0: GDP*kappa,
            'com': ''
        }

    class ProductionWorkers:
        """
        Production functions are the output to input factors.
        """
        leontiev = {
            'func': lambda nu=1, b=0.5, K=1, L=1, a=1, eta=1: 2*np.minimum(((b*K/nu), (1-b)*a*L)),
            'com': 'Leontiev production function'
        }

        ces = {
            'func': lambda A=1, b=0.5, K=1, L=1, a=1, eta=1: A *
            (b*K**(-eta) + (1 - b)*(L * a)**(-eta))**(-1./eta),
            'com': 'CES production function'
        }

        class Leontiev_Optimised:
            '''
            Case in which the amount of workers is the optimal one for profit optimisation
            '''
            Y = {
                'func': lambda K=0, nu=1: K/nu,
                'com': 'Assume full employement'
            }
            L = {
                'func': lambda b=0.5, a=1, K=0, nu=1: K*b/((1-b)*(a*nu)),
                'com': 'L for full capital use'
            }

        class CES_Optimised:
            '''
            Case in which the amount of workers is the optimal one for profit optimisation
            '''
            Y = {
                'func': lambda K=0, nu=1: K/nu,
                'com': 'Y CES with optimisation of profit'
            }
            L = {
                'func': lambda K=0: 0,
                'com': 'L CES, with ofptimisation of profit'
            }
            nu = {
                'func': lambda omega=0.1, b=1, A=1, eta=1: ((1 - omega) / b)**(-1./eta) / A,
                'com': 'nu deduced from CES optimisation of profit'
            }

    class Productivity:
        """
        Productivity is the "human power" in production function, the ponderation of each unit
        """
        exogenous = {
            'func': lambda itself=0, alpha=0: itself*alpha,
            'com': 'exogenous, exponential',
        }

        verdoorn = {
            'func': lambda itself=0, g=0, alpha=0, beta=0: itself * alpha + g * beta,
            'com': 'endogenous, impact of physical growth'
        }

    class Shareholding:
        """
        Shareholding is the share of GDP going from the firm to the shareowner
        """
        sharehold_lin = {
            'func': lambda divlinSlope=0, divlinconst=0, pi=0: divlinSlope*pi+divlinconst,
            'com': 'lin fit from Coping',
        }

    class Speculation:
        exp = {
            'func': lambda g=0, SpeExpoConst=0, SpecExpoSlope=0, SpecExpoexpo1=0, SpecExpoexpo2=0: - SpeExpoConst+SpecExpoSlope*np.exp(SpecExpoexpo1+g * SpecExpoexpo2),
            'com': 'speculation exponential function'
        }

    class Damage:
        general = {
            'func': lambda T=0, pi1=0, pi2=0, pi3=0, zeta3=1: 1 - 1/(1+pi1*T+pi2*T**2+pi3*T**zeta3),
            'com': 'General damage function'
        }

    class Population:
        """
        Population evolution
        """
        exp = {
            'func': lambda itself=0, n=0: itself * n,
            'com': 'exogenous exponential',
        }
        logistic = {
            'func': lambda itself=0, n=1, Nmax=1: itself * n * (1-itself/Nmax),
            'com': 'exogenous logistic (saturation)',
        }

    class Inflation:
        '''
        Price signal is important in the behavior of such system.
        However, prices are often not defined as a statevariable, but rather as
        the consequence of inflations processes : it is a social construct.
        '''
        # Price dynamics deduced from inflation
        pricefrominflation = {
            'func': lambda itself=0, inflation=0: itself*inflation,
            'com': 'Prices variation deduced from inflation',
        }

        # Inflation mechanism
        markup = {
            'func': lambda mu=0, eta=0, c=0, p=1: eta*(mu*c/p-1),
            'com': 'markup on production costs',
        }

    class Definitions:
        '''
        Classic intermediary variables that might be needed
        '''
        lamb = {
            'func': lambda L=0, N=1: L / N,
            'com': 'definition',
        }
        omega = {
            'func': lambda w=0, L=0, Y=1, p=1: (w * L) / (Y*p),
            'com': 'definition',
        }
        d = {
            'func': lambda D=0, GDP=1: D / GDP,
            'com': 'definition',
        }
        pi = {
            'func': lambda Pi=0, GDP=1: Pi/GDP,
            'com': 'definition',
        }
        GDP_monosec = {
            'func': lambda Y=0, p=0: Y * p,
            'com': 'definition',
        }
        elasticity = {
            'func': lambda eta=0: 1/(1+eta),
            'com': 'definition',
        }
