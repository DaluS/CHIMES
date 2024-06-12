
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

Developed initially as an internal tool for the Environmental Justice Program (EJP) at Georgetown, CHIMES has evolved into an open-source numerical environment with a range of features:

- An ensemble of user-friendly methods to manipulate, run, explore, and save models and their simulations
- A model base containing macroeconomic, climate, agent-based, circuits, and partial differential equation models. Each model includes logic, presets, explanations, and examples.
- A field base (quantities relevant to describe the systems such as temperature, price and GDP) with definitions, symbols, and units that can be shared across models.
- A Database that contains the value of the real world related to models (WIP)
- A tensor-based resolution system with an RK4 solver, facilitating efficient parallel and complex structure modelling.
- An ensemble of `get` and `set` methods for understanding and modifying model conditions.
- Additional methods for sensitivity and stability analyses.
- Easy-to-access plots for visualizing model outputs.
- A methodology for coupling external models through an API.

  
The main difference with the standard dynamical system library are:
1. the operations are based on tensors (hence easy parallel run for sensitivity, multi-regions, multi-agents, multi-sector, multi-whatever)
2. it uses model files written in Python (easy to do operations on models, easy to share)
3. It comes with many practical tools to make your life easy!

## **<div align="center">[There is a wiki that tells you everything about the library here!](https://github.com/DaluS/CHIMES/wiki/Home)</div>**

![image](https://github.com/DaluS/CHIMES/assets/11523050/a37b3b8b-2e9e-46cc-8c0e-51746c3590f4)

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



