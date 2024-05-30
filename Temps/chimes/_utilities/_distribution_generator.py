import numpy as np

def _GenerateIndividualSensitivity(key, mu, sigma, disttype='normal', dictpreset={}, N=10):
    '''
    Generate a preset taking random values in one distribution.
    * mu is the mean value
    * sigma is the standard deviation value
    The exception is 'uniform-bounds' in which you give the boundaries
        

    INPUT :
        * key : the field name you want to test the sensitivity
        * mu : the first parameter of your distribution (mean typically)
        * sigma : the second parameter of your distribution (std typically)
        * dispreset : dictionnary you want to add the distribution in
        * disttype : the type of distribution you pick the value on :
            1. 'log','lognormal','log-normal' for lognormal distribution
            2. 'normal','gaussian' for gaussian distribution
        * N : the number of value you want to pick

    For lognormal distribution: 
        if the mean value is 0, then its for 
    
    '''
    size = list(np.shape(mu))
    sign=np.sign(mu)
    mu=np.abs(mu)
    sigma=np.abs(sigma)
    if not size: 
        size=[N]
    size[0]=N
    if disttype in ['log', 'lognormal', 'log-normal']:
        # Calculating entry parameters for moments to be correct
        muu = np.log(mu**2/np.sqrt(mu**2 + sigma**2))
        sigmaa = np.sqrt(np.log(1+sigma**2/mu**2))
        dictpreset[key] =np.random.lognormal(muu,sigmaa,size)*sign
    elif disttype in ['normal', 'gaussian']:
        dictpreset[key] = np.random.normal(mu, sigma, size)*sign
    elif disttype in ['uniform-bounds']:
        dictpreset[key] = np.random.uniform(mu, sigma, size)*sign
    elif disttype in ['uniform']:
        dictpreset[key] = np.random.uniform(mu-sigma/2, mu+sigma/2, size)*sign
    else:
        raise Exception('wrong distribution type input')
    return dictpreset


def generate_dic_distribution(InputDic, dictpreset={}, N=10):
    '''
    Wrapup around GenerateIndividualSensitivity function, to generate multiple distributions entangled.

    InputDic should look like :
        {
        'alpha': {'mu': .02,
                  'sigma': .2,
                  'type': 'normal'},
        'k2': {'mu': 20,
               'sigma': .2,
               'type': 'log'},
        'mu': {'mu': 1.3,
               'sigma': .2,
               'type': 'uniform'},
        }

    'type' can be :
        1. 'log','lognormal','log-normal' for lognormal distribution
        2. 'normal','gaussian' for gaussian distribution
        3. 'uniform' for uniform distribution in interval [mu,sigma]

    Be careful, grid will generate N**len(InputDic.key()) run if activated !

    GenerateIndividualSensitivity :
        Generate a preset taking random values in one distribution.

    INPUT :
        * mu : the first parameter of your distribution (mean typically)
        * sigma : the second parameter of your distribution (std typically)
        * dispreset : dictionnary you want to add the distribution in
        * disttype : the type of distribution you pick the value on :
            1. 'log','lognormal','log-normal' for lognormal distribution
            2. 'normal','gaussian' for gaussian distribution
        * N : the number of value you want to pick

        IF THE DISTRIBUTION IS LOG, then mu is the median value
    '''
    dictpreset = {}
    for key, val in InputDic.items():
        dictpreset = _GenerateIndividualSensitivity(key,
                                                    val['mu'],
                                                    val['sigma'],
                                                    disttype=val['type'],
                                                    dictpreset=dictpreset,
                                                    N=N)
        dictpreset['nx']=N
    return dictpreset

