
def InitialCond_Relax(hub,relaxedvar,statevar,preset={},stepsConv=10): 
    '''
    Find new initial condition for relaxed variables so that they begin at a steady rate. 
    If lagX (differential variable) is the lag version of X (state variable),
    it finds lagX(t=0) so that $lagX(t=0)=X(t=0)$

    NOT IMPLEMENTED NOW 
    '''

    from scipy.optimize import fsolve
    def ecart(relaxedvar,statevar):
        hub.set_dparam(**preset)
        dparr=hub.get_dparam()
        return  np.sum([ (dparr[relaxedvar[i]]['value'][0,0,0,0,0] - 
                          dparr[statevar[i]  ]['value'][0,0,0,0,0]   )**2   
                          for i in range(len(relaxedvar)) ])  
                                         
    # load the preset 
    # get dparam values 


def InitialCond_Relax_far(hub,preset={},stepsP=10,stepsConv=10): 
    '''
    Iterative method to go from one preset to the other, if the equilibrium is tought to find.
    Start at the initial parameters/conditions
    Then generate intermediary preset that mix original state, and the final state, 
    find the right initial condition, then go on the next one. 
    '''