from ._set_methods import setM
from ._get_methods import getM
from ._calculate_methods import calculateM
from ._save_method import saveM


import numpy as np


def _comparesubarray(M):
    '''
    Take a big array of N dimensions (n1,n2,n3,n4),
    check if one dimension is juste a stack of a subarray with always same values.
    Return a list, each axis


    :param M:
    :param V:
    :return:
    '''
    M = np.array(M)
    Sameaxis = []
    dimensions = np.shape(M)
    for ii, d in enumerate(dimensions):

        Mrshp = M.reshape(-1, dimensions[ii])
        Dimtocompare = Mrshp.shape[0]

        Sameaxis.append(np.prod([np.array_equal(Mrshp[0, :],
                                                Mrshp[jj, :])
                                for jj in range(Dimtocompare)]) > 0)
    return Sameaxis
