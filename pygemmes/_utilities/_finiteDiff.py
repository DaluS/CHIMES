import scipy.linalg
import scipy.sparse.linalg as spalg
from scipy import special as spe
from scipy import sparse as spa
from scipy.linalg import toeplitz

import numpy as np


dx= 1
L = 4
X= np.arange(0,L,dx)
Y =np.arange(0,L,dx)
N=len(X)
NN=N**2

XX,YY = np.meshgrid(X, Y)

# 2D COORDINATES in 1D
X2 = XX.reshape(-1)
Y2 = YY.reshape(-1)

ZZ=np.exp(- 10*(np.sqrt((XX-0.5)**2+(YY-0.5)**2)))

# Empty matrix
diffmatX=np.zeros((len(X2),len(Y2)))
diffmatX[np.arange(NN)%NN ,(np.arange(NN)+1) % NN]=1/(2*dx)
diffmatX[(np.arange(NN)+1) % NN,np.arange(NN) % NN]=-1/(2*dx)
diffmatY= np.zeros((len(X2),len(Y2)))
diffmatY[(np.arange(NN))%NN ,(N+np.arange(NN)) % NN]=1/(2*dx)
diffmatY[(N+np.arange(NN)) % NN,(np.arange(NN)) % NN]=-1/(2*dx)

def dif1D(L, N, order=[1], x0=0, pts=3, type='fd'):
    """
    DIF1D function that generates 1D differentiation matrices.
    :param x0: Offsets the mesh.
    :param L: Length of the mesh.
    :param N: Number of mesh nodes.
    :param order: Derivative order desired. (List of integers)
    :param pts: Number of stencils for finite difference.
    :param type: 'fd'   for finite difference
                 'fp'   for finite difference in periodic domain
                 'cheb' for spectral chebyshev
                 'fou'  for periodic spectral fourier
    :return: [D, x, w]
            D[ith-1]: List containing the i'th order diff matrix.
            x: The discrete mesh points.
            w: The integration matrix
    """

    if type is 'fd':  # finite difference (D output is sparse)
        scale = L/2
        D = len(order)*[None]
        i = 0
        for o in order:
            [x, D[i]] = np.fddif(N, o, pts)
            D[i] /= (scale ** o)  # Scales the diff matrix
            i += 1
        x *= scale  # Scales the mesh
        x += x0 - x[0]  # Offsets the mesh
        w = (np.hstack((np.diff(x), 0))+np.hstack((0, np.diff(x))))/2.  # Integral

    elif type is 'fp':  # periodic finite differences (D output is dense)
        scale = L/2
        D = len(order)*[None]
        i = 0
        for o in order:
            [x, D[i]] = fdper(N, o, pts)
            D[i] /= (scale ** o)  # Scales the diff matrix
            i += 1
        x *= scale  # Scales the mesh
        x += x0 - x[0]  # Offsets the mesh
        w = np.ones(N)*(x[1]-x[0])  # Integral

    elif type is 'cheb':  # Chebyshev differentiation matrix
        scale = -L/2      # D output is dense
        [x, DM] = chebdif(N, max(order))
        D = len(order)*[None]
        i = 0
        for o in order:
            D[i] = DM[:, :, o-1]
            D[i] /= (scale ** o)
            i += 1
        x *= scale  # scales the mesh
        x += x0 - x[0]  # offsets the mesh
        w = L*clencurt(N)/2

    elif type is 'fou':  # Fourier periodic differentiation matrix
        scale = L/(2*np.pi) # D output is dense
        D = len(order)*[None]
        i = 0
        for o in order:
            [x, D[i]] = np.fourdif(N, o)
            D[i] /= (scale ** o)  # Scales the diff matrix
            i += 1
        x *= scale  # Scales the mesh
        x += x0 - x[0]  # Offsets the mesh
        w = np.ones(N)*(x[1]-x[0])  # Integral

    return [D, x, w]




Lx = 0.5
Ly = 0.1
Nx = 15
Ny = 15
pts = 9

Rx = dif.dif1D(L=Lx, N=Nx, type='fd', pts=pts, order=[1, 2])
Ry = dif.dif1D(L=Ly, N=Ny, type='fd', pts=pts, order=[1, 2])

def spd(vect):   # Simplified Sparse Diagonal creation
    return spa.spdiags(vect, 0, len(vect), len(vect), format='lil')

import numpy as np


def ufdwt(h, pts, order):
    """
    UFDWT is the "Uniform Finite Difference WeighTing". It calculates
    the weights, or coefficients, of the 1D differentiation matrix
    using a Finite-Difference scheme.
    :param h: Relative spacing between two mesh nodes.
    :param pts:  Number of stencils for calculating the derivatives.
    :param order: Order of the derivative desired (order<pts-1)
    :return: W: is the weight matrix. Each row contains a different set
    of weights (centered or off). If, for example, the number of finite
    difference points is odd, the centered difference weights will
    appear in the middle row.

    Implemented to Python by L. Bernardos, June 2015.
    """

    N = 2 * pts - 1

    A = np.tile(np.arange(pts)[:, np.newaxis], (1, N))
    B = np.tile(np.arange(-pts + 1, pts) * h, (pts, 1))
    M = (B ** A) / spe.gamma(A + 1)

    rhs = np.zeros((pts, 1))
    rhs[order] = 1

    W = np.zeros((pts, pts))
    for k in range(0, pts):
        W[:, k] = np.linalg.solve(M[:, np.arange(pts) + k], rhs)[:, 0]

    W = W.T
    W = W[::-1, :]
    return W

def fdper(N, order, pts):
    """
    FDPER function of Finite Difference PERiodical. It creates
    the differentiation matrix for N mesh points for periodic
    domains.
    :param N: Number of mesh nodes.
    :param order: Order of the derivative desired.
    :param pts: Number of stencils to use for finite difference
    :return: [x,D] x: domain from -1 to 1. D: Diff matrix.

    Implemented to Python by L. Bernardos, June 2015.
    """
    x = np.linspace(-1, 1, N+1)
    x = np.delete(x, -1)
    h = x[1] - x[0]

    # subroutine for finite difference weights
    W = ufdwt(h, pts, order)
    t = int((pts + 1) / 2)

    R = np.zeros(N)
    C = np.zeros(N)
    R[np.hstack((np.arange(-t+1, 0), np.arange(t)))] = W[t-1]
    C[np.hstack((np.arange(t-1, -1, -1), np.arange(-1, -t, -1)))] = W[t-1]
    D = np.toeplitz(C, R)
    return [x, D]