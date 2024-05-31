# <a id='toc1_'></a>[TP Introduction CHIMES](#toc0_)

**Table of contents**<a id='toc0_'></a>    
- [TP Introduction CHIMES](#toc1_)    
  - [Importation de la librairie](#toc1_1_)    
- [Introduction: Attracteurs](#toc2_)    
  - [Introduction : Systemes dynamiques, sensibilite, chaos](#toc2_1_)    
    - [Questions](#toc2_1_1_)    
    - [Instabilites](#toc2_1_2_)    
    - [Incertitude](#toc2_1_3_)    
  - [Goodwin-Keen: credit, and debt crisis](#toc2_2_)    
    - [Questions sur la courbe de Phillips](#toc2_2_1_)    
    - [Questions sur l'investissement](#toc2_2_2_)    
    - [Incertitudes de trajectoires](#toc2_2_3_)    
    - [Sensibilite individuelles](#toc2_2_4_)    
  - [Goodwin-Keen et chocs](#toc2_3_)    
  - ["Coping with Collapse" Modele economie-climat](#toc2_4_)    

<!-- vscode-jupyter-toc-config
	numbering=false
	anchor=true
	flat=false
	minLevel=1
	maxLevel=6
	/vscode-jupyter-toc-config -->
<!-- THIS CELL WILL BE REPLACED ON TOC UPDATE. DO NOT WRITE YOUR TEXT IN THIS CELL -->

Le but du TP est de manipuler des modeles dynamiques et de comprendre leur comportement, force et faiblesse.
Pour ce, on utilisera 3 modeles differents de plus en plus complexe.



## <a id='toc1_1_'></a>[Importation de la librairie](#toc0_)


```python
# Telecharger la librairie qui contient le TP et ses fonctions
!git clone https://github.com/DaluS/CHIMES

# Installer les dependances de la librairies
!pip install -r Climath-CHIMES/requirements.txt

# If you use google collab
from google.colab import output
output.enable_custom_widget_manager()


# A ACTIVER POUR DES FIGURES INTERACTIVES
import matplotlib.pyplot as plt
```


```python
# Add the library the the path
import sys
sys.path.insert(0,  "../../" )
#sys.path.insert(0,  "CHIMES" )
import chimes as chm

%matplotlib widget
```


```python
plt.close('all') # A exectuer si vous avez trop de figures ouvertes
```

# <a id='toc2_'></a>[Introduction: Attracteurs](#toc0_)

Ici on visualise simplement des trajectoires "chaotiques" pour quatres modeles differents. C'est une intro "mathematique" aux systemes dynamiques


```python
dhub={} 
for ii,attractor in enumerate(['Lorenz','Halvorsen','Aizawa','Rossler']):
   dhub[attractor]=chm.Hub(attractor+'_Attractor')
   if ii:
      dhub[attractor].set_fields(dt=0.05,Tsim=200)
   else: 
      dhub[attractor].set_preset('Canonical example')
   dhub[attractor].run()
   chm.Plots.XYZ(dhub[attractor],'x','y','z',title=attractor)
```

## <a id='toc2_1_'></a>[Introduction : Systemes dynamiques, sensibilite, chaos](#toc0_)

Avant de rentrer dans le coeur de modeles economiques, nous n'avons pas vu en cours l'importance des incertitudes et sensibilite des parametres.
Pour ce, on va etudier un systeme qui symbolise toutes les difficultes dans ce type de systeme: l'attracteur de Lorenz.


```python
chm.get_model_documentation('Lorenz_Attractor') # Donne la documentation sur le modele "Lorenz_Attractor"
```

### <a id='toc2_1_1_'></a>[Questions](#toc0_)
1. Quel nombre d'equation il y a dans ce systeme ?
2. Combien y a-t-il de points d'equilibres ? Lesquel ?



```python
hub=chm.Hub('Lorenz_Attractor','Canonical example',verb=False) #importer le modele
hub.run() #fais une simulation
hub.plot() #representer les variables
chm.Plots.XYZ(hub,'x','y','z') #representer en 3D
```

### <a id='toc2_1_2_'></a>[Instabilites](#toc0_)

On commence le systeme au niveau d'un point d'equilibre.  


```python
hub=chm.Hub('Lorenz_Attractor','BeginEQ1') #importer le modele
hub.run() #fais une simulation
hub.plot()
chm.Plots.XYZ(hub,'x','y','z')
```

3. Decrire la trajectoire. Le point d'equilibre est-il stable ?
4. A partir de quand les effets non-lineaire sont a prendre en compte ?
5. Le point initial est-il important dans un tel systeme ?
6. Bonus: calculer analytiquement l'equilibre du point



Le point d'équilibre vient lorsque $\frac{dx}{dt} = 0$, $\frac{dy}{dt} = 0$, $\frac{dz}{dt} = 0$. Bien entendu, le point $(0, 0, 0)$ est toujours un point d'équilibre.
Regardons plus en détail les points d'équilibre :
\begin{align*}
0 &= \sigma (y-x) \\
0 &= x*(\rho - z) - y \\
0 &= xy - \beta z \\
\end{align*}
d'où : $y = x$, $z = \frac{x^2}{\beta}$ et $x = \pm \sqrt{ \beta (\rho - 1)}$. Ceci n'est valable effectivement que dans le cas où $\rho > 1$.

Ce qui donne :
\begin{align*}
x &= \pm \sqrt{ \beta (\rho - 1)} \\
y &= \pm \sqrt{ \beta (\rho - 1)} \\
z &= \rho - 1
\end{align*}

Comme précisé plus tôt, les points d'équilibre sont symétriques par rapport à l'axe (Oz) !


### <a id='toc2_1_3_'></a>[Incertitude](#toc0_)

Lorsque l'on fait de la simulation, on utilise usuellement une valeur par parametre/condition initiale calibree. Hors, il peut exister une incertitude sur ces calibrations.
A quel point cela affecte la clarte des resultats ?

Ici, on fait tourner en parrallele 10 simulations avec des valeurs de conditions initiales qui varient de 0.01%. On fait ensuite un calcul de l'evolution moyenne et de l'ecart-type sur la simulation


```python
hub=chm.Hub('Lorenz_Attractor','Canonical example')
hub.run_uncertainty(0.01) # On fait 0.01% d'erreur sur les valeurs des champs
hub.plot(idx=0,filters_key=['x','z'],separate_variables={'':'x'}) # On regarde le premier systeme
hub.plot(idx=1,filters_key=['x','z'],separate_variables={'':'x'}) # On regarde le deuxieme systeme

```

7. Qualitativement les deux trajectoires sont-elle les meme ?


```python
chm.Plots.plotnyaxis(hub,[['x']],title=r'Uncertainty for 0.01% of error on fields value') # On regarde l'incertitude sur x et y
```

8. A partir de quand la prediction de trajectoire cesse-t-elle d'etre correcte avec cette incertitude ?
9. Que ce passe-t-il au point de rupture ?
10. Discuter, dans ce contexte, la difficulte de la modelisation en sociologie ou "chaque decision est une bifurcation"
11. Quelles proprietes emergentes pourrait-on etudier d'un tel systeme sans souffrir de cette sensibilite ?
12. BONUS: Etablir qualitativement une relation entre le taux d'incertitude et le moment la simulation se perd dans l'incertitude. On pourra utiliser le code en dessous, en le modifiant avec une boucle for


```python
for incertitude in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
  hub=chm.Hub('Lorenz_Attractor','Canonical example')
  hub.set_fields('Tsim',50)
  hub.run_uncertainty(incertitude) # On fait 0.01% d'erreur sur les valeurs des champs
  chm._plots.plotnyaxis(hub,[['x']],title=f'Uncertainty for {incertitude}% of error on fields value') # On regarde l'incertitude sur x et y
```

## <a id='toc2_2_'></a>[Goodwin-Keen: credit, and debt crisis](#toc0_)

On etudie maintenant un modele dit de "Goodwin-Keen" c'est a dire le modele de Goodwin (debut du cours) avec en plus une possibilite d'investissement par endettement, et une possibilite d'inflation.


```python
chm.get_model_documentation('GK') # Donne la documentation sur le modele "GK"
```

### <a id='toc2_2_1_'></a>[Questions sur la courbe de Phillips](#toc0_)
13. Qu'est-ce que la courbe de Phillips ?
14. Qu'est-ce qui est en entree, qu'est-ce qui est en sortie ?
15. Que se passe-t-il quand lambda tends vers 1 ?
16. Quel impact sur l'espace des phases par rapport a une forme lineaire ? Cela semble-t-il realiste ?

### <a id='toc2_2_2_'></a>[Questions sur l'investissement](#toc0_)
17. Qu'est-ce que le terme kappa ici ?
18. Sous quel critere on peut avoir $\kappa(\pi) \approx \pi$ ? Quelle dynamique dans ce cas la ?


```python
hub=chm.Hub('GK') #importer le modele
#hub.get_Network() # Montre le diagrame causal du modele. Si cela ne marche pas, affichez directement le fichier "GK.html"

# Basic run
hub.set_fields('Tsim',100)
hub.set_fields('eta',0)
hub.run()
hub.plot()
chm._plots.XYZ(hub,'employment','omega','d')
chm._plots.Var(hub,'employment',mode='cycles',title='Employment')
chm._plots.Var(hub,'d',mode='cycles',title='debt ratio')

```

19. Cette simulation converge-t-elle vers un état stable ?
20. Decrire l'evolution de la dette privee. La dette privee converge-t-elle ? Le ratio de dette privee converge-t-il ?  

### <a id='toc2_2_3_'></a>[Incertitudes de trajectoires](#toc0_)

On suppose que le modele est correctement parametrise (ce n'est pas le cas). On regarde l'effet de l'incertitude.



```python
hub=chm.Hub('GK')
hub.run_uncertainty(8)
chm._plots.plotnyaxis(hub,[['employment'],['omega'],['d']],title=r'Uncertainty for 5% of error on fields value') # On regarde l'incertitude sur x et y
```

21. Lancer plusieurs fois le code avec 8% d'incertitudes sur les valeurs. Qu'observez vous ?

### <a id='toc2_2_4_'></a>[Sensibilite individuelles](#toc0_)

Cette fois, on analyse les impacts separes des differentes valeurs du systeme


```python
hub=chm.Hub('GK')
hub.set_fields('Tsim',30)
out= hub.sensitivity(std=0.05) # 5% d'erreur sur les valeurs
chm._plots.Showsensitivity(out,vars=['omega','d']) # title='Influence des changements de variables sur omega et d'

chm._plots.Showsensitivity(out,vars=['Y']) # plot sur la variable Y (PIB)
```

22. Quel sont les valeurs les plus impactantes ? A quel moment dans le run la sensibilite est-elle la plus elevee ? Pourquoi sur Y les incertitudes grandissent-elle et pourquoi ?

23. Proposer une classification des variables selon qu'elles impacte le debut et la fin de run, et les variable de sortie observe

## <a id='toc2_3_'></a>[Goodwin-Keen et chocs](#toc0_)

Un systeme economique peut subir des chocs exogene, qui viennent changer des valeurs dans le systeme, le perturber...


```python
hub=chm.Hub('GK')
hub.run(steps=500,verb=False)
R=hub.get_dfields()
K0=R['K']['value'][500,0,0,0,0]
hub.set_fields(**{'K':K0/2},noreset=True)
hub.run()
hub.plot(filters_units=['','Units','y'],separate_variables={'':['pi','kappa']},title='capital shock')
```

24. Qu'est-ce qui se passe a T=50 ? Comment le systeme reagit-il ?



```python
hub=chm.Hub('GK')
hub.run(steps=500,verb=False)
R=hub.get_dfields()
delta=R['delta']['value'][0,0,0,0]
hub.set_fields(**{'delta':delta*10},noreset=True)
hub.run()
hub.plot(filters_units=['','Units.y^{-1}','y'],separate_variables={'':['pi','kappa']},title='depreciation shock')

```

25. Qu'est-ce qui est fait au systeme ici quelles consequences ?


```python
hub=chm.Hub('GK')
hub.get_summary() #Valeurs a l'etat initial
for i in range(19):
    hub.run(steps=50,verb=False)
    R=hub.get_dfields()
    delta=R['delta']['value'][0,0,0,0]
    hub.set_fields(**{'delta':delta*1.2},noreset=True,verb=False)
hub.run()
hub.plot(filters_units=['','Units','y'],separate_variables={'':['pi','kappa']},title='Exponential damages')
hub.get_summary() #Valeurs a l'etat final
```

26. Decrire ce qui est modelise ici. Que se passe-t-il a la fin du systeme ?



```python
### Multiples chocs aleatoires

import numpy as np
hub=chm.Hub('Goodwin_example',verb=False)

################################
currentvalues = {
    'delta':0.05,
    'nu':3,
    'alpha':0.02,
    'n':0.025,
}
events = {k:[] for k in list(currentvalues.keys())+['iteration']}
events['iteration'].append(0)

stepmaxsize = 10
stepminsizse = 1

relativevariation = 0.1

################################

itot=0
while 1:
    morestep = np.random.randint(stepminsizse,stepmaxsize)
    itot+=morestep
    if itot > 998:
        break
    else:
        hub.run(steps=morestep,verb=False)

    for k,v in currentvalues.items():
        currentvalues[k]*= np.random.normal(1,relativevariation)
        events[k].append(v)
    events['iteration'].append(itot)

    hub.set_fields(**currentvalues,
                   noreset=True,verb=False)

hub.run()
hub.plot(filters_units=['','Units','y'],
         title='Chocs')
chm._plots.XY(hub,'omega','employment',title='Chocs')

```

27. Expliquer ce que fait ce code.

28. Que pouvez-vous dire des trajectoires ? Que se passe-t-il quand on fait varier l'intensite du bruit ? Que se passe-t-il quand on relance plusieurs simulations ?

## <a id='toc2_4_'></a>["Coping with Collapse" Modele economie-climat](#toc0_)

Pour finir, voici un modele qui incorpore toutes les dynamiques precedentes, avec endogenisation de certains coefficients par fonction de dommage (qui substituent les chocs de la valeur de $\delta$) et une politique de decarbonation


```python
chm.get_model_documentation('GEMMES_Coping2018')
```


```python
print('Business as usual without climate damages')
hub1=chm.Hub('GEMMES_Coping2018',preset='BAU',verb=False)
hub1.run()
hub1.plot_preset()

print('Business as usual with climate damages')
hub2=chm.Hub('GEMMES_Coping2018',preset='BAU_DAM',verb=False)
hub2.run()
hub2.plot_preset()


print('transition scenario with climate damages')
hub3=chm.Hub('GEMMES_Coping2018',preset='TRANSITION',verb=False)
hub3.run()
hub3.plot_preset()
```

29. Decrire les dynamiques dans les trois scenarios. Discuter la difference de trajectoire dans l'espace des phases entre le scenario "Business as usual" et le scenario de transition



```python
hub4=chm.Hub('GEMMES_Coping2018')
```


```python
hub4=chm.Hub('GEMMES_Coping2018',preset='TRANSITION',verb=False)
hub4.run_uncertainty(5,N=100)
chm._plots.plotnyaxis(hub4,[['employment','omega'],['d'],['Y']])
```


```python
hub5=chm.Hub('GEMMES_Coping2018',preset='TRANSITION',verb=False)
hub5.set_fields('Tsim', 50)
out= hub5.run_sensitivity(std=0.05,keys=['r', 'rhoAtmo', 'gammaAtmo', 'Capacity',  'Nmax', 'deltapbackstop', 'apc', 'bpc', 'deltagsigmaEm', 'deltaEland', 'eta', 'mu', 'F2CO2','kappalinConst', 'kappalinSlope','pi1', 'pi2', 'pi3', 'zeta3', 'fk']) # 5% d'erreur sur les valeurs
chm.Plots.Showsensitivity(out,vars=['omega','d']) # title='Influence des changements de variables sur omega et d'
```

30. A partir de ce modele, que penser de 5% d'incertitude dans les mesures du monde ?
31. Quels sont les parametres les plus important d'apres cette simulation ?

## ICED Physical and nominal circuits 


```python
hub=chm.Hub('ICED')
#hub.get_summary()
hub.set_fields(**{'D':1,'r':0.05,'Delta':0.1,'kappaC':0.5,'w':0.4,"Delta":0.4,"Tsim":0.1,'Hw':.5,'Hc':0.1})
hub.run()
S1,S2=hub.supplements['Sankey'](hub)
S1.show()
S2.show()
```

    Already run: reset and run
    





# ICED Introduction: Submodels 

ICED can be seen as: 
* An extended Goodwin model (CHI)
* A Three-sector productive sector with shared accountability: two energy (green and brown) sector that feeds an output sector
* An ensemble of endogenization for social variables
* A Climate sector and its feedback

## 3-Capital dynamics


```python
hub=chm.Hub('3Capital',verb=False)
hub.set_fields('omega',0.6)
hub.set_fields('pc',1)
hub.run_uncertainty(uncertainty=5)
hub.plot_preset('default')
#hub.save('3CapitalwithNothin')
```

$Y\sigma$  



$Y=C$ 

$[\Gamma Y]$+

$[\Gamma [\Gamma Y]]$+

$$Y_{nec} = \sum_k^{\infty} \Gamma^k Y$$

$$DL_{\infty} 1/(1-x) = \sum_k^{\infty} x^k $$

$$CO2_{nec} = [(1-\Gamma)^{-1}  \sigma ] * Y$$



$Y = (0,0,...,1_{pain},0,0,0)$

Si on veut un vecteur $C= (1,2,4,5)$

Il faudra produire $Ytot = [(1-\Gamma)^{-1}C] $

Ca correspond a des emissions $\Sigma = [(1-\Gamma)^{-1}\sigma] .C $


```python

```


```python

```
