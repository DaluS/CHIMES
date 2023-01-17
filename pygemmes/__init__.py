
"""
pyIDEE

* Version 0.9
* Last update 2023/01/03
* Developped at the environmental justice program https://environmentaljustice.georgetown.edu/#
* Contact : Paul Valcke pv229@georgetown.edu

Welcome in PyIDEE, a modular library to prototype and study dynamical systems !
This library is oriented toward generation of macroeconomic complexity models

If you find bugs, want some new extensions, or help us improve the library, please create a new issue on github
If this is the first time you open this library, please look at the tutorial file in doc/tutorial.py or better, and execute it line by line.
"""
from ._models import get_available_models, get_available_functions,get_available_model_documentation
from ._toolbox import *
from ._core import Hub
from . import _plots as plots

# MESSAGE LOGO ########################################
from ._config import __PRINTLOGO, __PRINTINTRO
import os

if __PRINTINTRO:
    print(__doc__)
    __Add2 = os.path.dirname(os.path.realpath(__file__))+"\_config.py"
    __Add3 = os.path.dirname(os.path.realpath(__file__)) + "\doc\TUTORIALS\TUTORIAL.ipynb"
    print(
f"""The ipythonNotebook is at : {__Add3}
If you want to customize pyIDEE (advancer users) like removing this message, edit : {__Add2}""")



