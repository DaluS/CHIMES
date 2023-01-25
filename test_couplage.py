import pygemmes as pgm
import matplotlib.pyplot as plt

regions = ["World"]
rm = ["Copper", "LowAlloySteel"]
simulation_start_time_variable = 2010
simulation_end_time_variable = 2020
solver = 'eRK4-mater'


def materplot(scenario):
    plt.clf()
    plt.figure()
    scenario.plot(
        "TURMFlow",
        region=regions,
        tu=["PLDVFossil"],
        rm=rm,
        kind="area",
        title="Copper flow consumption",
        init_time=simulation_start_time_variable,
        final_time=simulation_end_time_variable,
    )
    plt.show()


def materplot2(scenario):
    scenario.plot(
         "TURMFlowProduction",
         region=regions,
         tu=["PLDVFossil"],
         rm=rm,
         kind="area",
         title="Copper flow production",
         init_time=simulation_start_time_variable,
         final_time=simulation_end_time_variable,
    )
    plt.show()


def main_run():

    print('Main_run launched')

    hub = pgm.Hub(model='Coping2018', preset='BAU')

    print('Hub Coping2018 ok')

    hub.set_dparam(key='dt', value=1./12)
    hub.set_dparam(key='Tmax', value=2020)
    print('Before hub.run')
    scenario = hub.run(solver='eRK4-mater')
    print('After hub.run')
    # pour faire le run
    # former argument solver = 'eRK4-mater' does no longer work

    # dax = hub.plot(key=["g", "lambda", "omega", "d",
    #                "N", "Eland", "T", "Pi"])

    return hub, scenario
