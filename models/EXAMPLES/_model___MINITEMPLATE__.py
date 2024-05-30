"""MINIMAL FILE, solving exp(0.01*t)"""

_LOGICS = dict(
    differential=dict(
        K=lambda K: 0.01 * K,
    ),
)
