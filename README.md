
<p align="center">
  <img src="https://github.com/DaluS/CHIMES/assets/11523050/59cb2a80-107f-401c-95f4-c1e16933c086" alt="LOGO" width="600"/>
</p>

![image](https://img.shields.io/badge/State-Beta-orange)


![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![image](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![image](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)

# CHIMES



CHIMES is a library to explore, prototype, analyze and couple dynamical models in python.

CHIMES means **C**ore for **H**olisitic **I**ntertwined **M**odel for **E**nvironmental **S**implexity. 

It has been developped as a structure for the next generation of complexity-based integrated assesment model, but can be used well beyond that.

At the core is the idea that quantities (here called fields) can have a causal logic, a mathematical definitionm that defines its value or its variation. 
hose fields are going to create a causal map of intertwined relationships looping on each others. 
Studying such model is studying the dance between those quantities. 


CHIMES is its own numerical environment, open on other structures. It has:
* A modelbase with macreconomic, climate, agent-based, circuits, partial differential equation models that contains logics, preset, explanation and examples for each.  
* A field-base with values, definitions that can be used and shared between models
* A tensor-based resolution system with an RK4 solver, that allow efficient parrallel and complex structure modeling
* An ensemble of `get` and `set` method to understand a model and modify its conditions
* An ensemble of additional methods for sensitivity, stability analyses
* An ensemble of easy to access plots
* A methodology to couple external models through an API. 

![image](https://github.com/georgetown-ejp/CHIMES/assets/11523050/00cd06e1-0a8d-4f38-a74a-f1ee006f83af)
*Some illustrations of CHIMES content*

## TL:DR USE 

If you are not in a hurry, read the section "Exploring the content" rather than this 
 
**To load and run a model**
Always use `?` and `tab` (help and autocompletion) to know what is in each element. 

```
import chimes as chm 

#we assume you want to run the model 'MODEL' 
hub=chm.Hub('MODEL') # will load the model in a hub using the default values
hub.run() # will simulate 100 years on a 0.1 timestep
hub.plot() # will plot all the fields by their units
```

**A bit slower: to explore the library**
```
chm.get_available_models()
chm.get_available_fields()
chm.get_available_functions_library()
chm.get_available_operators()
chm.get_available_plots()
chm.get_available_saves()
chm.get_model_documentation('modelname')
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
hub.set_fields(field,value)


## Another dynamical system library? 

Many libraries of model simulations exists already. CHIMES architecture bring new elements that facilitate the 

The advantage of CHIMES over the other architectures are the following: 
* Models files are extremely flexible, can be very short for prototyping, as well as include external models coupling or intermediate calculations in their creation. 
* Model files are in interaction between each others if needed to structure easily complex models or insist on one modification. They find undefined informations for their field in a shared library 
* The structure is made to solve tensors for each field: it is easy to do distribution of parameter values, multiple regions, multiple agents dynamics at a low computational costs. 
* Multiple analysis toolboxes and plot are made specifically for the architecture making the contributions scaling easily
* Simulations are highly interactive allowing "user endogenisation" and gamification of models. 
* The library is fully open-source



## Installation
You need python `3.11` or above and we recommend an IDE that supports Jupyter Notebooks. We recommend [visual studio](https://code.visualstudio.com/docs/python/python-tutorial)

To install the library with pip, use `pip install --user chimes`

For manual installation: 
1. Clone the repository or manual download (in green on top-right of the github page, `Code`, `Download zip`)
2. Install the content of `requirements.txt` (using pip `pip install -r requirement.txt`)
3. Add to the path the python library in the begining of your code `import sys; sys.path.insert(0, path)` where path is your installation folder

## Exploring the content 
There are four level of users: 
1. **Interface user**: explore models and their straightforward use. No code expertise required. simply execute `import chimes as chm; chm.Interface()` in a new `.ipynb` file or explore `tutorials/01_Interface.ipynb`
2. **Code user**: that use the library through code and manipulate existing models without changing their logics. We recommend to go through the folder `tutorials/02_[...].ipynb` and go through the files in order. you can also go in `docs/notebooks` and find inspiration in other user's notebooks. Once you feel confident, create your own notebooks!
3. **Modeler**: you write your own models and modify existing ones. You can look in the folder `tutorials` at the `write_models.md`, and explore all models in the `models` file. Once you feel confident you can do a copy of `models/__TEMPLATE__.py` or `models/__MINITEMPLATE__.py`, then modify it. We recommend you to get inspiration from existing models. We recommend: [ ] for extremely short model, [ ] for well-documented model, [ ] for multisectoral model with supplements, [ ] for webbing models together. 
4. **Developer**: first, thank you! You can explore the `chimes` folder and modify its content. You can explore the [existing issues](https://github.com/georgetown-ejp/CHIMES/issues), transform model supplements [ ] into general methods. Please explore `tutorial/04_ForModellers.ipynb`




## Components 

it is composed of :
* A `Model` base of files that contains  description, the mathematical logical links they are composed of, preset values, and supplements
* A `Field` base (any quantity measurable in the real world) with its name, unit and default value
* A `Database that contains the value of the natural world related to models (WIP)
* A method to load models and interact with it
* A solver library for high-speed simulation with a C core using an RK4 method
* An analysis library for statistical elements on runs
* A plot library to explore the output of the simulation
* An interface for a user-friendly experience

![image](https://github.com/georgetown-ejp/CHIMES/assets/11523050/22286361-1d5e-48c3-9d6c-d3179eb27515)
* The flow inside the library*

## Running the tests


## Authors

* [**Paul Valcke**](https://github.com/DaluS) - *Initial project, architecture, models, toolboxes, matplotlib, core* -
* [**Didier Vezinet**](https://github.com/Didou09) - *Class set, initial structure* -
* [**Stephen Kent**](https://github.com/stephen-kent) - *Server structure, refractors, dashboard* -
* [**Weiye Zhu**](https://github.com/I-dontlikeit) - *Redivis-exiobase coupling* - 

See also the list of [contributors](https://github.com/georgetown-ejp/CHIMES/contributors) who participated in this project.





# To upgrade [ NOT REALLY PART OF THE README ]

Status list (here taken from pySD)
- [ ] The github to be public (should makes the maintained status to work)
- [ ] https://coveralls.io for the pytest coverage ?
- [ ] Publish in JOSS 
- [ ] Readthedocs page


[![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)](https://github.com/georgetown-ejp/CHIMES/pulse)
[![Coverage Status](https://coveralls.io/repos/github/SDXorg/pysd/badge.svg?branch=master)](https://coveralls.io/github/georgetown-ejp/CHIMES?branch=devel)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pysd/badges/version.svg)](https://anaconda.org/conda-forge/pysd)
[![PyPI version](https://badge.fury.io/py/pysd.svg)](https://badge.fury.io/py/pysd)
[![PyPI status](https://img.shields.io/pypi/status/pysd.svg)](https://pypi.python.org/pypi/pysd/)
[![Py version](https://img.shields.io/pypi/pyversions/pysd.svg)](https://pypi.python.org/pypi/pysd/)
[![JOSS](https://joss.theoj.org/papers/10.21105/joss.04329/status.svg)](https://doi.org/10.21105/joss.04329)
[![Contributions](https://img.shields.io/badge/contributions-welcome-blue.svg)](https://pysd.readthedocs.io/en/latest/development/development_index.html)
[![Docs](https://readthedocs.org/projects/pysd/badge/?version=latest)](https://pysd.readthedocs.io/en/latest/?badge=latest)
