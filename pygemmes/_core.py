# -*- coding: utf-8 -*-

# %% Importations ###########

# built-in
import copy


# Common
import numpy as np


# Library-specific
from ._config import _FROM_USER
from ._config import _DEFAULTSIZE
from ._config import _VERB
from ._utilities import _utils, _class_checks, _class_utility, _cn
from ._utilities import _class_set
from ._utilities import _Network
from ._utilities import _solvers, _saveload
from ._utilities import _comparesubarray
from ._plots._plots import _DPLOT



class Hub():
    """
    MOST IMPORTANT OBJECT FOR THE USER.
    given a model name, it will load it and get its logics, presets and associated values.
    It will :
        * identify what are the parameters, the state variables, the differential variables
        * find their associated properties (definition, units, values)
        * find an order of calculation

    You then access to fields value modification, the structure and properties in the model,
    simulation, plots, deeper analysis...

    INPUTS :
    * model : STRING containing the model name
    * from_user : BOOLEAN if you want to use your file (True) or the one provided in pygemmes (False)
    * preset : DICTIONNARY name of the preset in the actual dictionnary of preset
    * dpreset : DICTOFDICTOFDIC a dictionnary of preset one can use (see model creation)
    * verb : BOOLEAN True for print in terminal

    model files are named _model_<model-name>.py

    A number of pre-defined models are available from the library,
        see pgm.get_available_models() to get a list

    All pre-defined model files are copied into your $HOME/.pygemmes/
        folder so you can:
            - edit them to change some parameters
            - create new model files that will be accessible to pygemmes
    You can use them using `from_user=True'
    """

    def __init__(
        self,
        model,
        from_user=_FROM_USER,
        preset=None,
        dpresets=None,
        verb=_VERB,
    ):

        # Initialize the hub main dictionnaries ###############################
        # Contains miscellaneous, practical informations
        self.__dmisc = {'run': False,        # Has a run been done
                        'dmulti': {},        # Which variables has been imposed as multiple, and what size
                        'cycles': False,     # Has an analysis of cycles been done
                        'derivative': False, # Has an analysis of derivatives been done
                        }

        # Load model files ####################################################
        (
            self.__dmodel,  # Contains the model informations
            self.__dparam,  # Contains all the fields and their relative properties
            self.__dmisc['dfunc_order'], # Order of resolution
            self.__dargs,  # Pointer for each field and function values
        ) = _class_set.load_model(
            model,
            from_user=from_user,
            verb=verb,
        )



        # Actualize the shape ##############################################
        self.__dmisc['dmulti']['NxNr'] = (self.__dparam['nx']['value'],
                                          self.__dparam['nr']['value'])
        self.__dmisc['dmulti']['scalar']= []
        self.__dmisc['dmulti']['vector'] = []
        self.__dmisc['dmulti']['matrix'] = []
        for k,v in self.dparam.items():
            size = v.get('size',[_DEFAULTSIZE,_DEFAULTSIZE])
            if size== [_DEFAULTSIZE,_DEFAULTSIZE]:
                self.__dmisc['dmulti']['scalar'].append(k)
            elif size[1]==_DEFAULTSIZE:
                self.__dmisc['dmulti']['vector'].append(k)
            else:
                self.__dmisc['dmulti']['matrix'].append(k)
        if len(self.__dmisc['dmulti']['vector']+self.__dmisc['dmulti']['matrix']):
            self.dmisc['multisectoral'] = True
        else:
            self.dmisc['multisectoral'] = False

        # update from preset if relevant ######################################
        if dpresets is not None:
            self.set_dpreset(dpresets,verb=verb)
        if preset is not None:
            self.set_preset(preset, verb=verb)
        else:
            self.reset()

    # ##############################
    # %% Setting parameters
    # ##############################
    def set_dpreset(self,
                    input,
                    preset_name=None,
                    verb=_VERB):
        """
        change the dictionnary of presets that you can load directly
        The structure is the same as in model files !

        Input must be : a dictionnary with
         { name1 : {fields : {key1:values,
                              key1:values,} ,
                   com: 'Message',
                   plots : {'plotname1':[{kwargs1},{kwargs2}...],
                            'plotname2':[{kwargs1},{kwargs2}...]}
         },

         if preset_name is a name in this dpreset,
          then it loads the preset
        """

        if type(input)!=dict:
            return 'Type of the input is wrong !'
        for kk,vv in input.items():
            if type(vv)!=dict:
                return 'input must be a dict of dict !'
            for keys in ['fields','com','plots']:
                if keys not in vv.keys():
                    return f'{keys} missing from the preset {kk}'
            for keys2 in vv.keys():
                if keys2 not in ['fields','com','plots']:
                    print(f'{keys2} in {kk} is not a field taken into account')

        if verb:
            print('OVERRIDE presets in dpreset')
        self.__dmodel['presets']=input

        if preset_name:
            self.set_preset(preset_name)

    def set_preset(self,
                   input,verb=_VERB):
        '''
        will load the preset that is already defined in dpreset (either in the model file or user added with set_dpreset
        preset must be a string
        check get_summary to see which are available !
        '''
        if input not in self.__dmodel['presets'].keys():
            return f"{input} is not a valid preset name ! the preset name must be in {list(self.__dmodel['presets'].keys())}"
        else :
            self.__dmodel['preset']=input
            self.set_dparam(self,**self.__dmodel['presets'][input]['fields'])

    def set_dparam(self,key=None,value=None,verb=_VERB,**kwargs):
        """
        Your best friend to change the fields values or sizes in the system.
        It can change :
            * dimensions ( duration of the simulated tine 'Tmax',
                           duration of one timestep 'dt'
                           number of system in parrallel 'nx',
                           number of regions             'nr',
                           number of sectors in a multisector object _nameofthedimension...
                           )
            * values of parameters and initial conditions, either for all systems/regions/sector, either indexwise

        if you want to change only one field, you can do "set_dparam(key,values)"
        if you want to change multiple fields at once you can do "set_dparam(**dict)" with dict={key:values},
        the way to put multiple values or specific sector will be explained in 2)

        1) ### CHANGE DIMENSIONS ###################################
        if you change a dimension such as the number of region of the number of sector, you can either put :
        an integer (and the sector name will be their number)
        a list of sector name (the number of sector will be the length of the list
        hub.set_dparam('nr',['France','Germany','China']) will create 3 named regions
        hub.set_dparam('nr',54) will create 54 regions with their number as index

        if Nprod is the number of production sector :
        hub.set_dparam('Nprod',100)
        hub.set_dparam('Nprod',['Consumption','Capital','Mine','Energy','Food'])

        CAUTION : if some specific values at certain indexes has been put, you cannot change the dimensions.
        do all your dimensions changes before filling specific values.

        2) ### CHANGE FIELDS AND INITIAL CONDITIONS ##################
        if no axis is explicitely put, the value will be changed for all axes

        # CHANGES ON MONOSECTORAL FIELDS
        (example on alpha, but it could be on anything else
        hub.set_dparam('alpha',0) will put 0 for all the axes of alpha (parrallel, regions,multisector...)
        hub.set_dparam('alpha',[0.1,0.2]) will put 0.1 in the first parrallel system, 0.2 in the second
        hub.set_dparam('alpha',[['nr','France'],0.5]) will put 0.5 in all parrallel systems, for the region named "France"
        hub.set_dparam('alpha',[['nr','France'],['nx',1],0.5]) will put 0.5 in the parrallel 1, region "France"
        hub.set_dparam('alpha',[['nr',0],['nx',0,4],[0.5,0.2]]) region 0, value 0.5 in parrallel 0, 0.2 in parrallel 4
        hub.set_dparam('alpha',[['nr','France','USA'],['nx',1],0.5]) parrallel 1, 0.5 both in France and USA

        hub.set_dparam('alpha',{'nr':['France','USA'],
                                'nx':1,
                                'value':0.5}                         will do the same !
        (the system will reconstruct automatically this dictionnary by itself)

        # FOR VECTOR OR MATRICES, THE SYSTEM WILL AUTOMATICALLY RECOGNIZE THE FIRST ENTRIES
        if 'Z' is a multisectoral element as a vector of dimension 2
        hub.set_dparam('Z',[0,1]) will put [0,1] for all parrallel all regions
        hub.set_dparam('Z',[['nr',0],[0,1]) will put [0,1] for all parrallel in region 0
        hub.set_dparam('Z',[['nr',0,1],[0,1]) will put [0,1] for all parrallel in region 0 and 1
        hub.set_dparam('Z',[['nx',0],['nr',0,1],[0,1]) will put [0,1] for parrallel system 0, in region 0 and 1

        if 'M' is a matric of dimension 2,2
        hub.set_dparam('Z',[[0,1],[1,0]]) will put [[0,1],[1,0]] for all parrallel all regions
        hub.set_dparam('Z',np.eye(2)) will put [[1,0],[0,1]] for all parrallel all regions})
        hub.set_dparam(**{'MATRIX': {'first':['energy','capital'],
                                     'second':['mine','consumption'],
                                     'nr':0,
                                     'value':[0.5,0.22]}})
        hub.set_dparam(**{'MATRIX': [['energy','capital'],['mine','consumption'],['nr',0],[0.5,0.22]]})
        hub.set_dparam(**{'MATRIX': [['energy','capital'],['mine','consumption'],[0.5,0.22]]})
        hub.set_dparam(**{'MATRIX': [['energy','capital'],0.22]})

        YOU CAN PUT A LOT OF CHANGES AT ONCE :
        dictchange={
                'Tmax':40,
                'Nprod': ['Consumption','Capital'],
                'nx':10,
                'alpha':np.linspace(0,0.02,10),
                'n':0.025,
                'phinull':0.1
                }
        hub.set_dparam(**dictchange)
        """

        # Take minimal changes
        if (key and value):
            kwargs[key]=value

        #### DECOMPOSE INTO SIZE AND VALUES #######
        setofdimensions = set(['nr','nx','dt','Tmax']+list(self.get_dparam(eqtype=['size'])))
        diffparam = set(self.get_dparam(eqtype=['differential', None])) - set(['__ONE__','time']) - setofdimensions

        dimtochange = {}
        fieldtochange = {}
        wrongfields = []

        for kk, vv in kwargs.items():
            if kk in list(setofdimensions):
                dimtochange[kk]=vv
            elif kk in list(diffparam):
                fieldtochange[kk]=vv
            else :
                wrongfields.append(kk)

        if verb:
            print('')
            print('### Identified keys to be changed ###')
            print(f'   Dimensions : {list(dimtochange.keys())}')
            print(f'   Fields : {list(fieldtochange.keys())}')
            print(f'   Ignored :{wrongfields}')

        #### SEND IT TO THE PIPE ###################
        self._set_dimensions(verb,**dimtochange)
        self._set_fields(verb,**fieldtochange)

    def _set_dimensions(self,verb=_VERB,**kwargs):
        '''
        Change the dimensions of the system
        '''

        # we scan all fields that will need to have their values changed
        # Check if we can change value
        setofdimensions = set(['nr','nx','dt','Tini','Tmax']+list(self.get_dparam(eqtype=['size'])))
        diffparam = set(self.get_dparam(eqtype=['differential', None])) - set(['__ONE__','time']) - setofdimensions
        parametersandifferential = list(diffparam)
        for kk in parametersandifferential:

            V=self.__dparam[kk]
            dimname=['nx','nr']+V['size']
            direct = 'initial' if V.get('eqtype','') == 'differential' else 'value'
            ValidAxis= _comparesubarray(V[direct])

            for ii,axis in enumerate(ValidAxis):
                dim=dimname[ii]
                if dim in kwargs.keys() and not axis:
                    print(f'ISSUE : YOU CHANGE {dim} while {kk} has specific values on it')
                    break


        # Put the values of the axis in the system
        for kk, vv in kwargs.items():
            # If its on multisectoral, put the value
            if kk not in ['dt','nx','Tmax']:
                if type(vv) is list:
                    self.__dparam[kk]['value'] = len(vv)
                    self.__dparam[kk]['list'] = vv
                elif type(vv) in [float,int]:
                    self.__dparam[kk]['value'] = vv
                    self.__dparam[kk]['list'] = list(np.arange(vv))
                if verb:
                    print(f"Now {kk} has {self.__dparam[kk]['value']} sectors with names {self.__dparam[kk]['list']}")
            # Else, we just change values
            else:
                self.__dparam[kk]['value'] = vv

        self.__dparam=_class_set.set_shapes_values(self.__dparam,
                                                   self.__dmisc['dfunc_order'])
        self.__dargs=_class_set.get_dargs_by_reference(self.__dparam,
                                                       dfunc_order=self.__dmisc['dfunc_order'])

    def _set_fields(self,verb=_VERB, **kwargs):
        # Get list of variables that might need a reshape
        parametersandifferential =  list(set(self.get_dparam(eqtype=['differential', None]))
                          - set(['__ONE__', 'time'])
                          - set(['nr', 'nx', 'dt', 'Tini', 'Tmax'] + list(self.get_dparam(eqtype=['size']))))

        # Get where the value is located
        direct = {k: 'initial' if self.__dparam[k].get('eqtype', '') == 'differential'
                else 'value'
                  for k in parametersandifferential}
        dimname= {}
        for kk in parametersandifferential:
            L = ['nx', 'nr'] +self.__dparam[kk]['size']
            dimname[kk] = [  self.__dparam[k2]['value'] for k2 in L]

        #######################
        oldvalue = { k: self.__dparam[k][direct[k]] for k in parametersandifferential }
        newvalue= {}

        # Dissecate new value allocation
        for kk in parametersandifferential:
            if kk in kwargs.keys():
                ### DECOMPOSE THE TYPE OF VARIABLE
                v= kwargs[kk]
                OLDVAL= np.copy(self.__dparam[kk][direct[kk]])
                # THIS IS A LIST OF VALUE
                if type(v) in [np.ndarray]:
                    #print('nd')
                    #if len(np.shape(v))==1:
                    newvalue[kk]=self._change_line(kk,v)
                elif type(v) in [list]:
                    #print('list')
                    #print(v)
                    if np.prod([type(vv) in [float,int] for vv in v]):
                        newvalue[kk]=self._change_line(kk, v)
                    elif np.shape(v)==np.shape(self.__dparam[kk]['value'][0,0,:,:]):
                        newvalue[kk] = self._change_line(kk, v)
                    else :
                        # WHERE SHIT HIT THE FAN : WE DO THAT IN ANOTHER FUNCTION
                        newvalue[kk] = self.__deep_set_dparam(OLDVAL,[],dimname,v,kk)
                # IF IT IS JUST A VALUE
                else :
                    if verb:print(f'Identified {kk} as a value change on all axes')
                    newvalue[kk] = kwargs[kk]+0.
            else:
                newvalue[kk]=np.ravel(np.array(oldvalue[kk]))[0]

        for kk in parametersandifferential:
            self.__dparam[kk][direct[kk]]=newvalue[kk]


        ### REINTIIALIZE SHAPES AND DIMENSIONS
        self.__dparam=_class_set.set_shapes_values(self.__dparam,
                                                   self.__dmisc['dfunc_order'])
        self.__dargs=_class_set.get_dargs_by_reference(self.__dparam,
                                                       dfunc_order=self.__dmisc['dfunc_order'])
        self.reset()

    def _change_line(self,kk,v):
        if self.__dparam[kk]['size'][0] == '__ONE__':
            print(f'Identified {kk} as value changes on nx (list)')
            newv = np.array(v)
            while len(np.shape(newv)) < 4:
                newv = newv[:, np.newaxis] + 0
        elif self.__dparam[kk]['size'][1] == '__ONE__':
            print(f'Identified {kk} as value changes on first vector dimension')
            newv=np.array(v)
            newv=newv[np.newaxis,np.newaxis,:,np.newaxis]+0
        else:
            print(f'Identified {kk} as value changes on the matrix')
            newv=np.array(v)
            print(newv,np.shape(newv))
            newv=newv[np.newaxis,np.newaxis,:,:]+0
        return newv

    def __deep_set_dparam(self, OLDVAL, FLATTABLE, dimname, inpt,name):
        '''
        If you are here, I am sorry. That will be messy.
        This is what happens when we ask a non-trivial construction of variable value

        :param OLDVAL:    What was loaded in the system before you change the value
        :param FLATTABLE: What dimensions contains nothing and thus can be broadcasted
        :param dimname:   The names and value of each dimensions
        :param v:         The new variables that we try to eat !
        :return:          A vector of the right dimensions, with only the correct values changes
        '''

        #######################################################
        ### Complete the needed informations ##################
        '''
        # AT THE END WE WANT : 
        { 'Nr': array of values,
          'Nx': array of values, 
          'values' : NP nan construction, with value changes}
        if personal dimensions exists, then added  
        '''

        fullinfos = {}
        #################################
        # if it's a dict, it is easier to translate
        if type(inpt) is dict:
            for k, v in inpt.dict():
                fullinfos[k] = v
        #################################
        # if it's a list, we decompose it
        elif type(inpt) is list:
            if name in self.dmisc['dmulti']['scalar']:
                #print(f'field {name} identified as a scalar!')
                fullinfos= self.__decompose_scalist(fullinfos,inpt)
            elif name in self.dmisc['dmulti']['vector']:
                #print(f'field {name} identified as a vector!')

                # check if the first elements are indexes for sector
                if type(inpt[0]) is list: # Check if its a list of sector
                    fullinfos['first']= inpt[0]
                    fullinfos = self.__decompose_scalist(fullinfos, inpt[1:])
                elif inpt[0] in self.__dparam[self.__dparam[name]['size']]['list']: # Check if it's a sector name
                    fullinfos['first'] = [inpt[0]]
                    fullinfos = self.__decompose_scalist(fullinfos, inpt[1:])
                else: # If nothing detected, treated as any other axis
                    fullinfos = self.__decompose_scalist(fullinfos, inpt)

            elif name in self.dmisc['dmulti']['matrix']:
                # FIRST AXIS
                Found0,Found1 = False,False
                if (type(inpt[0]) is list and len(inpt)>1): # Check if its a list of sector
                    fullinfos['first']= inpt[0]
                    Found0=True
                elif inpt[0] in self.__dparam[self.__dparam[name]['size']]['list']: # Check if it's a sector name
                    fullinfos['first'] = [inpt[0]]
                    Found0 = True
                if (Found0 and len(inpt )>2):
                    if type(inpt[1]) is list: # Check if its a list of sector
                        fullinfos['second']= inpt[1]
                        Found1=True
                    elif inpt[1] in self.__dparam[self.__dparam[name]['size']]['list']: # Check if it's a sector name
                        fullinfos['second'] = [inpt[1]]
                        Found1=True
                if not Found0 : fullinfos = self.__decompose_scalist(fullinfos, inpt[2:])
                if (Found0 and not Found1) : fullinfos = self.__decompose_scalist(fullinfos, inpt[1:])
                if Found1 : fullinfos = self.__decompose_scalist(fullinfos, inpt[2:])
        else :
            raise Exception(f'We have no idea what category of size {name} is')


        # Transform region name into numbers #
        for k in fullinfos.keys(): # For each axis
            if k not in ['value','first','second']:
                for ii,r in enumerate(fullinfos[k]):  # for each element
                    if type(r) is str :
                        fullinfos[k][ii]= self.__dparam[k]['list'].index(r)
            elif k in ['first','second']:
                for ii,r in enumerate(fullinfos[k]):  # for each element
                    if type(r) is str :
                        ax = self.__dparam[name]['size'][0 if k =='first' else 1]
                        fullinfos[k][ii]= self.__dparam[ax]['list'].index(r)

        if not bool(np.shape(fullinfos['value'])):
            fullinfos['value']=[fullinfos['value']]
        fullinfos['value']=np.array(fullinfos['value'])


        newval=np.copy(OLDVAL).astype(np.float)
        # transform scalar keys into non-scalar if needed
        lens = [int(np.prod(np.shape(v))) for k,v in fullinfos.items()]
        check= [ v!=np.amax(lens) for v in lens if v!=1]
        if np.sum(check): # If there are multiple sizes
            raise Exception(f'INCONSISTENCY IN {name} dimensions !')
        else :
            lmax = np.amax(lens)
            for ii in range(lmax):

                minidict = {k: v[min(ii,len(v)-1)] if int(np.prod(np.shape(v)))>=1
                      else v  for k,v in fullinfos.items()}


                # Complete the regions ###############
                dimx=['nx','nr']
                for idx in dimx:
                    if idx not in minidict.keys():
                        minidict[idx]=np.arange(self.__dparam[idx]['value'])
                dimx=['first', 'second']
                for ii,idx in enumerate(dimx):
                    if idx not in minidict.keys():
                        minidict[idx]=np.arange(self.__dparam[self.__dparam[name]['size'][ii]]['value'])[:]

                # Inject the value ####################
                newval[ minidict['nx'],
                        minidict['nr'],
                        minidict['first'],
                        minidict['second']] = minidict['value']


        return newval

    def __decompose_scalist(self,fullinfos,inpt):
        # it is simply the axis of decomposition
        if len(inpt) == 1 :
            pass
        elif len(inpt) == 2:
            #print('input is size 2')
            if type(inpt[0]) is str:
                #print('axis found')
                fullinfos[inpt[0]] = np.arange(len(inpt[-1]))
            else:
                #print('coefficients found')
                fullinfos[inpt[0][0]] = inpt[0][1:]
        elif len(inpt) > 2:
            #print('Long list !')
            for subl in inpt[:-1]:
                if type(subl) is str:
                    #print('axis found')
                    fullinfos[subl] = np.arange(len(inpt[-1]))
                else:
                    #print('coefficients found')
                    fullinfos[subl[0]] = subl[1:]
        else:
            print('The system do not understand your input')
        fullinfos['value'] = inpt[-1]
        return fullinfos

    # ##############################
    # %% Getting parameters ########
    # ##############################

    def get_dparam(self, condition=None,returnas=dict,verb=False, **kwdargs):
       """ Return a copy of the input parameters dict that you can filter
       lcrit = ['key', 'dimension', 'units', 'type', 'group', 'eqtype','isneeded']
       """
       lcrit = ['key', 'dimension', 'units',
                'type', 'group', 'eqtype', 'isneeded']

       return _class_utility._get_dict_subset(
           indict=self.__dparam,
           verb=False,
           returnas=dict,
           lcrit=lcrit,
           lprint=[],
           condition=condition,
           **kwdargs,
       )

    def get_dparam_as_reverse_dict(
       self,
       crit=None,
       returnas=None,
       verb=None,
       **kwdargs,
    ):
       """ Return/prints a dict of units/eqtype... with a list of keys

       if crit = 'units', return a dict with:
           - keys: the unique possible values of field 'units'
           - values: for each unique unit, the corresponding list of keys

       lcrit = ['dimension', 'units', 'type', 'group', 'eqtype']

       Restrictions on the selection can be imposed by **kwdargs
       The selection is done using self.get_dparam() (single-sourced)
       """

       # -------------
       # check input

       if verb is None:
           verb = False
       if returnas is None:
           returnas = dict if verb is False else False

       lcrit = ['dimension', 'units', 'type', 'group', 'eqtype']
       if crit not in lcrit:
           msg = (
               f"Arg crit must be in: {lcrit}\n"
               f"Provided: {crit}"
           )
           raise Exception(msg)

       if crit in kwdargs.keys():
           msg = (
               "Conflict detected!:\n"
               f"{crit} is the sorting criterion => not usable for selection!"
           )
           raise Exception(msg)

       # -------------
       # create dict

       lunique = set([v0.get(crit) for v0 in self.__dparam.values()])
       dout = {
           k0: self.get_dparam(returnas=list, **{crit: k0, **kwdargs})
           for k0 in lunique
       }

       # -------------
       # print and/or return

       if verb is True:
           lstr = [f'\t- {k0}: {v0}' for k0, v0 in dout.items()]
           msg = (
               "The following selection has been identified:\n"
               + "\n".join(lstr)
           )
           print(msg)

       if returnas is dict:
           return dout


    # ##############################
    # %% Read-only properties
    # ##############################
    @property
    def dfunc_order(self):
       """ The ordered list of intermediary function names """
       return self.__dmisc['dfunc_order']

    @property
    def dmodel(self):
       """ The model identifiers """
       return self.__dmodel

    @property
    def dargs(self):
       return self.__dargs

    @property
    def dparam(self):
       return self.get_dparam(returnas=dict, verb=False)

    @property
    def dmisc(self):
       return self.__dmisc


    # ##############################
    # reset
    # ##############################

   # ##############################
   # run simulation
   # ##############################
    def reset(self):
       """ Re-initializes all variables

       Only the first time step (initial values) is preserved
       All other time steps are set to nan
       """
       # reset ode variables
       for k0 in self.get_dparam(eqtype=['differential', 'statevar'], returnas=list):
           self.__dparam[k0]['value'][...] = np.nan

       # Reset initial for ode
       for k0 in self.get_dparam(eqtype=['differential'], returnas=list):
           self.__dparam[k0]['value'][0, ...] = self.__dparam[k0]['initial']
       self.__dparam['time']['value'][0,...] = self.__dparam['Tini']['value']

       # recompute initial value for function-parameters
       pstate = self.__dmisc['dfunc_order']['parameter']
       for k0 in pstate:
           dargs = {
               k1: self.__dparam[k1]['value']
               for k1 in self.__dparam[k0]['args'][None]
           }
           dargs.update({
               k1: self.__dparam[k1]['value']
               for k1 in self.__dparam[k0]['args']['parameter']
           })
           self.__dparam[k0]['value'] = self.__dparam[k0]['func'](**dargs)

       # recompute inital value for statevar
       lstate = self.__dmisc['dfunc_order']['statevar']

       for k0 in lstate:
           kwdargs = {
               k1: v1[0, ...] if k1 in self.__dmisc['dfunc_order']['statevar'] +
                                       self.__dmisc['dfunc_order']['differential'] else v1
               for k1, v1 in self.__dargs[k0].items()
           }

           # run function
           self.__dparam[k0]['value'][0, ...] = (
               self.__dparam[k0]['func'](**kwdargs)
           )

       # set run to False
       self.__dmisc['run'] = False

    def run(
           self,
           N=False,
           verb=None,
    ):
       """ Run the simulation, with any of the solver existing in :
           - pgm.get_available_solvers(returnas=list)
           Verb will have the following behavior :
           - none no print of the step
           - 1 at every step
           - any float (like 1.1) the iteration is written at any of these value

       if you define N, the system will reinterpolate the temporal values on N samples
       typically, N=Tmax will put 1 value per year

       Compute each time step from the previous one using:
           - parameters
           - differentials (ode)
           - intermediary functions in specified func_order
       """
       if (_VERB == True and verb is None):
           verb = 1.1

       # check inputs
       dverb = _class_checks._run_verb_check(verb=verb)

       # reset variables
       self.reset()

       # start time loop
       try:
           solver = _solvers.solve(
               dparam=self.__dparam,
               dmisc=self.__dmisc,
               dargs=self.__dargs,
               dverb=dverb,
           )
           self.__dmisc['run'] = True
           self.__dmisc['solver'] = solver
           if N:
            self.reinterpolate_dparam(N)

       except Exception as err:
           self.__dmisc['run'] = False
           raise err

    def reinterpolate_dparam(self, N=100):
       """
       If the system has run, takes dparam and reinterpolate all values.
       Typical use is to have lighter plots

       DO NOT WORK WELL WITH GRID
       NEED A RESET BEFORE A RUN TO REALLOCATE SPACE

       Parameters
       ----------
       Npoints : TYPE, optional
           DESCRIPTION. The default is 100.

        'reinterpolate_dparam IS DEPRECIATED, WILL BE ADAPTED TO MULTISECTORIALITY SOON'
       """
       P = self.__dparam
       t = P['time']['value']
       for k in self.__dmisc['dfunc_order']['statevar']+self.__dmisc['dfunc_order']['differential']:
           v = P[k]['value']
           prevshape= np.shape(v)
           v2 =v.reshape(P['nt']['value'],-1)
           #print(np.shape(v2))
           newval = np.zeros([N,np.shape(v2)[1]])
           newt = np.linspace(t[0,0,0,0], t[-1,0,0,0], N)
           for i in range(np.shape(newval)[1]):
               newval[:, i] = np.interp(newt[:,0], t[:, 0,0,0,0], v2[:, i])
           newshape =[N]+list(prevshape[1:])
           self.__dparam[k]['value'] = newval.reshape(newshape)

    # ##############################
    #  Introspection
    # ##############################
    def __repr__(self, verb=None):
       """ This is automatically called when only the instance is entered """

       if verb is None:
           verb = True

       col0 = [
           'model',
           'preset',
           'param (fix + func)',
           'differential',
           'statevar',
           'run',
           'source',
       ]

       ar0 = [
           self.__dmodel['name'],
           self.__dmodel['preset'],
           '{} + {}'.format(
               len(self.get_dparam(returnas=list, eqtype=None))-1,
               len(self.get_dparam(returnas=list, eqtype='parameter'))-1,
           ),
           len(self.get_dparam(returnas=list, eqtype='differential'))-1,
           len(self.get_dparam(returnas=list, eqtype='statevar')),
           self.__dmisc['run'],
           self.__dmodel['file'],
       ]
       if verb is True:
           return _utils._get_summary(
               lar=[ar0],
               lcol=[col0],
               verb=False,
               returnas=str,
           )
       else:
           return col0, ar0

    def get_summary(self, idx=0, Region=0):
        """
        INTROSPECTION TOOL :
        Print a str summary of the model, with
        * Model description
        * Parameters, their properties and their values
        * ODE, their properties and their values
        * Statevar, their properties and their values

        For more precise elements, you can do introspection using hub.get_dparam()

        INPUT :
        * idx = index of the model you want the value to be shown when there are multiple models in parrallel
        * region : name or index of the region you want to plot
        """

        _FLAGS = ['run', 'cycles', 'derivative','multisectoral','solver']
        _ORDERS = ['statevar', 'differential', 'parameters']

        Vals = self.__dparam

        print(60 * '#')
        print(20 * '#', 'SUMMARY'.center(18), 20 * '#')
        print(60 * '#')
        print('Model       :', self.dmodel['name'])
        print(self.dmodel['description'])
        print('File        :', self.dmodel['file'])

        print(20 * '#', 'Fields'.center(18), 20 * '#')
        for o in _ORDERS:
           print(o.ljust(15), str(len(self.dmisc['dfunc_order'][o])).zfill(3),
                 [z for z in self.dmisc['dfunc_order'][o] if z not in ['t','__ONE__','Tmax','Tini','dt','nt','nr','nx']])

        print(20 * '#', 'Presets'.center(18), 20 * '#')
        for k, v in self.dmodel['presets'].items():
           print('    ', k.center(18),':', v['com'])

        print(20 * '#', 'Flags'.center(18), 20 * '#')
        for f in _FLAGS:
           print(f.ljust(15) + ':', self.dmisc.get(f,''))

        print(20 * '#', 'Time vector'.center(18), 20 * '#')
        for k,v in Vals.items():
           if k in ['Tmax','Tini','dt','nt']:
               print(f"{k.ljust(20)}{str(v['value']).ljust(20)}{v['definition']}")

        print(20 * '#', 'Dimensions'.center(18), 20 * '#')
        sub= self.get_dparam(returnas=dict,eqtype=['size'],)
        for k in list(sub.keys())+['nx','nr']:
           v = Vals[k]
           print(f"{k.ljust(20)}{str(v['value']).ljust(20)}{v['definition']}")

        print('\n')
        print(60 * '#')
        print(20 * '#', 'fields'.center(18), 20 * '#')
        if self.__dparam['nr']['value']!=1:
            print(20 * '#', str('Region :'+str(self.__dparam['nr']['list'][Region])).center(18), 20 * '#')
        if self.__dparam['nx']['value'] != 1:
            print(20 * '#', str('Parr. sys numb:'+str(self.__dparam['nx'].get('list',np.arange(self.__dparam['nx']['value']))[idx])).center(18), 20 * '#')
        print(60 * '#')
        # parameters
        col2, ar2 = _class_utility._get_summary_parameters(self, idx=idx)
        # SCALAR ODE
        col3, ar3 = _class_utility._get_summary_functions_vector(
           self, idx=idx,Region=Region, eqtype=['differential'])
        # SCALAR Statevar
        col4, ar4 = _class_utility._get_summary_functions_vector(
           self, idx=idx,Region=Region, eqtype=['statevar'])



        # ----------
        # format output
        _utils._get_summary(
           lar =[ ar2,  ar3,  ar4 ],
           lcol=[ col2, col3, col4],
           verb=True,
           returnas=False,)

        # Print matrices
        _class_utility._print_matrix(self,idx=idx,Region=Region)

    def get_equations_description(self):
        '''
        Gives a full description of the model and its equations, closer to what one
        would expect in an article.
        get_Network to get the interactive version
        '''

        print('############# DIFFERENTIAL EQUATIONS ###########')
        for key in self.__dmisc['dfunc_order']['differential']:
            v = self.dparam[key]
            print('### ', key, ' ###########')
            print('Units        :', v['units'])
            print('Equation     :', f'd{key}/dt=', v['source_exp'])
            print('definition   :', v['definition'])
            print('units        :', v['units'])
            print('Comment      :', v['com'])
            print('Dependencies :')
            for key2 in v['kargs'] :
                v1 = self.dparam[key2]
                print('    ', key2, (8-len(key2))*' ',
                      v1['units'], (8-len(v1['units']))*' ', v1['definition'])
            print(' ')
        print('######### STATE VARIABLES EQUATIONS ###########')
        for key in self.__dmisc['dfunc_order']['statevar']:
            v = self.dparam[key]
            print('### ', key, ' ###########')
            print('Units        :', v['units'])
            print('Equation     :', f'{key}=', v['source_exp'])
            print('definition   :', v['definition'])
            print('Comment      :', v['com'])
            print('Dependencies :')
            for key2 in v['kargs'] :
                v1 = self.dparam[key2]
                print('    ', key2, (8-len(key2))*' ',
                      v1['units'], (8-len(v1['units']))*' ', v1['definition'])
            print(' ')
            print(' ')

    def get_Network(self,
                    filters=(),
                    auxilliary=False,
                    redirect=False,
                    screensize=1080,
                    custom=True,
                    params=False):
        """
        Create an interative network showing how fields are related as a
        causality network.
        filters : select what you want or not to see.
                    if [] contains only what will be shown
                    if () contains what will NOT be shown
        auxilliary : if False, remove variables that are not necessary for a run
        redirect : removed variable will transfer their dependency to the one they are linked to
        """
        _Network.Network_pyvis(self,
                               filters=filters,
                               redirect=redirect,
                               auxilliary=auxilliary,
                               screensize=screensize,
                               custom=custom,
                               plot_params=params)


    # ##############################
    #       plotting methods
    # ##############################

    def plot_preset(self, preset=None):
        '''
        Automatically plot all functions that are defined in _plot.py, associated with the preset

        If a preset is loaded, you do not need to precise it when using the function
        If no preset is loaded, you can try to plot its associated plots by calling it.
        '''

        if preset is None:
            preset = self.dmodel['preset']
        tempd = self.dmodel['presets'][preset]['plots']

        for plot, funcplot in _DPLOT.items():
            for argl in tempd.get(plot, []):
                funcplot(self, **argl)

    def plot(self,
             filters_key =(),
             filters_units=(),
             filters_sector=(),
             separate_variables={},
             idx=0,
             Region=0,
             title='',
             lw=2):
            '''
generate one subfigure per set of units existing.

There are three layers of filters, each of them has the same logic :
if the filter is a tuple () it exclude the elements inside,
if the filter is a list [] it includes the elements inside.

Filters are the following :
filters_units      : select the units you want
filters_sector     : select the sector you want  ( '' is all monosetorial variables)
filters_sector     : you can put sector names if you want them or not. '' corespond to all monosectoral variables
separate_variables : key is a unit (y , y^{-1}... and value are keys from that units that will be shown on another graph,

Region             : is, if there a multiple regions, the one you want to plot
idx                : is the same for parrallel systems
'''

            _DPLOT['byunits'](self,
                             filters_key,
                             filters_units,
                             filters_sector,
                             separate_variables,
                             lw,
                             idx ,
                             Region ,
                             title ,
                              )

    # ##############################
    #       Deep analysis methods
    # ##############################
    def calculate_Cycles(self, ref=None, n=10):
        '''
        This function is a wrap-up on GetCycle to do it on all variables.

        For each variables, it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself

        n : int, number of harmonics calculated in fourier decomposition
        '''

        leq = ['differential', 'statevar']
        fields = ['reference',
                  'period_indexes',
                  'period_T_intervals',
                  't_mean_cycle',
                  'period_T',
                  'meanval',
                  'medval',
                  'stdval',
                  'minval',
                  'maxval']


        for var, dic1 in self.get_dparam(returnas=dict, eqtype=leq).items():
            tempval = np.reshape(dic1['value'],(np.shape(dic1['value'])[0],-1))
            self.__dparam[var]['cycles'] = [{k: []
                                             for k in fields} for i in range(np.shape(tempval)[1])]
        for var, dic1 in self.get_dparam(returnas=dict, eqtype=leq).items():
            tempval = np.reshape(dic1['value'], (np.shape(dic1['value'])[0], -1))
            for idx in range(np.shape(tempval)[1]):
                if ref is None:
                    self.__dparam[var]['cycles'][idx]['reference'] = var
                    self._FillCycles(var,tempval[:,idx], var, idx, n=n)
                else:
                    self.__dparam[var]['cycles'][idx]['reference'] = ref
                    self._FillCycles(var,tempval[:,idx], ref, idx, n=n)
        self.reverse_cycles_dic()
        self.__dmisc['cycles'] = True

    def _FillCycles(self, var,tempval, ref='employment', id=0, n=10):
        '''
        it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself

        var : name of the variable we are working on
        ref : reference for the oscillations detections
        '''

        # Get the new dictionnary to edit
        dic = self.__dparam[var]
        dic1 = self.__dparam[var]['cycles'][id]

        # check if reference has already calculated its period
        # the reference has cycle and this cycle has been calculated on itself
        ready = False
        if 'cycles' in self.__dparam[ref].keys():
            dic2 = self.__dparam[ref]['cycles'][id]
            if (dic2['reference'] == ref and len(dic2.get('period_indexes',[]))>=1):
                # We can take the reference as the base
                ready = True
        # If there is no good reference
        # We calculate it and put
        if not ready:
            self._findCycles(ref, tempval,id)
            dic2 = self.__dparam[ref]['cycles'][id]

        for key in ['period_indexes', 'period_T_intervals',
                    't_mean_cycle', 'period_T']:
            dic1[key] = copy.deepcopy(dic2[key])

        tim = self.__dparam['time']['value'][:,0,0,0]
        dic1['period_T_intervals'] = [[tim[idx[0], 0], tim[idx[1], 0]]
                                      for idx in dic1['period_indexes']]
        dic1['t_mean_cycle'] = [
            (t[0] + t[1]) / 2 for t in dic1['period_T_intervals']]
        dic1['period_T'] = [
            (t[1] - t[0]) for t in dic1['period_T_intervals']]
        dic1['frequency'] = [
            1/(t[1] - t[0]) for t in dic1['period_T_intervals']]

        # Fill for each the characteristics
        values = tempval
        # print(var, dic1)
        dic1['meanval'] = [np.mean(values[idx[0]:idx[1]])
                           for idx in dic1['period_indexes']]
        dic1['medval'] = [np.median(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]
        dic1['stdval'] = [np.std(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]
        dic1['minval'] = [np.amin(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]
        dic1['maxval'] = [np.amax(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]

        # print([values[idx[0]:idx[1]] for idx in dic1['period_indexes']])

        Coeffs = [_cn(values[idx[0]:idx[1]], n)
                  for idx in dic1['period_indexes']]
        dic1['Coeffs'] = [Coeffs[i][1:]/Coeffs[i][1]
                          for i in range(len(Coeffs))]
        dic1['Harmonicity'] = [np.sum(Coeffs[i][1:]**2)/np.sum(Coeffs[i]**2)
                               for i in range(len(Coeffs))]

    def _findCycles(self, refval,tempval, idx=0):
        '''
        Detect all positions of local maximums and the time that is linked
        '''
        # initialisation
        periods = []
        id1 = 1

        dic1 = self.__dparam[refval]['cycles'][idx]
        val = tempval

        # identification loop
        while id1 < len(val) - 2:
            if (val[id1] > val[id1 - 1] and
                    val[id1] > val[id1 + 1]):
                if np.abs(val[id1]-val[id1-1]):
                    periods.append(1 * id1)
            id1 += 1

        # Fill the formalism
        self.__dparam[refval]['cycles'][idx]['period_indexes'] = [
            [periods[i], periods[i + 1]] for i in range(len(periods) - 1)
        ]
        tim = self.__dparam['time']['value']
        dic1 = self.__dparam[refval]['cycles'][idx]
        dic1['period_T_intervals'] = [[tim[idx[0]], tim[idx[1]]]
                                      for idx in dic1['period_indexes']]
        dic1['t_mean_cycle'] = [
            (t[0] + t[1]) / 2 for t in dic1['period_T_intervals']]
        dic1['period_T'] = [
            (t[1] - t[0]) for t in dic1['period_T_intervals']]
        dic1['reference'] = refval

    def reverse_cycles_dic(self):
        leq = ['differential', 'statevar']
        for var, dic1 in self.get_dparam(returnas=dict, eqtype=leq).items():
            c = dic1['cycles']
            newcycles = {k: [] for k in c[0].keys()}
            for i in range(len(c)):
                for k in c[i].keys():
                    newcycles[k].append(c[i][k])

            self.__dparam[var]['cycles_bykey'] = copy.deepcopy(newcycles)


    def calculate_StatSensitivity(self):
        '''
        When there are multiple run in parrallel, will associate to each variable
        a dict 'sensibility' in dparam, with statistical measures

        Do not use with grid=True
        '''
        leq = ['differential', 'statevar']
        R0= self.get_dparam()
        R = self.get_dparam(returnas=dict, eqtype=leq)

        for ke in R.keys():
            self.__dparam[ke]['sensitivity'] = []
            for kr in range(R0['nr']['value']):
                d={}
                for ii,kx in enumerate(R0[R0[ke]['size'][0]].get('list',[0])):
                    val = R[ke]['value'][:,:,kr,ii,0]
                    d[kx]={
                    'mean': np.mean(val, axis=1),
                    'stdv': np.std(val, axis=1),
                    'min' : np.amin(val, axis=1),
                    'max' :np.amax(val, axis=1),
                    'median': np.median(val, axis=1)}
                self.__dparam[ke]['sensitivity'].append(d)
        self.__dmisc['sensitivity'] = True

    def calculate_ConvergeRate(self, finalpoint,Region=0,idx=0):
        '''
        Will calculate how the evolution of the distance of each trajectory to
        the final point.
        Then, it fit the trajectory with an exponential, and return the rate
        of decrease of this exponential (the bigger the more stable).

        finalpoint has to be :
            { 'field1' : number1,
              'field2' : ['sectorname',number2],
              'field3' : number3}
        '''
        # Final step studies ##################
        R = self.get_dparam(
            key=[k for k in finalpoint]+['time'], returnas=dict)

        # Take into account multisectoriality
        sector={k:0 for k in finalpoint.keys()}
        for k,v in finalpoint.items():
            if type(v) is list :
                sector[k]=v[1]
                finalpoint[k]=v[0]

        Coords = [R[k]['value'][idx,Region,sector[k],0]-finalpoint[k] for k in finalpoint.keys()]
        dist = np.linalg.norm(Coords, axis=0)
        t = R['time']['value'][:, 0]

        # Fit using an exponential ############
        Nsys = self.dmisc['dmulti']['shape'][0]
        ConvergeRate = np.zeros(Nsys)
        for i in range(Nsys):
            if (np.isnan(np.sum(dist[:, i])) or np.isinf(np.sum(dist[:, i]))):
                ConvergeRate[i] = -np.inf
            else:
                fit = np.polyfit(t,
                                 np.log(dist[:, i]),
                                 1,
                                 w=np.sqrt(dist[:, i]))
                ConvergeRate[i] = -fit[0]
        return ConvergeRate


    # ##############################
    #       data conversion
    # ##############################
    def Extract_preset(self, t=-1):
        '''
        Create a dictionnary, containing all fields value at the instant t.
        by default take the value at the latest instant
        you can save it and put it with set_dparam in a new run !
        '''

        ### Getting time vector
        T = self.get_dparam(key=['time'])
        vectime = T['time']['value'][:, 0, 0, 0]

        ### Extracting values
        if t != -1:
            idt = np.argmin(np.abs(vectime - t)) - 1
        else:
            idt = -1
        R = self.get_dparam(key=('time', '__ONE__'))

        presetdict = {}
        for k, v in R.items():
            type = v.get('eqtype', None)
            if type in ['differential']:
                presetdict[k] = v['value'][idt, :, :, :]*1.
            elif type in ['parameters', None]:
                presetdict[k] = v['value']
            elif type in ['size']:
                presetdict[k] = v.get('list', v['value'])
        return presetdict

    def _to_dict(self):
        """ Convert instance to dict """
        dout = {
            'dmodel': copy.deepcopy(self.__dmodel),
            'dparam': self.get_dparam(),
            'dmisc': copy.deepcopy(self.__dmisc),
            'dargs': copy.deepcopy(self.__dargs),
        }
        return dout

    @classmethod
    def _from_dict(cls, dout=None, model_file=None):
        """ Create an instance from a dict """

        # --------------
        # check inputs
        c0 = (
            isinstance(dout, dict)
            and sorted(dout.keys()) == ['dargs', 'dmisc', 'dmodel', 'dparam']
            and all([isinstance(dd, dict) for dd in dout.values()])
        )
        if not c0:
            msg = (
                "Arg dout must be a dict of the form:\n"
                "{'dargs': dict, 'dmisc': dict, 'dparams': dict}\n"
                f"You provided:\n{dout}"
            )
            raise Exception(msg)

        # -------------
        # rebuild all functions from source, if necessary
        c0 = any([
            v0.get('source_kargs') is not None
            and not hasattr(v0.get('func'), '__call__')
            for k0, v0 in dout['dparam'].items()
        ])
        if c0:
            _saveload.rebuild_func_from_source(dout, model_file=model_file)

        # -------------------
        # create instance
        obj = cls()
        obj.__dmodel = dict(dout['dmodel'])
        obj.__dparam = {k0: dict(v0) for k0, v0 in dout['dparam'].items()}
        obj.__dmisc = dict(dout['dmisc'])
        obj.__dargs = dict(dout['dargs'])

        # update default args for functions
        _class_checks._update_func_default_kwdargs(
            lfunc=obj.get_dparam(returnas=list, eqtype=(None,)),
            dparam=obj.__dparam,
            dmulti=obj.__dmisc['dmulti'],
        )

        # re-pass dargs by reference
        obj.__dargs = _class_checks.get_dargs_by_reference(
            obj.__dparam,
            dfunc_order=obj.__dmisc['dfunc_order'],
        )

        return obj

    def __calculate_variation_rate(self, epsilon=0.0001):
        '''
        INACTIVE IN THIS VERSION

        Calculate all derivatives :
            * time derivative
            * time log_derivative (variation rate)
            * partial_derivatives (gradient on the other variables)
            * partial_contribution (partial_derivatives time the respective time derivate)

        partial derivative is associating to field Y a dic as {X : dY/dX} for each statevar

        accessible in :
            dparam[key]['time_derivate']
            dparam[key]['time_log_derivate']
            dparam[key]['partial_derivatives']
            dparam[key]['partial_contribution']
        '''

        R = self.__dparam

        varlist = self.dmisc['dfunc_order']['statevar'] + \
                  self.dmisc['dfunc_order']['differential']

        varlist.remove('time')

        for k in varlist:
            R[k]['time_derivate'] = np.gradient(
                R[k]['value'], axis=0) / R['dt']['value']
            R[k]['time_log_derivate'] = R[k]['time_derivate'] / R[k]['value']

            if R[k]['eqtype'] == 'differential':
                R[k]['time_dderivate'] = np.gradient(
                    R[k]['time_derivate'], axis=0) / R['dt']['value']
            # SENSITIVITY CALCULATION
            func = R[k]['func']
            args = R[k]['args']['differential'] + R[k]['args']['statevar']
            if 'itself' in R[k]['kargs']:
                args += k

            argsV = {k2: R[k2]['value'] for k2 in args}

            if k in args:
                argsV['itself'] = argsV[k]
                del argsV[k]
                args += ['itself']
                args.remove(k)

            R[k]['partial_derivatives'] = {}
            for k2 in args:
                argTemp = copy.deepcopy(argsV)
                argTemp[k2] += epsilon
                R[k]['partial_derivatives'][k2] = (
                                                          func(**argTemp) - func(**argsV)) / epsilon

        # Contribution of partial derivatives
        for k in varlist:
            R[k]['partial_contribution'] = {k2: R[k]['partial_derivatives'][k2]
                                                * R[k2]['time_derivate']
                                            for k2 in R[k]['partial_derivatives'].keys()}
        self.__dmisc['derivative'] = True



    # ##############################
    #       saving methods
    # ##############################

    def save(self, path=None, name=None, fmt=None, verb=None, returnas=None):
        """ Save the instance

        Saved files are stored in path/fullname.ext
        The extension (ext) depends on the format (fmt) chosen for saving
        The file full name (fullname) is the concatenation of a base default
        name and a user-defined name.
            ex.: Output_MODELNAME_USERDEFINEDNAME.ext
        where MODELNAME is the model's name

        By default path is set to 'output/', but the user can overload it

        """

        return _saveload.save(
            self,
            path=path,
            name=name,
            fmt=fmt,
            verb=verb,
            returnas=returnas,
        )

    # ##############################
    #       replication methods
    # ##############################

    def copy(self):
        """ Return a copy of the instance """

        dout = self._to_dict()
        return self.__class__._from_dict(dout=dout)

    # ##############################
    #       comparison methods
    # ##############################

    def __eq__(
        self,
        other,
        atol=None,
        rtol=None,
        verb=None,
        return_dfail=None,    ):
        """ Automatically called when testing obj1 == obj2 """
        return _class_utility._equal(
            self, other,
            atol=atol,
            rtol=rtol,
            verb=verb,
            return_dfail=return_dfail)
