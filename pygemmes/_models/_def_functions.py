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
    class phillips:
        """
        The Phillips function is linking the relative wage share increase rate to the
        employement.
        The phenomena behind is a class struggle
        """

        expo = lambda lamb=0,phiexp0=0,phiexp1=0,phiexp2=0: phiexp0 + phiexp1 * np.exp(phiexp2 * lamb)
        div = lambda lamb=0,phi0=0,phi1=0:-phi0 + phi1 / (1 - lamb)**2

        def lin(lamb=0,philinConst=0,philinSlope=0):
            '''
            From article :
            '''
            return philinConst + philinSlope * lamb,


    class kappa:
        """
        The kappa function is linking the relative profit to the share of GDP a firm
        will invest in new productive capital

        It is taking into account both the willingness of bankers to gives loans, and
        the will of the firm to ask for such loan
        """

        def lin(pi=0,
                kappalinConst=0,
                kappalinSlope=0):
            '''
            From article :
            '''
            return kappalinConst + kappalinConst * pi

        def exp(pi=0,
                k0=0,
                k1=0,
                k2=0):
            '''
            From article :
            '''
            return k0 + k1 * np.exp(k2 * pi)

        Ifromkappa = lambda GDP=0,kappa=0 : GDP*kappa

    class production:
        """
        Production functions are the output to input factors.

        """
        leontiev = lambda b=0.5,a=0,L=0,K=0,nu=1: 2*np.minimun((b*K/nu,(1-b)*a*L))
        ces = lambda A=1, b=0.5, K=1, L=1, a=1, eta=1: A*(b*K**(-eta) + (1 - b)*(L * a)**(-eta))**(-1./eta)

        class Leontiev_Optimised:
            '''
            Case in which the amount of workers is the optimal one for profit optimisation
            '''
            Y = lambda K=0,nu=1: K/nu
            L = lambda b=0.5,a=1,K=0,nu=1: K*b/((1-b)*(a*nu))

        class CES_Optimised:
            '''
            Case in which the amount of workers is the optimal one for profit optimisation
            '''
            Y = lambda K=0,nu=1 : K/nu
            L = lambda K=0 : 0
            nu = lambda omega=0.1, b=1, A=1, eta=1: ((1 - omega) / b)**(-1./eta) / A


    class productivity:
        """
        Productivity is the "human power" in production function, the ponderation of each unit
        """
        exogenous = lambda itself=0, alpha=0 : itself*alpha
        verdoorn = lambda itself=0, g=0, alpha=0, beta=0: itself * alpha + g * beta

    class shareholding:
        """
        Shareholding is the share of GDP going from the firm to the shareowner
        """
        def sharehold_lin(divlinSlope=0, divlinconst=0, pi=0):
            """
            From article :
            """
            return (divlinSlope*pi+divlinconst)

    class damage:
        """
        Damages functions
        """
        Damage = lambda T=0, pi1=0, pi2=0, pi3=0, zeta3=1: 1 - 1/(1+pi1*T+pi2*T**2+pi3*T**zeta3),


    class population:
        """
        Population evolution
        """
        expo = lambda itself=0, n=1: itself * n
        logistique = lambda itself=0, n=1, Nmax=1: itself * n * (1-itself/Nmax)

    class inflation:
        '''
        Price dynamics
        '''
        pricefrominflation = lambda itself=0, inflation=0 : itself*inflation
        markup = lambda mu=0, eta=0, omega=0: eta*(mu*omega-1)


    class definitions:
        '''
        Classic intermediary variables that might be needed
        '''
        lamb = lambda L=0, N=1: L / N
        omega = lambda w=0, L=0, Y=1, p=1: (w * L) / (Y*p)
        d = lambda D=0, GDP=1: D / GDP
        pi = lambda Pi=0, GDP=1: Pi/GDP
        GDP_monosec = lambda Y=0, p=0: Y * p
        elasticity = lambda eta=0 : 1/(1+eta)
