"""Goodwin model with minimal formalism"""


_LOGICS = dict(
    differential=dict(
        p=lambda p, inflation: p*inflation,
        a=lambda a, alpha: a*alpha,
        N=lambda N, n: N*n,
        K=lambda K, Ir, delta: Ir-delta*K,
        w=lambda w, phillips: w*phillips),
    statevar=dict(
        pi=lambda p, Y, Pi: Pi / (p*Y),
        omega=lambda p, Y, w, L: w*L/(p*Y),
        employment=lambda L, N: L/N,
        g=lambda Ir, K, delta: Ir/K-delta,
        Y=lambda K, nu: K/nu,
        Pi=lambda p, Y, w, L: p*Y-w*L,
        C=lambda Y, Ir: Y-Ir,
        Ir=lambda Pi, p: Pi/p,
        L=lambda K, a: K/a,
        phillips=lambda Phi0, Phi1, employment: Phi0+Phi1/(1-employment)**2),
)
