# Standard library imports
import numpy as np

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib

# Plotly imports
import plotly.graph_objects as go
import plotly
import inspect

# Internal imports
#from chimes.plots.tools._plot_tools import _plotly_colors

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


# Colors for plotly
_plotly_colors = [
    'rgba(31, 119, 180, 0.5)',    # Blue
    'rgba(255, 127, 14, 0.5)',    # Orange
    'rgba(44, 160, 44, 0.5)',     # Green
    'rgba(214, 39, 40, 0.5)',     # Red
    'rgba(148, 103, 189, 0.5)',   # Purple
    'rgba(140, 86, 75, 0.5)',     # Brown
    'rgba(227, 119, 194, 0.5)',   # Pinkish Purple
    'rgba(127, 127, 127, 0.5)',   # Gray
    'rgba(188, 189, 34, 0.5)',    # Olive Green
    'rgba(23, 190, 207, 0.5)',    # Turquoise
    'rgba(255, 0, 255, 0.5)',     # Magenta
    'rgba(0, 255, 255, 0.5)',     # Cyan
    'rgba(255, 255, 0, 0.5)',     # Yellow
    'rgba(127, 255, 127, 0.5)',   # Light Green
    'rgba(0, 0, 0, 0.5)',         # Black
    'rgba(127, 255, 255, 0.5)',   # Light Blue
    'rgba(255, 127, 255, 0.5)',   # Light Purple
    'rgba(255, 200, 0, 0.5)',     # Orange
    'rgba(200, 200, 0, 0.5)',     # Yellow-Green
    'rgba(255, 182, 193, 0.5)',   # Pink
]


def Sankey(
    nodes: dict,
    Links0: list,
    time: np.ndarray,
    Units: str = '',
    title: str = '',
    Scale: np.ndarray = False,
    returnFig: bool = False
) -> go.Figure:
    '''
    Represent the evolution of flows in the system with a scale and time slider.

    Parameters
    ----------
    - nodes (dict): Dictionary {node name: node number} that connects flows.
    - Links0 (list): List of lists, each inner list constructed as ['label', 'values over time', source_index, target_index, color_index].
    - time (np.ndarray): Time vector corresponding to each 'values over time' in Links0.
    - Units (str): Units of each flow in the Sankey diagram.
    - title (str): Title of the plot.
    - Scale (np.ndarray): Indicator of flow sizes with a reference. Same length as the time vector.
    - returnFig (bool): If True, return the plotly figure without displaying it.

    Returns
    -------
    - go.Figure: Plotly figure representing the Sankey diagram. Only if returnFig is True

    Notes:
    - If a flux is negative locally, the system automatically generate an inverse flux on those values. 

    Example
    -------
    ```
    chm.Plots.Sankey(nodes={'A': 0, 'B': 1}, 
                    Links0=[['Flow AB', np.array([10, 20, 30]), 0, 1, 0],
                            ['Flow BA', np.array([30, 20, 10]), 1, 0, 1]], 
                            time=np.array([1, 2, 3]), 
                            Units='kg/s', 
                            title='Sankey Diagram')```
    you can also check `ECHIMES` and `ICED` supplements that have in-build structures

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: 2024-01-19
    '''

    arrowlen = 15

    def link(i):
        '''
        translate the user-friendly input into dict for plotly at one frame of index i
        '''
        return dict(
            arrowlen=arrowlen,
            source=[L[2] for L in Links],
            target=[L[3] for L in Links],
            label=[L[0] for L in Links],
            value=[L[1][i] for L in Links],
            color=[_plotly_colors[L[4]] if type(L[4]) is int else L[4] for L in Links],
        )

    def scalescatter(i):
        '''
        display the scale scatter at a frame i
        '''
        return dict(
            x=[1],  # Set x-coordinate for the vertical bar (update for each frame)
            y=[Scale[i]],  # Set y-coordinate (log scale) based on Scale (update for each frame)
            mode='markers',
            marker=dict(color='black', size=15, symbol='diamond'),
            showlegend=False,
            text=['Cursor'],  # Text label for the cursor
            textposition='bottom center',  # Adjust text position
            xaxis='x2',  # Associate with the second x-axis
            yaxis='y2',  # Associate with the second y-axis
            node=Nodes, 
        )

    # LINKS UPDATE FOR NEGATIVE VALUES
    Links = []
    for L in Links0:
        if any(L[1] < 0):
            Links.append([L[0], np.maximum(L[1], 0), L[2], L[3], L[4]])
            Links.append([L[0], np.maximum(-L[1], 0), L[3], L[2], L[4]])
        else:
            Links.append(L)

    # Nodes generation
    Nodes = dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=list(nodes.keys()),
    )

    # FIGURE INITIALIZATION
    fig = plotly.subplots.make_subplots(rows=1, cols=1, specs=[[{'type': 'sankey'}]])
    fig.add_trace(go.Sankey(  # Create an initial Sankey diagram
        valueformat=".2f",
        valuesuffix=Units,
        node=Nodes,
        link=link(0),))

    if Scale:
        fig.add_trace(scalescatter(0))  # Add vertical bar

    # CREATE FRAMES ############################
    frames = [go.Frame(
        data=[go.Sankey(node=Nodes, link=link(i),),
              
              go.Scatter(**scalescatter(i))] if Scale else [go.Sankey(node=Nodes, link=link(i),)],
        name=f'{time:.2f}'
    ) for i, time in enumerate(time)]
    fig.frames = frames
    fig.update_layout(
        sliders=[{
            'steps': [{
                'args': [[f.name], {'frame': {'duration': 10, 'redraw': True}, 'mode': 'immediate'}],
                'label': str(f.name),
                'method': 'animate',
            } for f in frames],
            'transition': {'duration': 10, 'easing': 'cubic-in-out'},
        }],
        updatemenus=[{
            'buttons': [{
                'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                'label': 'Play',
                'method': 'animate'
            }],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }],
    )

    # Annotations ##############################
    if Scale:
        fig.add_annotation(  # Scale Title
            x=1,
            y=1.15,
            xref="paper",
            yref="paper",
            text='Scale',
            showarrow=False,
            font=dict(size=14),)
        fig.update_layout(  # Scale Placement
            xaxis2=dict(
                domain=[0.95, .96],
                showgrid=False,
                showticklabels=False,),
            yaxis2=dict(  # Scale scale
                type='log',
                range=[0, np.log10(max(Scale))],  # Set y-axis range
                showgrid=True,
                showline=False,
                showticklabels=True,),
        )
    fig.add_annotation(  # Slider Title
        text="Time",
        x=0.0,
        y=-.1,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=14),)

    fig.update_layout(title_text=title,
                      xaxis_range=[0, 5])
    if not returnFig:
        fig.show()
    else:
        return fig
