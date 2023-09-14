# CHIMES IMPORTS
from .._core import Hub
from .._models import get_available_models, get_available_functions,get_model_documentation,get_available_operators
from .._toolbox import get_available_plots, get_available_fields
from .._plots import _plots as plots
# CLASSIC LIBRARIES
import pandas as pd
import numpy as np

import ipywidgets as widgets

from IPython.display import display,HTML,Markdown
from IPython.display import IFrame
from itables import init_notebook_mode,options
options.columnDefs = [{"className": "dt-left", "targets": "_all"}]
options.classes="display nowrap compact"
options.scrollY="400px"
options.scrollCollapse=True
options.paging=False
pd.set_option('display.max_colwidth', None)
pd.set_option("display.colheader_justify","left")


from pandasgui import show

path = "C:\\Users\\Paul Valcke\\Documents\\GitHub\\GEMMES"
################################## PREPARATION FOR THE INTERFACE ###################################


class Interface:
    '''
    Interface for CHIMES, to avoid doing command-line approaches 
    
    Need to find a way to implement supplements
    '''
    def get_Exploration0(self):
        '''General properties of CHIMES'''
        
        #### PSEUDODECORATOR
        ShowOut = widgets.Output()    
        def clear_output_decorator2(func):
            def wrapper(*args, **kwargs):
                with ShowOut:
                    ShowOut.clear_output()
                    func(*args, **kwargs)
            return wrapper
 
        
        ### Widget declaration 
        @clear_output_decorator2
        def ShowModels_event(obj):   
            display(Markdown('If you want to know more about one specific model, go in the loading tab'))
            display(get_available_models())
        @clear_output_decorator2
        def ShowFields_event(obj):   display(get_available_fields(exploreModels=True))
        @clear_output_decorator2
        def ShowFunctions_event(obj):display(get_available_functions())
        @clear_output_decorator2
        def ShowPlots_event(obj):    display(get_available_plots())
        @clear_output_decorator2
        def ShowClear_event(obj):    pass
        @clear_output_decorator2
        def ShowUse_event(obj):      display(Markdown(self.PARAMS['tutorial']))
        @clear_output_decorator2
        def ShowWriting_event(obj):  display(Markdown(self.PARAMS['tutorialmodel']))
        @clear_output_decorator2
        def ShowWoperators_event(obj): display(get_available_operators())
            
            
        Bnames2 = {'Readme'  : {
                    'function':ShowUse_event,
                    'tooltip': '',
                    },
                  'Models list' : {
                    'function':ShowModels_event,
                    'tooltip': 'All models available in the system',
                    }, 
                  'Plots list'     : {
                    'function':ShowPlots_event,
                    'tooltip': 'All existing plots for simulations',
                    },
                  'Write a model'  : {
                    'function':ShowWriting_event,
                    'tooltip': 'Guide on how you can write your own models',
                    },
                  'Fields list'    : {
                    'function':ShowFields_event,
                    'tooltip': 'All quantities covered by models',
                    },
                  'Operators list'    : {
                    'function':ShowWoperators_event,
                    'tooltip': 'All Multi-regional, multi-sector, multi-agent operators',
                    },
                  'Functions list'    : {
                    'function':ShowFunctions_event,
                    'tooltip': 'Show all explicit functions with their doc',
                    },
                   'Clear'    : {
                    'function':ShowClear_event,
                    'tooltip': 'Clear Output',
                    },
        }
        Buttons2 = {b : widgets.Button(description=b,
                                       style=self.PARAMS['style'],
                                       #button_style='primary'
                                       ) for b in Bnames2.keys() }
        for b in Bnames2.keys(): Buttons2[b].on_click( Bnames2[b]['function'])    
        return widgets.VBox([widgets.HBox(list(Buttons2.values())),
                             ShowOut])

    def get_Loading(self):
        '''Loading model page'''
        LoadOut      = widgets.Output() 
        def clear_output_decorator2(func):
            def wrapper(*args, **kwargs):
                with LoadOut:
                    LoadOut.clear_output()
                    func(*args, **kwargs)
            return wrapper
                
        # ALL MODEL LIST 
        @clear_output_decorator2
        def ShowModels_event(obj):   
            display(Markdown('If you want to know more about one specific model, go in the loading tab'))
            display(get_available_models())        
        
        @clear_output_decorator2
        def createhub_event(obj):
            with LoadOut:
                try:
                    self.hub= Hub(Buttons3['Model'].value,preset=Buttons3['Preset'].value)
                    Buttons3['Load'].button_style='success'
                except BaseException as E:
                    print('select a model ')   
                    print(E)   

        @clear_output_decorator2
        def clear(obj):
            pass

        Bnames3 = {'Show list' : {
                    'function':ShowModels_event,
                    'tooltip': 'All models available in the system',
                    }, 
                   'Load': {
                    'function': createhub_event,
                    'tooltip': 'Load selected model and preset',
                    'button_style':'warning'
                   },
                  #  'Clear': {
                  #  'function': clear,
                  #  'tooltip': 'Load selected model and preset',
                  #  'button_style':''
                  # }
        }
        
        Dropnames={'Model':{
                    'value':'__TEMPLATE__',#self.hub.dmodel['name'],
                    'options':[None]+list(self.PARAMS['AllModels'].keys()),
                    'tooltip':'Model to explore',
                    },
                   'Preset':{
                    'value':None,
                    'options':[None]+list(self.PARAMS['AllModels'][self.hub.dmodel['name']]['Preset']),
                    'tooltip':'Preset to load',
                    },
                   }

        Buttons3 = {b : widgets.Button(description=b,
                                       style=self.PARAMS['style'],
                                       button_style=Bnames3[b].get('button_style','info')
                                       ) for b in Bnames3.keys() }
        for b in Bnames3.keys(): Buttons3[b].on_click( Bnames3[b]['function'])   

        for k,v in Dropnames.items():
            Buttons3[k]=widgets.Dropdown(description=k,**v)
          
        def valuechange(change):
            if Buttons3['Model'].value is not None:
                liste = self.PARAMS['AllModels'][Buttons3['Model'].value]['Preset']
            else:
                liste=[]
            Buttons3['Preset'].options = [None]+liste
            with LoadOut:
                LoadOut.clear_output()
                display(get_model_documentation(Buttons3['Model'].value))
                self.hub= Hub(Buttons3['Model'].value,preset=Buttons3['Preset'].value,verb=False)

        # Create a checkbox widget
        checkbox = widgets.Checkbox(
            value=False,  # Initial value (True or False)
            description='Verbatim',  # Label for the checkbox
            disabled=False  # Set to True to disable the checkbox
        )

        Buttons3['Model'].observe(valuechange, names='value')
            


        return widgets.VBox([widgets.HBox([Buttons3['Show list'],
                                           Buttons3['Model'],
                                           Buttons3['Preset'],
                                           Buttons3['Load'],
                                           checkbox,
                                           #Buttons3['Clear'],
                                           ]),
                             LoadOut])
 
    def get_network(self): # Network
        '''Create the HTML network'''
        createNetwork = widgets.Button(description='Create Network',button_style='success')
        outnet= widgets.Output()
        dchecks = {
            'Parameters': {
                'value': False,
                'tooltip': 'Show parameters',
                'disabled': False,
                },
            'Auxilliary': {
                'value': False,
                'tooltip': 'Show non-causal variables',
                'disabled': False,
                },
            'Redirect': {
                'value': False,
                'tooltip': 'Redirect causality of hidden variables',
                'disabled': False,
                },
        }
                
        list_input = widgets.Text(
            value='',
            description='Filter',
            tooltip= "['field1','field2'] to select what fields you keep, () for what you remove"
        )
        
        dbuttons_network= {k:widgets.Checkbox(description=k,style=self.PARAMS['style'],**v) for k,v in dchecks.items()}


        def parse_string_list_tuple(input_str):
            try:
                parsed_list = eval(input_str)
                if isinstance(parsed_list, list) and all(isinstance(item, str) for item in parsed_list):
                    return parsed_list
                elif isinstance(parsed_list, tuple) and all(isinstance(item, str) for item in parsed_list):
                    return parsed_list
                else:
                    raise ValueError("Input is not a valid list of strings in a list or tuple")
            except (SyntaxError, ValueError):
                return ()

        def createNetwork_event(obj):
            with outnet: 
                outnet.clear_output()
                self.hub.get_Network(params    =dbuttons_network['Parameters'].value,
                                     auxilliary=dbuttons_network['Auxilliary'].value,
                                     redirect  =dbuttons_network['Redirect'].value,
                                     filters    =parse_string_list_tuple(list_input.value)) 
                outnet.clear_output()
        createNetwork.on_click(createNetwork_event)

        return widgets.VBox([
                widgets.HBox([dbuttons_network['Parameters'],
                             dbuttons_network['Auxilliary'],
                             dbuttons_network['Redirect'],
                             list_input,
                             createNetwork]),
                            outnet])

    def get_run(self):
        clickrun = widgets.Button(description='RUN!',button_style='primary')
        outrun = widgets.Output()

        OutputSize = widgets.Text(
            value=str(self.hub.dparam['nt']['value']),
            description='Number of output time slices',
            tooltip= "Put an integer !",
            style=self.PARAMS['style']
        )
        InputSize = widgets.Text(
            value=str(self.hub.dparam['nt']['value']),
            description='Number of timestep',
            tooltip= "Put an integer !",
            style=self.PARAMS['style']
        )
        verbat=widgets.Checkbox(
            value=False,
            description='Counter in the run',
            disabled=False,
            indent=False
        )

        def parse_string_int(input_str):
            parsed = eval(input_str)
            if type(parsed) is int:
                return int(parsed)
            else:
                print('Input misunderstood')
                return False


        def clickrun_event(obj):
            with outrun:
                outrun.clear_output()
  
                if verbat.value: verb = 0.2 
                else: verb=0
                self.hub.run(NtimeOutput=parse_string_int(OutputSize.value),
                             NstepsInput=parse_string_int(InputSize.value),
                             verb= verb) 
                print('test')
        clickrun.on_click(clickrun_event)

        return widgets.VBox([widgets.HBox([InputSize,
                             OutputSize,
                             verbat,]),clickrun,outrun])

    def get_set(self):
        ''' 
        
        '''
        def showSummary(obj):
            alldicts=self.hub.get_new_summary()
            show(**alldicts)
        def setvalue(obj):
            self.hub.set_dparam(**eval(SetDparamText.value))
            clickSET.button_style='success'
        #### GET DATA IN PANDASGUI
        clickGUI = widgets.Button(description='Show fields!',button_style='primary')
        clickGUI.on_click(showSummary)


    
        #### NUMERICAL ENTRY
        SetParrallel=  widgets.Text(
            value=str(self.hub.dmisc['dmulti']['NxNr'][0]),
            description='Number of parrallel systems',
            tooltip= "",
            style=self.PARAMS['style']
        )
        
        SetRegion=  widgets.Text(
            value=str(self.hub.dmisc['dmulti']['NxNr'][1]),
            description='Number of spatial regions',
            tooltip= "",
            style=self.PARAMS['style']
        )

        SetTmax=  widgets.Text(
            value=str(self.hub.dparam['Tmax']['value']),
            description='Simulation length',
            tooltip= "",
            style=self.PARAMS['style']
        )
    

        # SET_DPARAM EXPRESSION 
        SetDparamText = widgets.Text(
            value="{'a':100,'b':10}",
            description='Dictionnary entry get_dparam',
            tooltip= "",
            style=self.PARAMS['style']
        )
            
        # BUTTON
        clickSETR = widgets.Button(description='Change',button_style='warning')
        clickSETP = widgets.Button(description='Change',button_style='warning')
        clickSETT = widgets.Button(description='Change',button_style='warning')
        clickSET = widgets.Button(description='Set New parameters !',button_style='warning')
               
        def parse_string_list_int(s):
            try: 
                parsed=eval(s)      
                if isinstance(parsed,list)  and all(isinstance(item, str) for item in parsed):
                    return parsed 
                elif isinstance(parsed,int):
                    return parsed
            except (SyntaxError, ValueError):
                return ()                 
        def parse_string_list_tuple(input_str):
            try:
                parsed_list = eval(input_str)
                if isinstance(parsed_list, list) and all(isinstance(item, str) for item in parsed_list):
                    return parsed_list
                elif isinstance(parsed_list, tuple) and all(isinstance(item, str) for item in parsed_list):
                    return parsed_list
                else:
                    raise ValueError("Input is not a valid list of strings in a list or tuple")
            except (SyntaxError, ValueError):
                return ()        
        clickSET.on_click(setvalue)
        
        
        ################ CHAOTIC INSTANCE TEMP ##################
        FIELDS = self.hub.dmisc['dfunc_order']['differential']+self.hub.dmisc['dfunc_order']['parameters']
        FIELDS = list(set(FIELDS)-set(['nx','nr','Nprod','__ONE__','Tmax','Tini','dt','time']))

        for f in FIELDS: 
            print(f)
            print(self.hub.dparam[f]['value'][0,0,0,0,0])

        buttons = {f: {'value':str(self.hub.dparam[f]['value'][0,0,0,0,0]),
                       'description':self.hub.dparam[f]['description'],
                       'tooltip': self.hub.dparam[f].get('com','')} for f in FIELDS}
        dsets =  {f :widgets.Text(
            style=self.PARAMS['style'],**v
        ) for f,v in buttons.items()}
  

        #########################################################

        return widgets.VBox([widgets.HTML(value='<strong>Explore fields values</strong>'),
                             clickGUI,
                             widgets.HTML(value='<strong>Set numerical fields</strong>'),
                             widgets.HBox([SetParrallel,clickSETP]),
                             widgets.HBox([SetRegion,clickSETR]),
                             widgets.HBox([SetTmax,clickSETT]),
                             widgets.HTML(value='<strong>Set general</strong>'),
                             widgets.HBox([SetDparamText,clickSET]),
                             widgets.HTML(value='<strong>Set details</strong>'),
                             *list(dsets.values())])


    # TAB PLOTS
    def get_plot(self):
        ########### PRESETS ############## 
        Outplot=widgets.Output()
        B1 = widgets.Button(description='Presets',style=self.PARAMS['style'])
        def B1e(obj): 
            with Outplot: 
                Outplot.clear_output(); 
                self.hub.plot_preset()
        B1.on_click(B1e)

        ########### ONE VARIABLE ########
        def PLOToneVariable(hub): 
            TimeSlider = widgets.FloatRangeSlider(
                    value=[self.hub.dparam['time']['value'][0,0,0,0,0], 
                           self.hub.dparam['Tmax']['value']],
                    min=self.hub.dparam['time']['value'][0,0,0,0,0],
                    max=self.hub.dparam['Tmax']['value'],
                    step=self.hub.dparam['dt']['value'],
                    description='Time range:',
                    disabled=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='.1f',
                    continuous_update=True
                ) 
            Parrallel = widgets.Dropdown(
                options=self.hub.dparam['nx']['list'],
                value=self.hub.dparam['nx']['list'][0],
                description='parrallel :',
                continuous_update=True
            ) 
            Region = widgets.Dropdown(
                options=self.hub.dparam['nr']['list'],
                value=self.hub.dparam['nr']['list'][0],
                description='Region :',
                continuous_update=True
            ) 
            Scaling = widgets.Dropdown(
                options=[True,False],
                value = False,
                description='Scaling axes'
            )
            outPLOT = widgets.Output()
            Plotvars = self.hub.dmisc['dfunc_order']['statevar']+self.hub.dmisc['dfunc_order']['differential']
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
                    value=[self.hub.dparam['time']['value'][0,0,0,0,0], self.hub.dparam['Tmax']['value']],
                    min=self.hub.dparam['time']['value'][0,0,0,0,0],
                    max=self.hub.dparam['Tmax']['value'],
                    step=self.hub.dparam['dt']['value'],
                    description='Time range:',
                    disabled=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='.1f',
                    continuous_update=True
                ) 
            Parrallel = widgets.Dropdown(
                options=self.hub.dparam['nx']['list'],
                value=self.hub.dparam['nx']['list'][0],
                description='parrallel :',
                continuous_update=True
            ) 
            Region = widgets.Dropdown(
                options=self.hub.dparam['nr']['list'],
                value=self.hub.dparam['nr']['list'][0],
                description='Region :',
                continuous_update=True
            ) 
            outPLOT = widgets.Output()
            Plotvars = self.hub.dmisc['dfunc_order']['statevar']+self.hub.dmisc['dfunc_order']['differential']
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
                    value=[self.hub.dparam['time']['value'][0,0,0,0,0], self.hub.dparam['Tmax']['value']],
                    min=self.hub.dparam['time']['value'][0,0,0,0,0],
                    max=self.hub.dparam['Tmax']['value'],
                    step=self.hub.dparam['dt']['value'],
                    description='Time range:',
                    disabled=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='.1f',
                    continuous_update=True
                ) 
            Parrallel = widgets.Dropdown(
                options=self.hub.dparam['nx']['list'],
                value=self.hub.dparam['nx']['list'][0],
                description='parrallel :',
                continuous_update=True
            ) 
            Region = widgets.Dropdown(
                options=self.hub.dparam['nr']['list'],
                value=self.hub.dparam['nr']['list'][0],
                description='Region :',
                continuous_update=True
            ) 
            outPLOT = widgets.Output()
            Plotvars = self.hub.dmisc['dfunc_order']['statevar']+self.hub.dmisc['dfunc_order']['differential']
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
                    value=[self.hub.dparam['time']['value'][0,0,0,0,0], 
                           self.hub.dparam['Tmax']['value']],
                    min=self.hub.dparam['time']['value'][0,0,0,0,0],
                    max=self.hub.dparam['Tmax']['value'],
                    step=self.hub.dparam['dt']['value'],
                    description='Time range:',
                    disabled=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='.1f',
                    continuous_update=True
                ) 
            Parrallel = widgets.Dropdown(
                options=self.hub.dparam['nx']['list'],
                value=self.hub.dparam['nx']['list'][0],
                description='parrallel :',
                continuous_update=True
            ) 
            Region = widgets.Dropdown(
                options=self.hub.dparam['nr']['list'],
                value=self.hub.dparam['nr']['list'][0],
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
                min=self.hub.dparam['time']['value'][0,0,0,0,0],
                max=self.hub.dparam['Tmax']['value'],
                step=self.hub.dparam['dt']['value'],
                description='Time',
                continuous_update=True,
                orientation='horizontal',
                readout_format='.1f')

            Parrallel = widgets.Dropdown(
                options=self.hub.dparam['nx']['list'],
                value=self.hub.dparam['nx']['list'][0],
                description='parrallel :',
                continuous_update=True
            ) 

            Region = widgets.Dropdown(
                options=self.hub.dparam['nr']['list'],
                value=self.hub.dparam['nr']['list'][0],
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
                with Outplot: Outplot.clear_output();display(Markdown('## 1 variable'));display(PLOToneVariable(self.hub))
            def B21e(obj): 
                with Outplot: Outplot.clear_output();display(Markdown('## Cycles and sensitivity'));display(sensitvity(self.hub))
            def B22e(obj): 
                with Outplot: Outplot.clear_output();display(Markdown('## 3D Plot'));display(Plot3D(self.hub))
            def B3e(obj): 
                with Outplot: Outplot.clear_output();display(Markdown('## Plots by units'));display(Byunits(self.hub))
            def B7e(obj): 
                with Outplot: Outplot.clear_output();display(Markdown('## Sankey Diagrams'));display(plotSankey(self.hub))
            

        
            B2 = widgets.Button(style=self.PARAMS['style'],description='2D plot'    );B2 .on_click(B2e)
            B21= widgets.Button(style=self.PARAMS['style'],description='Sensitivity');B21.on_click(B21e)
            B22= widgets.Button(style=self.PARAMS['style'],description='3D Plot'    );B22.on_click(B22e)
            B3 = widgets.Button(style=self.PARAMS['style'],description='By Units'   );B3 .on_click(B3e)  
            B4 = widgets.Button(style=self.PARAMS['style'],description='N Y axes'   )
            B5 = widgets.Button(style=self.PARAMS['style'],description='Cycles'     )
            B6 = widgets.Button(style=self.PARAMS['style'],description='Repartition')
            B7 = widgets.Button(style=self.PARAMS['style'],description='Sankey'     );B7.on_click(B7e)  


        return widgets.VBox([B1,widgets.HBox([B2,B22,B21]),
                                widgets.HBox([B3,B4,B5,B6,B7]),
                                Outplot]) 

    def get_supp(self):
        outrun = widgets.Output()    
        with outrun:
            print('HELLO')
            display(self.hub.get_supplements(returnas=True))
        return(widgets.VBox([outrun]))
    #########################################################################
    #                      INTERFACE TO RULE THEM ALL  
    # #######################################################################
    def __init__(self,hub=None):
        #### INITIAL PARAMETER DICTIONNARY
        self.PARAMS = {}
        self.PARAMS['style']      = {'description_width': 'initial'}
        self.PARAMS['Categories'] = ['eqtype','source_exp','definition','com','group','units','symbol','isneeded']
        self.PARAMS['AllModels'] = get_available_models(hide_underscore=False,Return=dict)
        self.PARAMS['FULL']      = get_available_models(FULL=True,hide_underscore=False)
        with open(path+'\\README.md', 'r') as fh: self.PARAMS['tutorial'] = fh.read()
        with open(path+'\\Tutorial-model.md', 'r') as fh: self.PARAMS['tutorialmodel'] = fh.read()        

        
        #### MODEL LOADING
        if type(hub)!= type(Hub):
            self.hub=Hub('__TEMPLATE__',verb=False)
        else:
            self.hub=hub
                 
        #### PSEUDODECORATOR
        OUT = widgets.Output()     
        def clear_output_decorator(func):
            def wrapper(*args, **kwargs):
                with OUT:
                    OUT.clear_output()
                    func(*args, **kwargs)
            return wrapper

        #### ALL THE MAIN WIDGETS 
        @clear_output_decorator
        def pgm_event(obj): 
            display(Markdown('# Exploring CHIMES content and use'))
            display(self.get_Exploration0())
        
        @clear_output_decorator    
        def load_event(obj): 
            display(Markdown('# Loading model'))
            display(self.get_Loading())
            display(Markdown('# Network Representation'))
            display(self.get_network()) 
            
        @clear_output_decorator
        def a_event(obj): 
            display(Markdown('# Explore and Change values'))
            display(self.get_set())
            
        @clear_output_decorator
        def b_event(obj): 
            display(Markdown('# Run the simulation')); display(self.get_run())
            
        @clear_output_decorator
        def d_event(obj): 
            display(Markdown('# Plots')); display(self.get_plot())

        @clear_output_decorator
        def clear_event(obj):
            pass

        @clear_output_decorator
        def supp_event(obj): 
            display(Markdown('# Explore the supplements'))
            display(self.get_supp())
        Bnames = {
            'CHIMES'  : {
                    'function':pgm_event,
                    'tooltip': 'To learn about the content of the library',
                    },
            'Model' : {
                    'function':load_event,
                    'tooltip': 'To learn more about a model',
                    }, 
            'Values'  : {
                    'function':a_event,
                    'tooltip': 'See and change values in a model',
                    },
            'Supplements' : {
                    'function':supp_event,
                    'tooltip': 'Model-based material',
                    },
            'Run'     : {
                    'function':b_event,
                    'tooltip': 'Do the temporal resolution',
                    },
            'Plot'    : {
                    'function':d_event,
                    'tooltip': 'All plots available',
                    },
            'Clear': {
                    'function':clear_event,
                    'tooltip':'Clear the interface'
                  }
        }
        
        #### Apply the widgets
        Buttons = {b : widgets.Button(description=b,
                                      style=self.PARAMS['style'],
                                      button_style='primary') for b in Bnames.keys() }
        for b in Bnames.keys(): Buttons[b].on_click( Bnames[b]['function'])    
        display(widgets.VBox([widgets.HBox(list(Buttons.values())),
                            OUT]))