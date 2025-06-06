---
title: 'CHIMES: modular modeling of dynamical system with tensors'
tags:
  - Python
  - System Dynamics
  - Tensor
  - Economy
  - Ecology
authors:
  - name: Paul Valcke
    orcid: 0000-0002-7290-8881
    affiliation: 1
  - name: Didier Vezinet
    orcid: 
    affiliation: 2
affiliations:
 - name: The Earth Commons, Georgetown University, 20007 Washington DC, USA
   index: 1
 - name: Cool Nuclear Fusion Stuff, Massachussets, USA
date: 25 December 2023
bibliography: paper.bib

---

## Summary

### Context 

System Dynamics are ubiquitous in process-based representation of complex systems. 

Used in many disciplines [ ], multiple formalisms [ ]

Models often coupled [] 

Interdisciplinary systems more required, complexity models more required [], computation costs bigger []

In particular ECO-ECO Tensor dynamics [], finite differences tensor too 

[Existing structures Stella, Vensim, PySD, Not practical ][ Minsky ]

[Cassandra]


Covering it all 

### Main functional elements 


## Statement of need




System Dynamics (SD) is a mathematical approach used to describe and simulate the dynamics of complex systems over time. The foundations of the methodology were laid in the 1950s by Professor Jay W. Forrester of the Massachusetts Institute of Technology . The building blocks of SD models are stocks, flows, variables, parameters, and lookup tables. Stocks represent cumulative quantities which take a certain value at each moment in time (integral), and flows are the rates at which those quantities change per unit of time (derivative). Variables express intermediate calculations, parameters set external conditions for the simulation, and lookup tables are single-valued functions that accept another model component as an argument. These components can combine to create feedback loops in which the state of the stock variables feeds back to influence flows in the model. The relationships between these model components can be represented using causal loop diagrams, see Figure .


Since its inception, the SD methodology has been applied in different areas, including manufacturing, energy, climate, population, ecology and economics [@croads:2012;@Moallemi:2021;@FETENEADANE2019212;@harvey:2021]. In the 1990s, the popularity of the methodology gave rise to the development of several visual programming systems for building SD models. These domain-specific modeling environments were widely adopted by the SD community due to their convenient graphical user interfaces. Stella&#174; and Vensim&#174;, though not open-source, are two of the most popular commercial system dynamics modeling tools, but many others exist (see @wiki:Comparison_of_system_dynamics_software;@sdopentools).

PySD is a Python library that transpiles models built in Stella&#174;'s or Vensim&#174;'s domain-specific languages into Python, allowing the user to load, parametrize and execute SD models, and to take advantage of the extensive data-science capabilities of the Python ecosystem. PySD was first released in September 2014 by James Houghton [@houghton_siegel_2015].

The main functional elements of PySD are 1) a set of parsing expression grammars (PEGs) (and their corresponding node visitor classes) to parse models built using Stella&#174; and Vensim&#174; (in *.xmile* and *.mdl* formats, respectively); 2) isomorphic implementations of the most frequently used Stella&#174; and Vensim&#174; built-in functions and other basic operations; 3) a builder, to write the parsed model code in Python and 4) a fordward Euler solver to run the models.

In addition to the aforementioned core functionality, PySD also allows users to import model inputs from external sources (from spreadsheet files), modify model variables at runtime, split models into any number of modules and submodules (corresponding to Vensim&#174; views), isolate parts of a model to be run individually, store intermediate simulation results and resume the simulation from that particular state, and run models using PySD alone (without Stella&#174; or Vensim&#174;). All these features are made available to the user through a command-line interface.

Despite its maturity, PySD is currently in a very active development phase, and a proof to that is that most of the extra features listed in the paragraph above were implemented in the 21 months that separate releases *v0.11.0* and *v3.7.0*.

The main novelty introduced in release *v3.0.0* is that the parsing process is now isolated from the building process, which opens the door to the development of additional model builders (in Python) to write the output models in any programming language. This has been achieved by creating an intermediate abstract model representation (AMR), as shown in Figure \ref{fig:ABSTRACTMODEL}, that embeds all the information contained in the original models, plus additional information such as the order of operations, in pure Python objects.

![New model parsing-building logic in PySD v3.0.0. PEG acronym stands for Parsing Expression Grammar. \label{fig:ABSTRACTMODEL}](abstract_model.pdf)

Future releases will focus on cutting down simulation times and on including additional built-in Stella&#174; and Vensim&#174; functions. The most relevant performance-oriented development will be the migration from xarray to numpy to perform array operations, which in addition to the expected overhead reduction will also allow for further potential model optimizations (i.e. JIT compilation).

## Statement of need

Stella&#174; and Vensim&#174; are excellent tools for model conceptualization and design using causal loop diagrams. Their solvers are easy to parametrize, efficient (implemented in C and C++) and thoroughly tested. However, the Python ecosystem offers powerful open-source tools for data visualization, sensitivity analysis, graph theory, machine learning and other data analysis tasks that are unavailable in the domain-specific modeling environments. Most importantly, though models created using Stella&#174; and Vensim&#174; can be exported into text format (*.xmile* and *.mdl*, respectively), users must install propietary software in order to execute the models and visualize the results.

PySD was designed to supplement the capabilities of the domain-specific modeling tools by bringing their outputs into the larger Python data analytics ecosystem. This approach allows users to integrate their models with the most up-to-date analytics tools, and allows the large Stella&#174; and Vensim&#174; user-base to make their models fully open-source and sharable.

PySD is in use by hundreds of modelers and data scientists in academia, industry, and government; and has been used in over two dozen academic publications. The latest improvements to the library have taken place in the context of the European H2020 projects MEDEAS [@medeasproj] and LOCOMOTION [@locomotionproj], in which several authors of the present work participate. The MEDEAS project ended in early 2020, and aimed at developing an Integrated Assessment Model (IAM), named *pymedeas* [@pymedeas:2020;@samso:2020], to analyze different energy transition scenarios under biophysical constraints (e.g. climate change and resource availability). The LOCOMOTION project, which is still ongoing (2019-2023), aims to build a new and more complex IAM, departing from the one developed during the MEDEAS project. In MEDEAS the model was built using Vensim&#174;, and later translated to Python using PySD, and the same approach is being used in the LOCOMOTION project.

## Acknowledgements

This work was supported by []. T
The author would like to acknowledge the users of the code []


## References









\ref{fig:CLD}
[@Forrester:1971]
![An example Causal Loop Diagram showing how the various components of system dynamics models are visualized by domain-specific modeling environments. \label{fig:CLD}](CLD_example.pdf)