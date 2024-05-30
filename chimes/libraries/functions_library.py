
"""
Contains all the functions that can be share between models.
To use them write first :

from chimes.libraries import Funcs

then call a function using for example :
    Funcs.productivity.exogenous

If you want the equation to be readable in network view/ get_summary, use lambda function
In all other cases, use definition functions

This way, changing a brick can be compared easily !
When two brick do not target the same field but goes together (for example Y and L in a produciton function)
Then they are in a subclass.

lamb is still used as a substitute to lambda
do not use _ in any name
"""

import numpy as np


class Funcs:
    class Phillips:
        """
The Phillips function is linking the relative wage share increase rate to the
employment.
The phenomena behind is a class struggle
        """
        # DEFINTIIONS OF phillips
        exp = {
            'func': lambda employment, phiexp0, phiexp1, phiexp2: phiexp0 + phiexp1 * np.exp(phiexp2 * employment),
            'com': 'Exponential param curve'
        }

        div = {
            'func': lambda employment, phi0, phi1: -phi0 + phi1 / (1 - employment)**2,
            'com': 'diverging (force employment \leq 1)'
        }

        lin = {
            'func': lambda employment, philinConst, philinSlope: philinConst + philinSlope * employment,
            'com': 'linear param curve'
        }

        pidiv = {
            'func': lambda zpi, pi, phi0, phi1, employment: -phi0 + (pi / 0.15)**zpi * phi1 / (1 - employment)**2,
            'com': 'Diverging Phillips with nonlinear profit impact. Closes lambda-omega phasespace'
        }

        # DEFINITION OF w (Wage)
        salaryfromPhillips = {
            'func': lambda phillips, w, gammai, inflation: w * (phillips + gammai * inflation),
            'com': 'salary through negociation'
        }

        salaryfromPhillipsNoInflation = {
            'func': lambda phillips, w: w * phillips,
            'com': 'Phillips impact (no negociation)'
        }

        salaryfromPhillipsProfitsNoInflation = {
            'func': lambda phillips, w, pi, zpi: w * phillips * pi**zpi,
            'com': 'Phillips impact (no negociation)'
        }

        # Relaxation on lambda
        lambdarelax = {
            'func': lambda lamb0, employment, taulamb: (lamb0 - employment) / taulamb,
            'com': 'Percieved salary in negociation'
        }

    class Kappa:
        """
The kappa function is linking the relative profit to the share of GDP a firm
will invest in new productive capital

It is taking into account both the willingness of bankers to gives loans, and
the will of the firm to ask for such loan
        """

        # DEFINITION OF kappa
        lin = {
            'func': lambda pi, kappalinConst, kappalinSlope, kappalinMin, kappalinMax: np.clip(kappalinConst + kappalinSlope * pi, kappalinMin, kappalinMax),
            'com': 'linear param curve'
        }
        exp = {
            'func': lambda pi, k0, k1, k2: k0 + k1 * np.exp(k2 * pi),
            'com': 'exponential param curve'
        }

        # DEFINITIONS OF IR AND I #
        ifromkappa = {
            'func': lambda GDP, kappa: GDP * kappa,
            'com': 'I deduced from kappa func'
        }
        ifromnobank = {
            'func': lambda Pi: Pi,
            'com': 'Benefits into investment'
        }
        irfromI = {
            'func': lambda I, p: I / p,
            'com': 'Real units from money invest and price'
        }
        # DEFINITIONS OF K #
        kfromI = {
            'func': lambda I, K, delta, p: I / p - K * delta,
            'com': 'Capital evolution from investment and depreciation',
        }
        kfromIr = {
            'func': lambda Ir, K, delta: Ir - K * delta,
            'com': 'Capital evolution from investment and depreciation',
        }

        # USING B (Kapital Buffer) #
        bfromIr = {
            'func': lambda Ir, B, tauK: Ir - B / tauK,
            'com': 'Investment - activation with characteristic time',
        }
        kfromB = {
            'func': lambda B, K, delta, tauK: B / tauK - K * delta,
            'com': 'Capital evolution from investment and depreciation',
        }

    class ProductionWorkers:
        """
Production functions are the output to input factors.
        """
        leontievnu = {
            'func': lambda nu, K, L, a: np.minimum((K / nu, a * L)),
            'com': 'Leontiev production function based on nu formalism'
        }

        leontiev = {
            'func': lambda nu, b, K, L, a, A: np.minimum((2 * b * A * K, 2 * (1 - b) * a * L)),
            'com': 'Leontiev production function with A and b'
        }

        # CES FUNCTIONS
        cesY = {
            'func': lambda A, b, K, CESexp, L, a: (b * (A * K)**(-CESexp) + (1 - b) * (a * L)**(-CESexp))**(-1 / CESexp),
            'com': 'CES production function'
        }
        cesY2 = {
            'func': lambda cesYcarac, cesLcarac, CESexp, L: cesYcarac * ((1 + (L / cesLcarac)**(-CESexp)) / 2)**(-1 / CESexp),
            'com': 'CES production function using caracteristics'
        }
        cesYcarac = {
            'func': lambda K, A, b, CESexp: K * A * (2 * b)**(-1 / CESexp),
            'com': 'Typical Y in CES'
        }
        cesLcarac = {
            'func': lambda A, K, a, b, CESexp: A * (K / a) * (2 * (1 - b))**(1 / CESexp),
            'com': 'Typical Labour in CES'
        }
        omegacarac = {
            'func': lambda w, cesLcarac, p, cesYcarac: w * cesLcarac / (p * cesYcarac),
            'com': 'Typical omega from K,p,w'
        }

        Leontiev_OptimisedYfnu = {
            'func': lambda K, nu: K / nu,
            'com': 'Assume full required employment, nu formalism'
        }
        Leontiev_OptimisedLfa = {
            'func': lambda Y, a: Y / a,
            'com': 'Assume full instant employment, nu formalism'
        }
        Leontiev_OptimisedY = {
            'func': lambda K, nu, b: 2 * b * K / nu,
            'com': 'Assume full employment'
        }
        Leontiev_OptimisedL = {
            'func': lambda b, a, K, nu: K * b / ((1 - b) * (a * nu)),
            'com': 'L for full capital use'
        }

        CES_Optimisedl = {
            'func': lambda omegacarac, CESexp: (omegacarac**(-CESexp / (1 + CESexp)) - 1)**(1 / CESexp),
            'com': 'impact of elasticity on real employment'}

        CES_OptimisedY = {
            'func': lambda K, omegacarac, l, b, CESexp, A: K * ((1 - omegacarac * l) / b)**(1. / CESexp) * A,
            'com': 'Y CES with optimisation of profit'
        }
        CES_OptimisedL = {
            'func': lambda l, cesLcarac: cesLcarac * l,
            'com': 'L CES, deduced from l'
        }
        CES_Optimisednu = {
            'func': lambda omega, b, A, CESexp: ((1 - omega) / b)**(-1. / CESexp) / A,
            'com': 'nu deduced from CES optimisation of profit'
        }

    class Productivity:
        """
Productivity is the "human power" in production function, the ponderation of each unit
        """
        exogenous = {
            'func': lambda a, alpha: a * alpha,
            'com': 'ODE exogenous, exponential',
        }

        verdoorn = {
            'func': lambda a, g, alpha, beta: a * (alpha + g * beta),
            'com': 'ODE endogenous, impact of physical growth'
        }

    class Shareholding:
        """
Shareholding is the share of GDP going from the firm to the shareowner
        """
        lin = {
            'func': lambda divlinSlope, divlinconst, pi, GDP, divlinMin, divlinMax: GDP * np.clip((divlinSlope * pi + divlinconst), divlinMin, divlinMax),
            'com': 'lin fit from Coping',
        }

    class Speculation:
        """
Speculation is the flux of money going from or to the financial market
        """
        exp = {
            'func': lambda g, SpecExpo1, SpecExpo2, SpecExpo3, SpecExpo4: - SpecExpo1 + SpecExpo2 * np.exp(SpecExpo3 + g * SpecExpo4),
            'com': 'speculation exponential function'
        }

    class Damage:
        """
Linking Temperature to economic impact
        """
        general = {
            'func': lambda T, pi1, pi2, pi3, zeta3: 1 - 1 / (1 + pi1 * T + pi2 * T**2 + pi3 * T**zeta3),
            'com': 'General damage function'
        }

    class Population:
        """
Population evolution
        """
        exp = {
            'func': lambda N, n: N * n,
            'com': 'ODE exogenous exponential',
        }
        logistic = {
            'func': lambda N, n, Nmax: N * n * (1 - N / Nmax),
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
            'func': lambda p, inflation: p * inflation,
            'com': 'ODE Prices variation deduced from inflation',
        }

        # Inflation mechanism
        markup = {
            'func': lambda mu, eta, c, p: eta * (mu * c / p - 1),
            'com': 'markup on production costs',
        }
        markupInventory = {
            'func': lambda mu, eta, c, p, chi, dotV, V: eta * (mu * c / p - 1) + chi * dotV / V,
            'com': 'markup+ relative inventory ',
        }
        markupInventY = {
            'func': lambda mu, eta, c, p, chiY, dotV, Y: eta * (mu * c / p - 1) + chiY * dotV / Y,
            'com': 'markup+ inventory variat/Flux ',
        }
        costonlylabor = {
            'func': lambda w, a: w / a,
            'com': 'price with only labor salary',
        }

    class Definitions:
        '''
Classic intermediary variables that might be needed
        '''
        employment = {
            'func': lambda L, N: L / N,
            'com': 'its definition',
        }
        omega = {
            'func': lambda w, L, Y, p: (w * L) / (Y * p),
            'com': 'its definition',
        }
        d = {
            'func': lambda D, GDP: D / GDP,
            'com': 'its definition',
        }
        pi = {
            'func': lambda Pi, GDP: Pi / GDP,
            'com': 'its definition',
        }
        GDPmonosec = {
            'func': lambda Y, p: Y * p,
            'com': 'its definition',
        }
        nu = {
            'func': lambda Y, K: K / Y,
            'com': 'its definition',
        }
        elasticity = {
            'func': lambda eta: 1 / (1 + eta),
            'com': 'its definition',
        }
        s = {
            'func': lambda Speculation, GDP: Speculation / GDP,
            'com': 'its definition',
        }
        m = {
            'func': lambda M, GDP: M / GDP,
            'com': 'its definition',
        }
        v = {
            'func': lambda GDP, M: GDP / M,
            'com': 'its definition (also 1/m)'
        }
        t = {
            'func': lambda t: 1,
            'com': 'time',
            'initial': 0,
        }

    class Atmosphere:
        '''
        Modelisation of an atmosphere, with CO2 and Temperature
        '''

        F = {
            'func': lambda F2CO2, CO2AT, CAT: F2CO2 / np.log(2) * np.log(CO2AT / CAT),
            'com': 'Forcing as sensitivity',
        }

        Three_LayersCO2AT = {
            # 1./3.666 is to convert from CO2 to C
            'func': lambda Emission, phi12, CO2UP, CUP, CAT, CO2AT: (1. / 3.666) * Emission - phi12 * CO2AT + phi12 * CAT / CUP * CO2UP,
            'com': '3-Layer dynamics (Atmosphere)',
        }
        Three_LayersCO2UP = {
            'func': lambda phi12, phi23, CAT, CUP, CLO, CO2AT, CO2UP, CO2LO: phi12 * CO2AT - CO2UP * (phi12 * CAT / CUP - phi23) + phi23 * CUP / CLO * CO2LO,
            'com': '3-Layer dynamics (Upper ocean)',
        }
        Three_LayersCO2LO = {
            'func': lambda phi23, CO2UP, CUP, CLO, CO2LO: phi23 * CO2UP - phi23 * CUP / CLO * CO2LO,
            'com': '3-Layer dynamics (lower ocean)',
        }
        Three_LayersT = {
            'func': lambda F, rhoAtmo, T, gammaAtmo, T0, Capacity: (F - rhoAtmo * T - gammaAtmo * (T - T0)) / Capacity,
            'com': 'Forcing and ocean dynamics',
        }
        Three_LayersT0 = {
            'func': lambda gammaAtmo, T, T0, Capacity0: (gammaAtmo * (T - T0)) / Capacity0,
            'com': 'Accumulation from atmosphere',
        }
