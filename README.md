
<p align="center">
  <img src="https://github.com/DaluS/CHIMES/assets/11523050/59cb2a80-107f-401c-95f4-c1e16933c086" alt="LOGO" width="600"/>
</p>

![image](https://img.shields.io/badge/Status-Beta-yellow)


![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![image](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![image](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)

[![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)](https://github.com/georgetown-ejp/CHIMES/pulse)
[![Coverage Status](https://coveralls.io/repos/github/SDXorg/pysd/badge.svg?branch=master)](https://coveralls.io/github/dalus/CHIMES?branch=devel)
[![Contributions](https://img.shields.io/badge/contributions-welcome-blue.svg)](https://pysd.readthedocs.io/en/latest/development/development_index.html)

# CHIMES

CHIMES is a user-friendly library to explore, prototype, analyze and couple dynamical models in python.
It is built for both beginners and advanced users and provides access to complex tensorial dynamics resolution if needed. 

CHIMES means **C**ore for **H**olisitic **I**ntertwined **M**odel for **E**nvironmental **S**implexity. 

It has been developed as a structure for the next generation of complexity-based integrated assessment models, but it can be used well beyond that.

The main difference with the standard library is that:
1. the operations are based on tensors (hence easy parallel run for sensitivity, multi-regions, multi-agents, multi-sector, multi-whatever)
2. it uses model files written in Python (easy to do operations on models, easy to share)
3. It comes with many practical tools to make your life easy!

[There is a wiki that tells you everything about the library here!](https://github.com/DaluS/CHIMES/wiki/Home)

![image](https://github.com/DaluS/CHIMES/assets/11523050/a37b3b8b-2e9e-46cc-8c0e-51746c3590f4)
*Some illustrations of CHIMES content*

## Short tutorial 

Always use `?` and `tab` (help and autocompletion) to know what is in each element. The methods often use the same `get`, `set`, and `calculate` conventions for method names.

```
import chimes as chm 
chm.get_available_model() # See all available models

#we assume you want to run the model 'MODEL' 
hub=chm.Hub('MODEL') # will load the model in a hub using the default values
hub.run() # will simulate 100 years on a 0.1 timestep
hub.plot() # will plot all the fields by their units
```

**To explore a model**
```
hub=chm.Hub('modelname')      # Load a model file from `get_available_models()`
hub=chm.load_saved('nameofthefile') # Load a previous hub from `get_available_saves()`
hub.get_Network()             # Create a causal network of the model logics
hub.get_summary()             # Tell you everything about the model 
R = hub.get_dfields()          # Give you access to all fields inside the hub
hub.get_presets()             # Give you all presets you can load
hub.get_supplements()         # Give you all the supplementary functions available
```

**To change values**
```
hub.set_fields(field=value) # Apply it before a run !
```

## Authors

* [**Paul Valcke**](https://github.com/DaluS) - *Initial project, architecture, models, toolboxes, matplotlib, core* -
* [**Didier Vezinet**](https://github.com/Didou09) - *Class set, initial structure* -
* [**Stephen Kent**](https://github.com/stephen-kent) - *Server structure, refractors, dashboard* -
* [**Weiye Zhu**](https://github.com/I-dontlikeit) - *Redivis-exiobase coupling* - 

See also the list of [contributors](https://github.com/georgetown-ejp/CHIMES/contributors) who participated in this project.



