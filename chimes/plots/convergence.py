import numpy as np

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib
import matplotlib as mpl

# Matplotlib RCParams useful elements
matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
plt.rcParams.update({'font.size': 10})
params = {'legend.fontsize': 6,
          'legend.handlelength': 0,
          'legend.borderpad': 0,
          'legend.labelspacing': 0.0}
SIZETICKS = 20
SIZEFONT = 10
LEGENDSIZE = 20
LEGENDHANDLELENGTH = 2


def convergence(hub, finalpoint: dict, showtrajectory=False, returnFig=False):
    """
    Visualize the convergence of a simulation in a 3D phase space.

    Parameters:
        hub (Hub): The chimeshub object.
        finalpoint (dict): Dictionary containing the final points in the phase space dimensions dict(x=3,y=2,z=1).
        showtrajectory (bool, optional): Whether to show the trajectory of converging points. Defaults to False.
        returnFig (bool, optional): Whether to return the figure object. Defaults to False.

    Raises:
        Exception: If the length of finalpoint keys is not equal to 3.

    Returns:
        matplotlib.figure.Figure or None: If returnFig is True, returns the figure object, otherwise, None.

    Note:
        This method plots the convergence of a simulation in a 3D phase space. It visualizes the final points 
        as scatter points and optionally shows the trajectory of converging points. The color of scatter points 
        represents the convergence rate.

    """
    if len(finalpoint.keys()) != 3:
        raise Exception('Use three dimensions for your phase space!')

    # Plot of everything ####################
    ConvergeRate = hub.calculate_ConvergeRate(finalpoint)

    # Create a new figure
    fig = plt.figure()

    # Create a 3D axes
    ax = plt.axes(projection='3d')

    keys = list(finalpoint.keys())

    # Scatter plot of final points
    ax.scatter(finalpoint[keys[0]], finalpoint[keys[1]], finalpoint[keys[2]], s=100, c='k')

    # Scatter plot with color representing convergence rate
    R = hub.get_dfields(key=list(finalpoint.keys()) + ['time'], returnas=dict)
    scat = ax.scatter(R[keys[0]]['value'][0, ConvergeRate > 0.0001],
                      R[keys[1]]['value'][0, ConvergeRate > 0.0001],
                      R[keys[2]]['value'][0, ConvergeRate > 0.0001],
                      c=ConvergeRate[ConvergeRate > 0.0001],
                      cmap='jet',
                      norm=mpl.colors.LogNorm(vmin=np.amin(ConvergeRate[ConvergeRate > 0.01])))

    # Add trajectory of converging points if required
    if showtrajectory:
        for i in range(len(ConvergeRate)):
            if ConvergeRate[i] > 0:
                ax.plot(R[keys[0]]['value'][:, i, 0, 0, 0],
                        R[keys[1]]['value'][:, i, 0, 0, 0],
                        R[keys[2]]['value'][:, i, 0, 0, 0], c='k', lw=0.1)

    # Set axis labels
    ax.set_xlabel(R[keys[0]]['symbol'])
    ax.set_ylabel(R[keys[1]]['symbol'])
    ax.set_zlabel(R[keys[2]]['symbol'])

    # Add colorbar
    cbar = fig.colorbar(scat)
    cbar.ax.set_ylabel(r'$f_{carac}^{stab} (y^{-1})$')

    # Show the plot
    plt.show()

    # Return the figure object if required
    if returnFig:
        return fig
