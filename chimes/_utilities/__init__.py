import numpy as np


def _cn(y, n):
    '''
    calculate cn fourier coefficients for one cycle, not normalized
    '''
    return np.array([np.abs(np.mean(y*np.exp(-1j*2*i*np.pi*np.linspace(0, 1, len(y))))) for i in range(10)])

def _comparesubarray(M):
    '''
    Take a big array of N dimensions (n1,n2,n3,n4),
    check if one dimension is juste a stack of a subarray with always same values.
    Return a list, each axis


    :param M:
    :param V:
    :return:
    '''
    M=np.array(M)
    Sameaxis=[]
    dimensions=np.shape(M)
    for ii,d in enumerate(dimensions):

        Mrshp=M.reshape(-1,dimensions[ii])
        Dimtocompare = Mrshp.shape[0]

        Sameaxis.append(np.prod([np.array_equal(Mrshp[0,:],
                                               Mrshp[jj,:])
                                for jj in range(Dimtocompare)])>0)
    return Sameaxis

def in_notebook():
    try:
        from IPython import get_ipython
        if 'IPKernelApp' not in get_ipython().config: return False
    except ImportError:    return False
    except AttributeError: return False
    return True


def pprint(ldf):
    if in_notebook():
        from IPython.display import display,HTML,Markdown
        '''Print with newline in dataframe'''
        try : ldf = ldf.style.set_properties(**{'text-align': 'left'})
        except BaseException: pass
        return display(HTML(ldf.to_html().replace("\\n","<br>")))
    else:
        return print(ldf)