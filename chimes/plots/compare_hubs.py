from chimes.plots.tools.compare_run import Prepare_data
from chimes.plots.tools.compare_run import data_display
from chimes.plots.tools._plot_tools import _plotly_colors


def compare_hubs(
        hubs,
        variables=(),
        x='time',
        idx=True,
        region=True,
        tini=0,
        tend=-1,
        lw=1,
        title='',
        returnFig=False):
    '''
    Compare multiple Hubs, parrallel runs of a hub or different regions of a Hub
    '''
    XOut, YOut = Prepare_data(hubs, variables=variables, x=x, parrallel=idx, Regions=region, tini=tini, tend=tend)

    # Sort the unique model names to ensure consistent color assignment
    unique_models_sorted = sorted(set(
        model_name
        for data_dict in YOut.values()
        for model_name in data_dict.keys()
    ))

    # Assign a color to each model using a fixed color palette
    color_palette = _plotly_colors
    model_colors = {
        model: color_palette[i % len(color_palette)]
        for i, model in enumerate(unique_models_sorted)
    }

    fig = data_display(XOut, YOut, model_colors, title, xlabel=x)  # Pass model_colors here

    if returnFig:
        fig.show()
    else:
        return fig
