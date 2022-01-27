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
do not use _ in any name
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
            'com': 'Exponential param curve'
        }

        div = {
            'func': lambda lamb=0, phi0=0, phi1=0: -phi0 + phi1 / (1 - lamb)**2,
            'com': 'diverging (force omega \leq 1)'
        }

        lin = {
            'func': lambda lamb=0, philinConst=0, philinSlope=0: philinConst + philinSlope * lamb,
            'com': 'linear param curve'
        }
        salaryfromPhillips = {
            'func': lambda phillips=0, itself=0, gammai=0, inflation=0: itself * (phillips + gammai*inflation),
            'com': 'salary through negociation',
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
            'com': 'linear param curve'
        }
        exp = {
            'func': lambda pi=0, k0=0, k1=0, k2=0: k0 + k1 * np.exp(k2 * pi),
            'com': 'exponential param curve'
        }
        ifromkappa = {
            'func': lambda GDP=0, kappa=0: GDP*kappa,
            'com': 'I deduced from kappa func'
        }
        kfromI = {
            'func': lambda I=0, itself=0, delta=0, p=1: I/p - itself * delta,
            'com': 'Capital evolution from investment and depreciation', },

    class ProductionWorkers:
        """
Production functions are the output to input factors.
        """
        leontiev = {
            'func': lambda nu=1, b=0.5, K=1, L=1, a=1, A=0: np.minimum((b*K/nu, (1-b)*A*a*L)),
            'com': 'Leontiev production function'
        }

        # CES FUNCTIONS
        cesY = {
            'func': lambda A=1, b=0.5, K=1, CESexp=100, L=1, a=1: (b*(A*K)**(-CESexp) + (1-b)*(a*L)**(-CESexp))**(-1/CESexp),
            'com': 'CES production function'
        }
        cesY2 = {
            'func': lambda cesYcarac=0, cesLcarac=1, CESexp=100, L=1: cesYcarac * ((1 + (L/cesLcarac)**(-CESexp))/2)**(-1/CESexp),
            'com': 'CES production function using caracteristics'
        }
        cesYcarac = {
            'func': lambda K=0, A=0, b=0.5, CESexp=100: K*A*(2*b)**(-1/CESexp),
            'com': 'Typical Y in CES'
        }
        cesLcarac = {
            'func': lambda A=0, K=0, a=1, b=0.5, CESexp=100:   A*(K/a) * (2*(1-b))**(1/CESexp),
            'com': 'Typical Labour in CES'
        }
        omegacarac = {
            'func': lambda w=0, cesLcarac=0, p=1, cesYcarac=1: w*cesLcarac/(p*cesYcarac),
            'com': 'Typical omega from K,p,w'
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
            r'''
The idea is to use both CES production function and profit optimisation :
$$ Y = \left[ b (AK)^{-\eta} + (1-b) (aL)^{-\eta} \right]^{-1/\eta} $$
$$\dfrac{d \Pi}{d L}= 0$$
$$\dfrac{\partial Y}{\partial L}=w/p$$

It goes like this :

$$ Y = A (2b)^{-1/\eta} K \left[ \dfrac{1 + \dfrac{1-b}{b} \left(\dfrac{aL}{AK}\right)^{-\eta}}{2}\right]^{-1/\eta} $$
$$ Y = Y_c \left[ \dfrac{1 +\left(\dfrac{L}{L_c}\right)^{-\eta}}{2}\right]^{-1/\eta} $$
$$ Y_c =  A (2b)^{-1/\eta} K $$
$$ L_c = \left( \dfrac{b}{1-b} \right)^{-1/\eta}\dfrac{AK}{a} $$
$$ L_c = \left[ 2(1-b) \right]^{1/\eta} \dfrac{Y_c}{a}$$
$$\omega_c=\dfrac{wL_c}{pY_c}=\dfrac{w}{a p}\left[ 2(1-b) \right]^{1/\eta} $$
$$\omega= \dfrac{L}{L_c}\dfrac{w  L_c}{pY_c}=l \omega_c $$

$$f(l)= \left[ \dfrac{1 +l^{-\eta}}{2}\right]^{-1/\eta} $$
$$\dfrac{\partial Y}{\partial L}= \dfrac{Y_c}{L_c} \dfrac{\partial f(l)}{\partial l}$$
$$\dfrac{\partial Y}{\partial L}= \dfrac{Y_c}{L_c} l^{-\eta-1}\left[ 1 + l^{-\eta}\right]^{-\frac{\eta+1}{\eta}}$$
$$\dfrac{\partial Y}{\partial L}= \dfrac{Y_c}{L_c} \left[ 1 + l^{\eta}\right]^{-\frac{\eta+1}{\eta}}$$

$$\left[ 1 + l^{\eta}\right]^{-\frac{\eta+1}{\eta}}=\dfrac{wL_c}{pY_c}=\omega_c$$

l is thus the adjustment variable compared to a Leontiev : if $l=1$ then the system behave the same way.

$$l = \left( \omega_c^{-\frac{\eta}{(1+\eta)}} -1 \right)^{\frac{1}{\eta}}$$
            '''
            l = {
                'func': lambda omegacarac=0.5, CESexp=100: (omegacarac**(-CESexp/(1+CESexp)) - 1)**(1/CESexp),
                'com': 'impact of elasticity on real employement'}

            Y = {
                'func': lambda K=0, omega=.1, b=.5, CESexp=.5, A=1: K*((1 - omega) / b)**(1./CESexp) * A,
                'com': 'Y CES with optimisation of profit'
            }
            L = {
                'func': lambda l=0, cesLcarac=0: cesLcarac*l,
                'com': 'L CES, deduced from l'
            }
            nu = {
                'func': lambda omega=0.1, b=1, A=1, CESexp=1: ((1 - omega) / b)**(-1./CESexp) / A,
                'com': 'nu deduced from CES optimisation of profit'
            }

    class Productivity:
        """
Productivity is the "human power" in production function, the ponderation of each unit
        """
        exogenous = {
            'func': lambda itself=0, alpha=0: itself*alpha,
            'com': 'ODE exogenous, exponential',
        }

        verdoorn = {
            'func': lambda itself=0, g=0, alpha=0, beta=0: itself * alpha + g * beta,
            'com': 'ODE endogenous, impact of physical growth'
        }

    class Shareholding:
        """
Shareholding is the share of GDP going from the firm to the shareowner
        """
        shareholdlin = {
            'func': lambda divlinSlope=0, divlinconst=0, pi=0: divlinSlope*pi+divlinconst,
            'com': 'lin fit from Coping',
        }

    class Speculation:
        """
Speculation is the flux of money going from or to the financial market
        """
        exp = {
            'func': lambda g=0, SpecExpo1=0, SpecExpo2=0, SpecExpo3=0, SpecExpo4=0: - SpecExpo1+SpecExpo2*np.exp(SpecExpo3+g * SpecExpo4),
            'com': 'speculation exponential function'
        }

    class Damage:
        """
Linking Temperature to economic impact
        """
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
            'com': 'ODE exogenous exponential',
        }
        logistic = {
            'func': lambda itself=0, n=1, Nmax=1: itself * n * (1-itself/Nmax),
            'com': 'ODE exogenous logistic (saturation)',
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
            'com': 'ODE Prices variation deduced from inflation',
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
        GDPmonosec = {
            'func': lambda Y=0, p=0: Y * p,
            'com': 'definition',
        }
        nu = {
            'func': lambda Y=1, K=1: K/Y,
            'com': 'definition',
        }
        elasticity = {
            'func': lambda eta=0: 1/(1+eta),
            'com': 'definition',
        }
        s = {
            'func': lambda Speculation=0, GDP=1: Speculation/GDP,
            'com': 'definition',
        }
