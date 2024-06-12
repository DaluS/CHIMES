# Condensed tutorial

You want to learn every basic things in one file, through examples ? This is the right example for you, mixing everything at once


```python
# Basic imports
import numpy as np

# requirements install, uncomment, execute, then comment once done
#!pip install -r ../../../../requirements.txt

# CHIMES IMPORTATION
import sys
sys.path.insert(0, '../../')
import chimes as chm
```


```python
# IMPROVING THE DISPLAY (OPTIONAL) ##############################
# Better display of tables
import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option("display.colheader_justify","left")

# Interactive tables 
from itables import init_notebook_mode,options
options.columnDefs = [{"className": "dt-left", "targets": "_all"}]
options.classes="display nowrap compact"
options.scrollY="400px"
options.scrollCollapse=True
options.paging=False
init_notebook_mode(all_interactive=True)

# traditional display for ipython
from IPython.display import display,HTML,Markdown
from IPython.display import IFrame

# Better display of plots: latex encoding in plotly
%matplotlib widget
import plotly
plotly.offline.init_notebook_mode()
display(HTML('<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_SVG"></script>'))
```

## get methods

chimes (chm) has multiple methods to explore what is available. Typically with `get_available` methods (use tab or ? to have more informations)


```python
chm.get_available_models() # List of available models
```


```python
chm.get_model_documentation('Lorenz_Attractor') # more documentation
```

## Hub to load a model

The Hub is the object to manipulate a model (equations, presets, plots associated to it...)


```python
hub=chm.Hub('Lorenz_Attractor',verb=True) # Load a model
```


```python
hub.get_summary() # All informations about a model
```


```python
hub.run() # Do a simulation on 100 years
```


```python
hub.plot(tini=200,tend=400) # Plot the results
```


```python
hub.set_fields(dt=0.01,Tsim=40) # Change the time step a the simulation duration
hub.run()
chm.Plots.XYZ(hub,'x','y','z',color='distance2') # Plot the 3D trajectory with the plots in `chm.Plots`
```


```python
chm.get_available_plots()
```


```python
chm.get_plot_documentation('XYZ')
```


```python
hub.set_fields(sigma=10,rho=28,beta=8/3,x=0,y=10,z=0.01) # Change the parameters
hub.run()
```


```python
hub.plot()
```


```python
hub.get_Network(params=True,auxilliary=True)
```


```python
hub.get_presets() # List of available presets
```


```python
hub.get_supplements() # List of available supplements
```


```python
hub=chm.Hub('Lorenz_Attractor','BeginEQ1') # Load a model with a preset
hub.run()
hub.plot_preset() # Plot the results with the preset
```


```python
hub=chm.Hub('Lorenz_Attractor','BeginEQ1') # Load a model with a preset
hub.run_uncertainty(1,N=10) # Do 10 system in parrallel with each value taken 1% around the original
hub.plot_preset()
```


```python
chm.Plots.Var(hub,'x',mode='sensitivity')
```


```python
hub=chm.Hub('Lorenz_Attractor','BeginEQ1') 
hub.supplements['OneTenthPercentUncertainty'](hub) # Execute the supplementary function. See the docu1mentation for more informations
```


```python
# Using the shock module
hub=chm.Hub('GK','debtstabilisation') # Load a model 
hub.set_fields(Tsim=130,eta=0.1) # Change the time step a the simulation duration, and inflation dynamics

choc_it = 600 # Select the iteration at which there will be a shock
hub.run(steps=choc_it,verb=1) # Run choc_it iterations

v=hub.get_dvalues() # Get the values of the variables 
hub.set_fields(K=v['K'][choc_it]/1.6,noreset=True)
hub.run()
chm.Plots.XYZ(hub,'omega','employment','d','time',title='Stabilisation, destabilisation, then re-stabilisation')
```


```python
# Will find all presets, run them and show their difference
hub=chm.Hub('GK')
hub.compare_presets(['K','employment','omega','d','kappa'])
```


```python

```