"""
def CREATE_INTERFACE():
    import ipywidgets as widgets
    from IPython.display import display,HTML,Markdown
    from IPython.display import IFrame
    from itables import init_notebook_mode
    init_notebook_mode(all_interactive=True)
    import pandas as pd    

    def pprint(ldf):
        '''Print with newline in dataframe'''
        try : ldf = ldf.style.set_properties(**{'text-align': 'left'})
        except BaseException: pass
        return display(HTML(ldf.to_html().replace("\\n","<br>")))
        
    _PATH_HERE=os.path.abspath(os.path.dirname(__file__))
    _PARENT= os.path.abspath(os.path.join(_PATH_HERE, os.pardir))
    from pathlib import Path


    PARAMS = {}
    PARAMS['style']      = {'description_width': 'initial'}
    PARAMS['Categories'] = ['eqtype','source_exp','definition','com','group','units','symbol','isneeded']
    with open(os.path.join(_PARENT, 'README.md'), 'r') as fh: PARAMS['tutorial'] = fh.read()
    with open(os.path.join(_PARENT, 'Tutorial-model2.md'), 'r') as fh: PARAMS['tutorialmodel'] = fh.read()
    PARAMS['AllModels'] = get_available_models(details=True)
    PARAMS['FULL']      = get_available_models(FULL=True)

    if type(hub)!= Hub:
        hub=Hub('__TEMPLATE__',verb=False)
        hub.run(verb=False)

    # TAB EXPLORATION / LOAD 
    def get_Exploration0(hub):
        '''General properties of pygemmes'''
        ### Widget declaration 
        ShowPygemmes  = widgets.Button(style=PARAMS['style'],description='Pygemmes description')
        ShowModels    = widgets.Button(style=PARAMS['style'],description='Model list'          )
        ShowFields    = widgets.Button(style=PARAMS['style'],description='Fields list'         )
        ShowFunctions = widgets.Button(style=PARAMS['style'],description='Functions list'      )
        ShowPlots     = widgets.Button(style=PARAMS['style'],description='Plots list'          )
        ShowUse       = widgets.Button(style=PARAMS['style'],description='Use Tutorial'        )
        ShowWriting   = widgets.Button(style=PARAMS['style'],description='Model Tutorial'      )
        ShowClear     = widgets.Button(style=PARAMS['style'],description='Clear'               )
        ShowOut = widgets.Output()

        ### Widget Functions 
        def ShowPygemmes_event(obj):
            with ShowOut:ShowOut.clear_output();print(__doc__)
        ShowPygemmes.on_click(ShowPygemmes_event)
        def ShowModels_event(obj):
            with ShowOut:ShowOut.clear_output();display(get_available_models())
        ShowModels.on_click(ShowModels_event)
        def ShowFields_event(obj): 
            with ShowOut:ShowOut.clear_output();display(get_available_fields())
        ShowFields.on_click(ShowFields_event)
        def ShowFunctions_event(obj):
            with ShowOut:ShowOut.clear_output();display(get_available_functions())
        ShowFunctions.on_click(ShowFunctions_event)
        def ShowPlots_event(obj):
            with ShowOut:ShowOut.clear_output();display(get_available_plots())
        ShowPlots.on_click(ShowPlots_event)
        def ShowClear_event(obj):
            with ShowOut:ShowOut.clear_output()
        ShowClear.on_click(ShowClear_event)
        def ShowUse_event(obj):
            with ShowOut:ShowOut.clear_output();display(Markdown(PARAMS['tutorial']))
        ShowUse.on_click(ShowUse_event)
        def ShowWriting_event(obj):
            with ShowOut:ShowOut.clear_output();display(Markdown(PARAMS['tutorialmodel']))
        ShowWriting.on_click(ShowWriting_event)
        
        return widgets.VBox([widgets.HBox([ShowPygemmes,ShowModels,ShowFields,ShowFunctions,ShowPlots,ShowUse,ShowWriting]),
                                    ShowOut])

    def get_Loading(hub):
        '''Loading model'''
        ### Widget declaration 
        Loadout      = widgets.Output() 
        Loaddropdown = widgets.Dropdown(options=list(PARAMS['AllModels'].index),value=hub.dmodel['name'],description='Model file :')
        Loadpresets  = widgets.Dropdown(options=[None]+PARAMS['AllModels'].loc[hub.dmodel['name']].loc['Preset'], description='Preset :')
        createhub    = widgets.Button(description='LOAD !')

        def valuechange(change):
            Loadpresets.options = [None]+PARAMS['AllModels'].loc[change['new']].loc['Preset']
            with Loadout:
                Loadout.clear_output()
                display(Markdown('# Model: '+PARAMS['FULL'].loc[change['new']].loc['name']))
                display(Markdown(PARAMS['FULL'].loc[change['new']].loc['description']))
                display(Markdown(PARAMS['FULL'].loc[change['new']].loc['address']))
                if PARAMS['FULL'].loc[change['new']].loc['description'] != PARAMS['FULL'].loc[change['new']].loc['longDescription']:
                    display(Markdown(PARAMS['FULL'].loc[change['new']].loc['longDescription']))
                display(Markdown('# Presets'))
                display(pd.DataFrame(pd.DataFrame(PARAMS['FULL'].loc[change['new']].loc['presets']).transpose()['com']))
                display(Markdown('# Supplements'))
                display(PARAMS['FULL'].loc[change['new']].loc['supplements'])

                hub= Hub(Loaddropdown.value,preset=Loadpresets.value,verb=False)
        Loaddropdown.observe(valuechange, names='value')

        def createhub_event(obj):
            global hub
            with Loadout:
                hub= Hub(Loaddropdown.value,preset=Loadpresets.value,verb=True)
        createhub.on_click(createhub_event)
        return widgets.VBox([widgets.HBox([Loaddropdown,Loadpresets,createhub]),Loadout])

    def set_value(hub):     
        vardrop = widgets.Dropdown(options=list(set(hub.dmisc['dfunc_order']['parameters']
                            +hub.dmisc['dfunc_order']['differential'])
                            -set(['__ONE__','dt'])),value=list(set(hub.dmisc['dfunc_order']['parameters']
                            +hub.dmisc['dfunc_order']['differential'])
                            -set(['__ONE__','dt']))[0],description='Field to change :',style=PARAMS['style'])

        Parrallel2 = widgets.Dropdown(
            options=hub.dparam['nx']['list'],
            value=hub.dparam['nx']['list'][0],
            description='parrallel:',
            continuous_update=True
        ) 
        Region2 = widgets.Dropdown(
            options=hub.dparam['nr']['list'],
            value=hub.dparam['nr']['list'][0],
            description='Region:',
            continuous_update=True
        ) 
        Multi1 = widgets.Dropdown(
            options=hub.dparam[hub.dparam[vardrop.value]['size'][0]]['list'],
            value=hub.dparam[hub.dparam[vardrop.value]['size'][0]]['list'][0],
            description='Multi1:',
            continuous_update=True
        ) 
        Multi2 = widgets.Dropdown(
            options=hub.dparam[hub.dparam[vardrop.value]['size'][1]]['list'],
            value=hub.dparam[hub.dparam[vardrop.value]['size'][1]]['list'][0],
            description='Multi2:',
            continuous_update=True
        ) 

        def update_multi1(*args):
            Multi1.options = hub.dparam[hub.dparam[vardrop.value]['size'][0]]['list']
        def update_multi2(*args):
            Multi2.options = hub.dparam[hub.dparam[vardrop.value]['size'][1]]['list']
        vardrop.observe(update_multi1, 'value')
        vardrop.observe(update_multi2, 'value')

        def setval(vardrop,Parrallel2,Region2,Multi1,Multi2):
            IndP = hub.dparam['nx']['list'].index(Parrallel2.value)
            IndR = hub.dparam['nr']['list'].index(Region2.value)
            IndM1= hub.dparam[hub.dparam[vardrop.value]['size'][0]]['list'].index(Multi1.value)
            IndM2= hub.dparam[hub.dparam[vardrop.value]['size'][1]]['list'].index(Multi2.value)
            val = str(hub.dparam[vardrop.value]['value'][0,IndP,IndR,IndM1,IndM2]) if vardrop.value in hub.dmisc['dfunc_order']['differential'] else (str(hub.dparam[vardrop.value]['value'][  IndP,IndR,IndM1,IndM2]) if hub.dparam[vardrop.value]['group']!='Numerical' 
                else  str(hub.dparam[vardrop.value]['value']))
            return val

        setvalue =  widgets.FloatText(
            value=  setval(vardrop,Parrallel2,Region2,Multi1,Multi2) ,
            description='Set value:',
        ) 
        def update_val(*args): setvalue.value = setval(vardrop,Parrallel2,Region2,Multi1,Multi2)
        vardrop.observe(update_val,'value')
        Multi1.observe(update_val,'value')
        Multi2.observe(update_val,'value')


        clickset = widgets.Button(description='Set !')
        def clickset_event(obj):
            hub.set_dparam(vardrop.value,[Parrallel2,Region2, Multi1,Multi2,float(setvalue.value)] )
        clickset.on_click(clickset_event)           

        clicksummary = widgets.Button(description='get summary')
        clickFields =widgets.Button(description='get Fields')
        outINTROS = widgets.Output()

  
        with outINTROS:
            display(hub.get_fieldsproperties())
        display('Hello')
        def clickFields_event(obj):
            with outINTROS:
                outINTROS.clear_output()
                display(hub.get_fieldsproperties())
        clickFields.on_click(clickFields_event)

        return widgets.VBox([widgets.HBox([vardrop,setvalue,clickset]),Parrallel2,Region2,Multi1,Multi2,clickFields,outINTROS])

    # Network
    def get_network(hub):
        '''Create the HTML network'''
        createNetwork = widgets.Button(description='Create Network')
        dropdownP = widgets.Dropdown(style=PARAMS['style'],options=[True,False],value=True,description='Show parameters :')
        dropdownA = widgets.Dropdown(style=PARAMS['style'],options=[True,False],value=True,description='Show Auxilliary :')
        outnet= widgets.Output()

        def createNetwork_event(obj):
            with outnet: hub.get_Network(params=dropdownP.value,auxilliary=dropdownA)  
        createNetwork.on_click(createNetwork_event)

        return widgets.HBox([dropdownP,dropdownA,createNetwork])

    # Values summary
    def get_value(hub):
            #ValueFrame = pd.DataFrame()
            clickValues = widgets.Button(description='get values')
            
            TimeSlider = widgets.FloatRangeSlider(
                    value=[hub.dparam['time']['value'][0,0,0,0,0], hub.dparam['dt']['value']],
                    min=hub.dparam['time']['value'][0,0,0,0,0],
                    max=hub.dparam['Tmax']['value'],
                    step=hub.dparam['dt']['value'],
                    description='Time range:',
                    disabled=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='.1f',
                    continuous_update=True
                ) 

            Out1 = widgets.Output()
            Out2 = widgets.Output()
            Out3 = widgets.Output()

            def showValues(): 
                dfp = hub.get_dataframe(hub,eqtype=None,t0=0,t1=0,)
                dfd = hub.get_dataframe(hub,eqtype='differential',t0=TimeSlider.value[0],t1=TimeSlider.value[1],)
                dfs = hub.get_dataframe(hub,eqtype='statevar'    ,t0=TimeSlider.value[0],t1=TimeSlider.value[1],)
                Out1.clear_output()
                Out2.clear_output()
                Out3.clear_output()
                with Out1: 
                    display(Markdown('<p style="text-align: center;">'+' Parameters '+'</p>'))
                    pprint(dfp.transpose())
                with Out2: 
                    display(Markdown('<p style="text-align: center;">'+' Differential variables '+'</p>'))
                    pprint(dfd.transpose())
                with Out3: 
                    display(Markdown('<p style="text-align: center;">'+' State Variables '+'</p>'))
                    pprint(dfs.transpose())

            def clickValues_event(obj):
                pass
                showValues()
            clickValues.on_click(clickValues_event)
            #showValues()
            
    
            return widgets.VBox([widgets.HBox([clickValues,TimeSlider]), widgets.HBox([Out1,Out2,Out3])])


    # RUN 
    def get_run(hub):
        clickrun = widgets.Button(description='RUN!')
        outrun = widgets.Output()
        def clickrun_event(obj):
            global hub
            with outrun:
                hub.run()
        clickrun.on_click(clickrun_event)

        setReinterp =  widgets.FloatText(
        value=hub.dparam['nt']['value'],
        description='Reinterpolate on:',style=PARAMS['style'])

        #  Set  
        clickset = widgets.Button(description='Set !')
        def clickset_event(obj):
            hub.reinterpolate_dparam(int(setReinterp.value))
            with outrun:
                print("reinterpolated")
        clickset.on_click(clickset_event)

        return widgets.VBox([clickrun,widgets.HBox([setReinterp,clickset]),outrun])


    # TAB PLOTS
    def get_plot(hub):
        ########### PRESETS ############## 
        Outplot=widgets.Output()
        B1 = widgets.Button(description='Presets',style=PARAMS['style'])
        def B1e(obj): 
            with Outplot: 
                Outplot.clear_output(); 
                hub.plot_preset()
        B1.on_click(B1e)

        ########### ONE VARIABLE ########
        def PLOToneVariable(hub): 
            TimeSlider = widgets.FloatRangeSlider(
                    value=[hub.dparam['time']['value'][0,0,0,0,0], hub.dparam['Tmax']['value']],
                    min=hub.dparam['time']['value'][0,0,0,0,0],
                    max=hub.dparam['Tmax']['value'],
                    step=hub.dparam['dt']['value'],
                    description='Time range:',
                    disabled=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='.1f',
                    continuous_update=True
                ) 
            Parrallel = widgets.Dropdown(
                options=hub.dparam['nx']['list'],
                value=hub.dparam['nx']['list'][0],
                description='parrallel :',
                continuous_update=True
            ) 
            Region = widgets.Dropdown(
                options=hub.dparam['nr']['list'],
                value=hub.dparam['nr']['list'][0],
                description='Region :',
                continuous_update=True
            ) 
            Scaling = widgets.Dropdown(
                options=[True,False],
                value = False,
                description='Scaling axes'
            )
            outPLOT = widgets.Output()
            Plotvars = hub.dmisc['dfunc_order']['statevar']+hub.dmisc['dfunc_order']['differential']
            varXdrop = widgets.Dropdown(options=Plotvars,value='time',description='X axis :')
            varYdrop = widgets.Dropdown(options=Plotvars,value='time',description='Y axis :')
            varCdrop = widgets.Dropdown(options=Plotvars,value='time',description='color :')

            clickplot = widgets.Button(description='Plot !')
            def clickplot_event(obj):
                with outPLOT:
                    plots.XY(hub,x=varXdrop.value,
                                        y=varYdrop.value,
                                        color = varCdrop.value,
                                        idx=Parrallel.value,
                                        Region=Region.value,
                                        tini=TimeSlider.value[0],
                                        tend=TimeSlider.value[1],
                                        scaled=Scaling.value)
            clickplot.on_click(clickplot_event)

            clickclear = widgets.Button(description='clear')
            def clickclear_event(obj):
                with outPLOT:
                    #plt.close('all')
                    outPLOT.clear_output()
            clickclear.on_click(clickclear_event)

            return widgets.VBox([widgets.HBox([TimeSlider,Parrallel,Region]),
                                    widgets.HBox([varXdrop,varYdrop,varCdrop]),
                                    widgets.HBox([Scaling,clickplot,clickclear]),outPLOT])    

        def Plot3D(hub):
            TimeSlider = widgets.FloatRangeSlider(
                    value=[hub.dparam['time']['value'][0,0,0,0,0], hub.dparam['Tmax']['value']],
                    min=hub.dparam['time']['value'][0,0,0,0,0],
                    max=hub.dparam['Tmax']['value'],
                    step=hub.dparam['dt']['value'],
                    description='Time range:',
                    disabled=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='.1f',
                    continuous_update=True
                ) 
            Parrallel = widgets.Dropdown(
                options=hub.dparam['nx']['list'],
                value=hub.dparam['nx']['list'][0],
                description='parrallel :',
                continuous_update=True
            ) 
            Region = widgets.Dropdown(
                options=hub.dparam['nr']['list'],
                value=hub.dparam['nr']['list'][0],
                description='Region :',
                continuous_update=True
            ) 
            outPLOT = widgets.Output()
            Plotvars = hub.dmisc['dfunc_order']['statevar']+hub.dmisc['dfunc_order']['differential']
            varXdrop = widgets.Dropdown(options=Plotvars,value='time',description='X axis:')
            varYdrop = widgets.Dropdown(options=Plotvars,value='time',description='Y axis:')
            varZdrop = widgets.Dropdown(options=Plotvars,value='time',description='Z axis:')
            varCdrop = widgets.Dropdown(options=Plotvars,value='time',description='color:')

            clickplot = widgets.Button(description='Plot !')
            def clickplot_event(obj):
                with outPLOT:
                    plots.XYZ(hub,x=varXdrop.value,
                                    y=varYdrop.value,
                                    z=varZdrop.value,
                                    color = varCdrop.value,
                                    idx=Parrallel.value,
                                    Region=Region.value,
                                    tini=TimeSlider.value[0],
                                    tend=TimeSlider.value[1],)
            clickplot.on_click(clickplot_event)

            clickclear = widgets.Button(description='clear')
            def clickclear_event(obj):
                with outPLOT:
                    #plt.close('all')
                    outPLOT.clear_output()
            clickclear.on_click(clickclear_event)

            return widgets.VBox([widgets.HBox([TimeSlider,Parrallel,Region]),
                                widgets.HBox([varXdrop,varYdrop,varZdrop,varCdrop]),
                                widgets.HBox([clickplot,clickclear]),outPLOT])    

        def sensitvity(hub):
            TimeSlider = widgets.FloatRangeSlider(
                    value=[hub.dparam['time']['value'][0,0,0,0,0], hub.dparam['Tmax']['value']],
                    min=hub.dparam['time']['value'][0,0,0,0,0],
                    max=hub.dparam['Tmax']['value'],
                    step=hub.dparam['dt']['value'],
                    description='Time range:',
                    disabled=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='.1f',
                    continuous_update=True
                ) 
            Parrallel = widgets.Dropdown(
                options=hub.dparam['nx']['list'],
                value=hub.dparam['nx']['list'][0],
                description='parrallel :',
                continuous_update=True
            ) 
            Region = widgets.Dropdown(
                options=hub.dparam['nr']['list'],
                value=hub.dparam['nr']['list'][0],
                description='Region :',
                continuous_update=True
            ) 
            outPLOT = widgets.Output()
            Plotvars = hub.dmisc['dfunc_order']['statevar']+hub.dmisc['dfunc_order']['differential']
            vardrop = widgets.Dropdown(options=Plotvars,value='time',description='Variable')
            Mode = widgets.Dropdown(options=[False,'sensitivity','cycles'],value=False,description='Mode:')
            Wlog = widgets.Dropdown(options=[False,True],value=False,description='Y log')

            clickplot = widgets.Button(description='Plot !')
            def clickplot_event(obj):
                with outPLOT:
                    plots.Var(hub,vardrop.value,
                                    idx=Parrallel.value,
                                    Region=Region.value,
                                    tini=TimeSlider.value[0],
                                    tend=TimeSlider.value[1],
                                    mode=Mode.value,
                                    log=Wlog.value
                                    )
            clickplot.on_click(clickplot_event)

            clickclear = widgets.Button(description='clear')
            def clickclear_event(obj):
                with outPLOT:
                    #plt.close('all')
                    outPLOT.clear_output()
            clickclear.on_click(clickclear_event)

            return widgets.VBox([widgets.HBox([TimeSlider,Parrallel,Region]),
                                    widgets.HBox([vardrop,Mode,Wlog]),
                                    widgets.HBox([clickplot,clickclear]),outPLOT])    

        def Byunits(hub):
            display('FILTERS CANNOT WORK DUE TO HTML ISSUES')
            TimeSlider = widgets.FloatRangeSlider(
                    value=[hub.dparam['time']['value'][0,0,0,0,0], hub.dparam['Tmax']['value']],
                    min=hub.dparam['time']['value'][0,0,0,0,0],
                    max=hub.dparam['Tmax']['value'],
                    step=hub.dparam['dt']['value'],
                    description='Time range:',
                    disabled=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='.1f',
                    continuous_update=True
                ) 
            Parrallel = widgets.Dropdown(
                options=hub.dparam['nx']['list'],
                value=hub.dparam['nx']['list'][0],
                description='parrallel :',
                continuous_update=True
            ) 
            Region = widgets.Dropdown(
                options=hub.dparam['nr']['list'],
                value=hub.dparam['nr']['list'][0],
                description='Region :',
                continuous_update=True
            ) 
            outPLOT = widgets.Output()
            
            vardrop1 = widgets.Dropdown(options=['Not coded'],value='Not coded',description='Keys filter')
            vardrop2 = widgets.Dropdown(options=['Not coded'],value='Not coded',description='Units filter')
            vardrop3 = widgets.Dropdown(options=['Not coded'],value='Not coded',description='sectors filter')
            vardrop4 = widgets.Dropdown(options=['Not coded'],value='Not coded',description='separation filter')


            clickplot = widgets.Button(description='Plot !')
            def clickplot_event(obj):
                with outPLOT:
                    plots.plotbyunits(hub,
                                    idx=Parrallel.value,
                                    Region=Region.value,
                                    tini=TimeSlider.value[0],
                                    tend=TimeSlider.value[1],
                                    )
            clickplot.on_click(clickplot_event)

            clickclear = widgets.Button(description='clear')
            def clickclear_event(obj):
                with outPLOT:
                    #plt.close('all')
                    outPLOT.clear_output()
            clickclear.on_click(clickclear_event)

            return widgets.VBox([widgets.HBox([TimeSlider,Parrallel,Region]),
                                    widgets.HBox([vardrop1,vardrop2,vardrop3,vardrop4]),
                                    widgets.HBox([clickplot,clickclear]),outPLOT])    

        def plotSankey(hub):
            TimeSlider = widgets.FloatSlider(
                value=3,
                min=hub.dparam['time']['value'][0,0,0,0,0],
                max=hub.dparam['Tmax']['value'],
                step=hub.dparam['dt']['value'],
                description='Time',
                continuous_update=True,
                orientation='horizontal',
                readout_format='.1f')

            Parrallel = widgets.Dropdown(
                options=hub.dparam['nx']['list'],
                value=hub.dparam['nx']['list'][0],
                description='parrallel :',
                continuous_update=True
            ) 

            Region = widgets.Dropdown(
                options=hub.dparam['nr']['list'],
                value=hub.dparam['nr']['list'][0],
                description='Region :',
                continuous_update=True
            ) 


            #global FIGS

            outPLOT = widgets.Output()
            clickplot = widgets.Button(description='Plot !')
            def clickplot_event(obj):
                with outPLOT:
                    outPLOT.clear_output()
                    figPhy,figMoney=plots.Sankey(hub,TimeSlider.value,Parrallel.value,Region.value)
                    figPhy.show()
                    figMoney.show()
            clickplot.on_click(clickplot_event)

            def updateSankey(obj):
                #if figPhy:
                with outPLOT:
                    outPLOT.clear_output()
                    figPhy,figMoney=plots.Sankey(hub,TimeSlider.value,Parrallel.value,Region.value)
                    figPhy.show()
                    figMoney.show()  
            TimeSlider.observe(updateSankey,'value')

            return widgets.VBox([widgets.HBox([TimeSlider,Parrallel,Region]),
                                clickplot,
                                outPLOT])

        ######### PLOT BUTTONS 
        for _ in range(1):
            def B2e(obj): 
                with Outplot: Outplot.clear_output();display(Markdown('## 1 variable'));display(PLOToneVariable(hub))
            def B21e(obj): 
                with Outplot: Outplot.clear_output();display(Markdown('## Cycles and sensitivity'));display(sensitvity(hub))
            def B22e(obj): 
                with Outplot: Outplot.clear_output();display(Markdown('## 3D Plot'));display(Plot3D(hub))
            def B3e(obj): 
                with Outplot: Outplot.clear_output();display(Markdown('## Plots by units'));display(Byunits(hub))
            def B7e(obj): 
                with Outplot: Outplot.clear_output();display(Markdown('## Sankey Diagrams'));display(plotSankey(hub))
            

        
            B2 = widgets.Button(style=PARAMS['style'],description='2D plot'    );B2 .on_click(B2e)
            B21= widgets.Button(style=PARAMS['style'],description='Sensitivity');B21.on_click(B21e)
            B22= widgets.Button(style=PARAMS['style'],description='3D Plot'    );B22.on_click(B22e)
            B3 = widgets.Button(style=PARAMS['style'],description='By Units'   );B3 .on_click(B3e)  
            B4 = widgets.Button(style=PARAMS['style'],description='N Y axes'   )
            B5 = widgets.Button(style=PARAMS['style'],description='Cycles'     )
            B6 = widgets.Button(style=PARAMS['style'],description='Repartition')
            B7 = widgets.Button(style=PARAMS['style'],description='Sankey'     );B7.on_click(B7e)  


        return widgets.VBox([B1,widgets.HBox([B2,B22,B21]),
                                widgets.HBox([B3,B4,B5,B6,B7]),
                                Outplot]) 


    #########################################################################
    #                      INTERFACE TO RULE THEM ALL  
    # #######################################################################
    for _ in range(1):
        Bnames = ['PYGEMMES','Loading','Values','Run','Plot','Analysis']
        Buttons = {b : widgets.Button(description=b,style=PARAMS['style'],button_style='primary') for b in Bnames }
        OUT = widgets.Output()

        ### Widget Functions 
        def pgm_event(obj): 
            with OUT: 
                OUT.clear_output(); 
                display(Markdown('# Exploring Pygemmes content and use'))
                display(get_Exploration0(hub))
        Buttons['PYGEMMES'].on_click( pgm_event)
        def load_event(obj): 
            with OUT: 
                OUT.clear_output(); 
                display(Markdown('# Loading model'))
                display(get_Loading(hub))
                display(Markdown('# Network Representation'))
                display(Markdown('(You need to load it before)'))
                display(get_network(hub)) 
        Buttons['Loading'].on_click( load_event)
        def a_event(obj): 
            with OUT: 
                OUT.clear_output(); 
                display(Markdown('# Changing values'))
                display(set_value(hub))
                
 
                display(Markdown('# Explore fields values'))
                display(get_value(hub))
        Buttons['Values'].on_click( a_event)
        def b_event(obj): 
            with OUT: 
                OUT.clear_output(); display(Markdown('# Run the simulation')); display(get_run(hub))
        Buttons['Run'].on_click( b_event)
        def d_event(obj): 
            with OUT: 
                OUT.clear_output(); display(Markdown('## Plots')); display(get_plot(hub))
        Buttons['Plot'].on_click( d_event)
        display(widgets.VBox([widgets.HBox([Buttons['PYGEMMES'],Buttons['Values'],Buttons['Analysis']]),
                            widgets.HBox([Buttons['Loading'],Buttons['Run'],Buttons['Plot']]),
                            OUT]))

"""