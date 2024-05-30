import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

from ._plot_tools import _indexes, _key


def ParrallelRegion(hub, par_reg, typ='parrallel'):
    # par_reg management

    if type(par_reg) is bool and par_reg is True:
        R = hub.get_dfields()
        if typ == 'parrallel':
            out = np.arange(R['nx']['value'])
        else:
            out = np.arange(R['nr']['value'])
    elif par_reg is False:
        out = [0]
    elif type(par_reg) in [str]:
        out = [par_reg]
    elif type(par_reg) in [list, np.ndarray]:
        out = par_reg
    else:
        raise Exception(f'''Type of input for parrallel and region not understood !
                        \n You have given {par_reg}
                        \n it should be a list, a boolean, str or index value''')
    return out


def Prepare_data(hubs, variables=(), x='time', parrallel=True, Regions=True, tini=0, tend=-1):
    """
    return dict with key as field names, value as dictionnary, with each key being a model name 
    """

    # Transform hubs into a dictionnary ##############
    hublist = []
    # Manage hubs alone as list of one element
    if type(hubs) not in [list, dict]:
        hublist = [{'hub': hubs}]
    # Transform hub list into a dictionnary
    if type(hubs) is list:
        for hub in hubs:
            hublist.append({'hub': hub, })

    # Manage variables introduction
    tempvar = []
    if type(variables) is tuple:
        for dhub in hublist:
            tempvar.extend([f for f in dhub['hub'].dmisc['dfunc_order']['statevar'] +
                            dhub['hub'].dmisc['dfunc_order']['differential'] if f not in variables])
        variables = list(set(tempvar))
        variables = tempvar

    XOut = {}
    YOut = {k: {} for k in variables}
    # Work of the list dictionnary
    alreadyhub = []  # check that we have unique names
    for dhub in hublist:
        # Unload the data
        if 'hub' not in dhub.keys():
            raise Exception('You need to put each hub with the keyword "hub" ')
        hub = dhub['hub']
        region = dhub.get('nr', ParrallelRegion(hub, Regions, 'region'))
        parrallel = dhub.get('nx', ParrallelRegion(hub, parrallel))
        tini = dhub.get('tini', tini)
        tend = dhub.get('tend', tend)
        R = hub.get_dfields()

        # IF hubs have the same
        name = hub.name
        if name in alreadyhub:
            preset = hub._dflags.get('preset', False)
            if preset:
                name += '_'+preset
            else:
                name += '_'+1
        alreadyhub.append(name)

        # Generate the y values
        for key in [f for f in variables if f in hub.dmisc['dfunc_order']['statevar'] +
                    hub.dmisc['dfunc_order']['differential']]:
            for r in region:
                for p in parrallel:
                    # NAME MANAGEMENT
                    key, keysector, key_name = _key(R, key)

                    if len(region) > 1:
                        if type(r) is int:
                            name += '^'+R['nr']['list'][r]
                        else:
                            name += '^'+str(r)
                    if len(parrallel) > 1:
                        if type(p) is int:
                            name += '^'+R['nx']['list'][r]
                        else:
                            name += '^'+str(p)
                    if key_name:
                        name += '_'+key_name

                    # Adding the value
                    hub, idx, Region, idt0, idt1 = _indexes(hub, p, r)
                    ms2 = 0
                    YOut[key][name] = R[key]['value'][idt0:idt1, idx, Region, keysector, ms2]
                    XOut[name] = R[x]['value'][tini:tend, 0, 0, 0, 0]
    return XOut, YOut


def data_display(XOut, YOut, model_colors, title='', xlabel='time'):

    # Determine the graph dimensions in row and columns
    NbGraphs = len(YOut.keys())
    rows = int(np.sqrt(NbGraphs))
    cols = int(np.ceil(NbGraphs/rows))

    subplot_titles = [f"{variable}" for variable in YOut.keys()]
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=subplot_titles)
    idd = {k: 0 for k in XOut.keys()}
    # Use a counter to track the subplot position
    subplot_counter = 1

    # Iterate through each variable (K, employment, wage share, etc.)
    for variable_name, models_data in YOut.items():
        row = (subplot_counter - 1) // cols + 1
        col = (subplot_counter - 1) % cols + 1

        # Iterate through each model's data within the variable
        for model_name, y_data in models_data.items():
            time_array = XOut[model_name]
            # Assign a legend group for each unique model name
            legend_group = model_name

            # Add a trace for the current model's data
            fig.add_trace(
                go.Scatter(
                    x=time_array, y=y_data,
                    mode='lines',
                    name=model_name,
                    legendgroup=legend_group,
                    line=dict(color=model_colors[legend_group]),
                    showlegend=True if idd[model_name] == 0 else False
                ),
                row=row, col=col
            )

            if xlabel != 'time':
                fig['layout']['yaxis'+str(subplot_counter)]['title'] = variable_name
                fig['layout']['xaxis'+str(subplot_counter)]['title'] = xlabel
            idd[model_name] += 1

        subplot_counter += 1

    # Update the layout to show legends and adjust the plot size
    fig.update_layout(
        height=600, width=1200,
        title_text=title,
        legend=dict(orientation="h"),  # Horizontal legend below the plot
        legend_title_text='Model:'
    )

    return fig
