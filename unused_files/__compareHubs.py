'''
One hub, multiple elements inside (multiple regions, parrallel runs)
input: hub : all parrallel, all regions plotted separately
hub, parallel=[ list of integers ], region = [list of integers ] : only the one in the list are plotted
hub, parallel=[ list of strings ], region = [list of of strings ]: conversion of string names into indexes, same as above

List of hubs
[hub1,hub2],region = [ list], parallel = [list ] : iterate the parameters on each hub, with the region and the parallel corresponding in the order
[hub1,hub2,hub3], region = [ 2,1,1], parallel = ['test',0,'extreme']:
plot hub1, region 2, parallel 'test'
plot hub2, region 1, parallel 0
plot hub3, region 1, parallel 'extreme'
'''
import numpy as np


# Fake raw data
t1 = np.arange(0.0, 100, 0.01)
t2 = np.arange(0.0, 100, 0.1)
t3 = np.arange(10, 80, 0.1)
t4 = np.arange(20, 80, 0.01)

ydata1 = np.sin(2 * np.pi * t1)
ydata2 = np.cos(2 * np.pi * t2)
ydata3 = 0.1*np.exp(0.01 * t1)*np.sin(2 * np.pi * t1)
ydata4 = .35*np.exp(0.01 * t2)
ydata5 = np.exp(0.01 * t1)
ydata6 = np.exp(0.01 * t2-0.01*t2**2)
ydata7 = np.exp(0.01 * t1)
ydata8 = np.exp(0.01 * t2)
ydata9 = np.exp(0.01 * t3)
ydata10 = np.exp(0.01 * t1)
ydata11 = np.exp(0.01 * t2)
ydata12 = np.exp(0.01 * t4)

x = {'GK_01^US': t1,
     'GEMMES_02^WORLD': t2,
     'Anothermodel': t3,
     'Yetanothermodel': t4},


FAKE_DATA = {
    'K': {
        'GK_01^US': ydata1,
        'GEMMES_02^WORLD': ydata2, },
    'employment': {
        'GK_01^US': ydata3,
        'GEMMES_02^WORLD': ydata4, },
    'wage share': {
        'GK_01^US': ydata5,
        'GEMMES_02^WORLD': ydata6, },
    'Emissions': {
        'GK_01^US': ydata7,
        'GEMMES_02^WORLD': ydata8,
        'Anothermodel': ydata9},
    'employment2': {
        'GK_01^US': ydata10,
        'GEMMES_02^WORLD': ydata11, },
    'External': {
        'Yetanothermodel': ydata12},
}
# Finding categories to know what plots to consider
ordered_dict = {}
for entry_name, entry_dict in FAKE_DATA.items():
    ordered_keys = sorted(entry_dict.keys())
    key_str = ', '.join(ordered_keys)
    ordered_dict[key_str] = entry_name
# Colors : the format is the most practical for you
    OUTcolors = {'GK_01^US': '',
                 'GEMMES_02^WORLD': ''}

#    return FAKE_DATA, ordered_dict, OUTcolors

'''
def compare_hubs(
        hub,
        idx=False,
        region=False,
        tini=False,
        tend=False,

        filters_key=(),
        filters_units=(),

        lw=1,
        title='',
        returnFig=False):

    OUT1 = data_processing(hub, idx, region, tini, tend)
    F = data_display(OUT1)

    if returnFig:
        F.show()
    else:
        return F
'''
