# P7_FOSTER_Harris
AlgoInvest&Trade

Application python qui examine une liste d'actions pour déterminer 
la meilleure solution d'investissement pour en tirer un maximum de profit. Cette application teste toutes les
solutions possibles pour vous donner la solution la plus optimisée possible. 

Projet 7 OpenClassrooms

## Prérequis de base
1. Une application de type 'terminal' - GitBash, Mintty, Cygwin (si vous êtes sur Windows) 
   ou les terminaux par défaut si vous utilisez Macintosh ou Linux.
2. Python 3.9

## Installation
### Pour les développeurs et utilisateurs (windows 10, mac, linux) :
#### Clonez la source de AlgoInvest&Trade localement (en utilisant votre terminal) :
```sh
$ git clone https://github.com/harrisafoster/P7_FOSTER_Harris
$ cd P7_FOSTER_Harris
```
##### Dans votre terminal dans le dossier P7_FOSTER_Harris/ : Créer et activer un environnement virtuel avec (windows 10) :
```sh
$ python -m venv env
$ source ./env/Scripts/activate
```
##### Créer et activer un environnement virtuel avec (mac & linux) :
```sh
$ virtualenv venv
$ source venv/bin/activate
```
##### Et installez les packages requis avec :
```sh
$ pip install -r requirements.txt
```
## Utilisation
### Vous pouvez mettre l'application bruteforce.py en route depuis votre terminal avec :
```sh
$ python bruteforce.py
```
### Vous pouvez mettre l'application optimisation.py en route depuis votre terminal avec :
```sh
$ python optimisation.py
```

## Mode d'emploi

Différence clé entre Bruteforce.py et Opimisation.py : Bruteforce va vérifier toutes les solutions possible sans ignorer
les solutions qu'il a déjà essayé. Il prendra donc beaucoup plus de temps avec des fichiers plus importants. Il est alors
recommandé d'utiliser l'application Bruteforce uniquement avec des petits échantillons de données (moins de 50 exemplaires)

Optimisation.py va ignorer les solutions qu'il a déjà essayé et prendra donc moins longtemps avec des fichiers .csv
plus importants. Il est donc préférable d'utiliser optimisation.py pour examiner des fichiers .csv de plus de 50 exemplaires.

Il est aussi important de dire que l'application utilisera uniquement les fichiers .csv. Chaque fichier examiné doit
comprendre trois colonnes nommées 'name', 'price', et 'profit.' Dans la colonne 'profit' les nombres doivent être
des nombres de type FLOAT (%29.99 deviendrait donc 29.99 et non .2999).

Tout cela dit, une fois l'application lancée, il vous demandera quel fichier vous voudrez analyser. Il est donc impératif
que tous vos fichiers .csv se trouve dans le dossier P7_FOSTER_Harris/datasets/. Dès que vous aurez renseigné le nom du 
fichier exact (sample1.csv par exemple), il vous demandera ensuite si vous voulez garder le budget par défaut (500€) ou 
si vous voulez renseigner un budget customisé. Si vous décidez d'utiliser cette option, il faudra renseigner un nombre
entier (ex. 700). Ensuite il examinera vos données pour donner la solution optimisée sous format total dépensé, total gagné, 
et les actions à acheter pour suivre cette solution. 

## Built with
Python 3.9 