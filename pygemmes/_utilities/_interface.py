import ipywidgets as widgets
from IPython.display import display,HTML,clear_output,Markdown
import numpy as np
import pandas as pd

from ...core import Hub

################# INITIALIZATION ############################## 
default = '__EMPTY__' ## DEFAULT MODEL LOAD IN THE SYSTEM 
style = {'description_width': 'initial'}
pd.set_option('display.max_colwidth', None)
AllModels = pgm.get_available_models(details=True)
hub=Hub(default,verb=False)
hub.run(verb=False)

def pprint(ldf):
    try :
        ldf = ldf.style.set_properties(**{'text-align': 'left'})
    except BaseException:
        pass
    return display(HTML(ldf.to_html().replace("\\n","<br>")))

def widgetinterface():
