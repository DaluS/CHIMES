# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 11:02:26 2022

@author: Paul Valcke
"""

import numpy as np


class Funcs:
    class Phillips:
        """
        The Phillips function is linking the relative wage share increase rate to the
        employement.
        The phenomena behind is a class struggle
        """

        def expo(lamb=0,
                 phiexp0=0,
                 phiexp1=0,
                 phiexp2=0,
                 ):
            '''
            From article :
            '''
            return phiexp0 + phiexp1 * np.exp(phiexp2 * lamb)

        def div(lamb=0,
                phi0=0,
                phi1=0,
                phi2=0,
                ):
            '''
            From article :
            '''
            return -phi0 + phi1 / (1 - lamb)**2

        def lin(lamb=0,
                philinConst=0,
                philinSlope=0,
                ):
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
                k2=0,):
            '''
            From article :
            '''
            return k0 + k1 * np.exp(k2 * pi)


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
            Y = 0
            L = 0
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
        markup = lambda mu=0, eta=0, omega=0: eta*(mu*omega-1),
