import numpy as np


def _cn(y, n):
    '''
    calculate cn fourier coefficients for one cycle, not normalized
    '''
    return np.array([np.abs(np.mean(y*np.exp(-1j*2*i*np.pi*np.linspace(0, 1, len(y))))) for i in range(10)])
