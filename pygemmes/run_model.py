"""
This script is used to launch the model Coping2018 from pygemmes.
"""
# imports --------------------------------------------------------------
import pygemmes as pgm
import matplotlib.pyplot as plt

# main -----------------------------------------------------------------
if __name__=='__main__':
    print('\n Usage python run_model.py\n')

    hub = pgm.Hub(model='Coping2018')
    
    # low damage function
    #hub.set_dparam(key='pi3', value=0.)
    
    hub.set_dparam(preset='coping')
    hub.set_dparam(Tmax=20)
    # business as usual
    # hub.set_dparam(key='pi1', value=0.)
    # hub.set_dparam(key='pi2', value=0.)
    # hub.set_dparam(key='pi3', value=0.)
    #hub.set_dparam(key='Tmax', value=10.)
    #hub.set_dparam(key='eta', value=0.)

    
    #hub.get_summary()
    #hub.get_Network(params=True)


    hub.run()
    hub.get_summary()
    #data = hub.get_dparam()
    #Etot = data['Emission']['value']
    #time = data['time']['value']
    #plt.plot(time, Etot)
    #plt.show()

    #dax = hub.plot()
    #dax2 = hub.plot(key=['K', 'Y', 'D', 'lambda', 'omega', 'd', 'T', 'DK', 'Dy'])  # Select the variables
    dax3 = hub.plot(key=['I', 'L', 'N', 'K', 'Y', 'D', 'lambda', 'omega', 'd', 'T', 'DK', 'Dy', 'p', 'inflation', 'pi', 'emissionreductionrate', 'Emission'])
    #dax4 = hub.plot(key=['emissionreductionrate', 'Emission', 'Eind', 'Eland', 'N'])
    
    # finalpoint = {
    #           'lambda': 0.967297870750419,
    #           'omega': 0.84547946985534,
    #           'd': -0.0771062162051694,
    #           }
    
    # R = hub.get_dparam(key=[k for k in finalpoint]+['time'], returnas=dict)
    # fig = plt.figure('3D', figsize=(10, 10))
    # cmap = plt.cm.jet_r
    # ax = plt.axes(projection='3d')
    # ax.set_xlabel(r'$\lambda$')
    # ax.set_ylabel(r'$\omega$')
    # ax.set_zlabel(r'$\d$')
    # t = R['time']['value'][:, 0]
    
    
    
    
    
    print('\nEnd of all.')
