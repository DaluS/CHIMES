"""Lotka-Volterra as a Goodwin system"""

import numpy as np
_DESCRIPTION = """
## What is this model ?

This model is a minimal dynamical core, similar to a Goodwin phase-space dynamics, but even simpler. 
The equation system is thus: 

$$\dot{x} = x (A-B f(y))$$
$$\dot{y} = y (C-D g(x))$$

Where $f(x)$ and $g(y)$ are increasing functions. 
The advantage is that the equilibrium is easy to calculate

$$y_{eq} = f^{-1}(A/B)$$
$$x_{eq} = g^{-1}(C/D)$$

The system has closed cycles, and the equilibrium is not stable nor unstable. 
To simplify, we use $f(y)=y$, and $g(x)=x$. 

One of the interest of such practice is to replace the parameters with subparameters and linear dependency

$$A \to A_0 + A_x (x-x_{eq}) + A_y (y-y_{eq})$$
$$B \to B_0 + B_x (x-x_{eq}) + B_y (y-y_{eq})$$
$$C \to C_0 + C_x (x-x_{eq}) + C_y (y-y_{eq})$$
$$D \to D_0 + D_x (x-x_{eq}) + D_y (y-y_{eq})$$

Changing the parameters will not change the equilibrium point, but it will change the stability. 
This can be typically captured by the calculation of the Jacobian, its trace and determinant

## Expected behavior
* When $A_x,B_x,C_x,D_x,A_y,B_y,C_y,D_y$ are zero, the system is doing closed cycles.
* Increasing $B_x,D_y$ stabilize the system (and slow down the cycles locally)
* Increasing $A_x,C_y$ destabilize the system (and accelerate the cycles locally)
* Increasing $A_y,C_x$ accelerate the cycles
* Increasing $B_y,D_x$ slow down the cycles

## Oscillating equilibrium 




"""

_TODO = ['Presets and plots']
_ARTICLE = ""
_DATE = "2024/06/11"
_CODER = "Paul Valcke"
_KEYWORDS = ['Stability','Predatory-Prey','Lotka-Volterra','Goodwin',]

_LOGICS = {
    'differential': {  # Differential variables are defined by their time derivative and not their value
        'y': { 
            'initial': .4,
            'func': lambda x, C, D, y: y * (C-D*x),
        },
        'x': {
            'func': lambda x, A, B, y: x * (A-B*y),
            'initial': .7,
        },
        'y0': {
            'initial': .7,
            'func': lambda x0, C0, D0, y0: y0 * (C0-D0*x0), 
        },
        'x0': {
            'func': lambda x0, A0, B0, y0: x0 * (A0-B0*y0),
            'initial': .7,
        },
    },
    'statevar': {  # State variables value are defined by their logic
        'xeqM': lambda C, D: C/D,
        'yeqM': lambda A, B: A/B,
        'xeq': lambda C0, D0: C0/D0,
        'yeq': lambda A0, B0: A0/B0,

        'A': lambda A0, Ax, Ay, x, y, xeq, yeq: A0+Ax*(x-xeq)+Ay*(y-yeq),
        'B': lambda B0, Bx, By, x, y, xeq, yeq: B0+Bx*(x-xeq)+By*(y-yeq),
        'C': lambda C0, Cx, Cy, x, y, xeq, yeq: C0+Cx*(x-xeq)+Cy*(y-yeq),
        'D': lambda D0, Dx, Dy, x, y, xeq, yeq: D0+Dx*(x-xeq)+Dy*(y-yeq),
    },
    'parameter': dict(
        A0=1,
        B0=3,
        C0=1.5,
        D0=4,
        
        Ax=0,
        Bx=0,
        Cx=0,
        Dx=0,
        
        Ay=0,
        By=0,
        Cy=0,
        Dy=0,
    ),
}

_SUPPLEMENTS = {
}

_PRESETS = {
}
