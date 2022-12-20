# DashBoard NBA

## Introduction

Ce projet s'effectue dans le cadre de l'unité E3FI-PR2 supervisée par Daniel Courivau. L'objectif est d'utiliser le language de programmation python pour créer un DashBoard interactif sur le sujet notre choix. Nous avons choisis de baser notre projet sur les statistiques offensives des joueurs NBA. Les données des joueurs sont récupérées sur le site  [basketball reference](https://www.basketball-reference.com) dans l'onglet 'Leader' -> '2022-2023 NBA' -> 'Points'.
Pour chaque joueur, 30 données statistiques différentes sont disponibles sur le site. Par exemple, nous avons leur poste, leur équipe, le nombre de points marqué, le nombre de passe, les pourcentages de reussite et leur nombre de match joué.

Tous les fichiers nécessaire à la bonne exécution du projet sont disponibles dans ce dépôt GIT. Il vous faudra simplement installer les modules comme expliqué à la section 'User Guide'.

## User Guide

### Installation des modules et du dépôt GIT

Pour utiliser le DashBoard sur votre machine, vous devez vous assurer d'avoir correctement installer Git.
Vous devez cloner le depôt du projet sur votre machine. Pour ce faire, entrez la commande suivante dans un terminal:
```
$ cd Votre_Repertoire_De_Travail
$ git clone https://github.com/vyyyn93/DashBoard_Marvyn_Mehdi.git
```
Le projet utilise les modules suivants:
beautifulsoup4==4.11.1
* dash==2.7.0
* nominatim==0.1
* requests==2.28.1
* plotly==5.11.0
* dash==2.7.0
* dash-bootstrap-components==1.2.1
* dash-core-components==2.0.0
* dash-html-components==2.0.0
* dash-table==5.0.0

Pour installer ces modules, rendez vous dans le repertoire où vous avez initaliser le dépôt GIT et entrez la commande suivante dans un terminal:

``` 
$ python -m pip install -r requirements.txt
```

Pour lancer le scrapping des données et initialiser le DashBoard, exécutez cette commande dans le terminal.
```
$ python main.py
```

Vous pouvez consultez le DashBoard [ici](http://127.0.0.1:8050/).

### Utilisation du DashBoard

Le DashBoard est composé de 2 pages distinctes. Pour passer d'une page à l'autre, cliquez sur le bouton 'Map' ou 'Histogramme'. La bouton de la page où vous vous trouvez change de couleur et deviens plus sombre.  

Sur la page 'Histogramme', vous trouvez d'abord l'histogramme du nombre de point par match. Pour visualiser l'histogramme des passes par match, cliquez sur le bouton 'Assists Per Game' situé en dessous de l'histogramme.

Sur la page 'Map', vous trouvez la géolocalisation des 10 meilleurs scoreurs NBA classés via la statistique point par matchs (PPG). Cliquez sur les Pop-Up rouges pour découvrir le nom du joueur, son classement, son équipe et son nombre de PPG.
En dessous de la map, vous pourrez visualiser le classement en détail des 20 meilleurs scoreurs, ainsi que leur poste.

## Rapport d'analyse
Les histogrammes nous donnent une repartition des tâches offensisves princirpales (Scoring et playmaking) parmis les joueurs NBA. En particulier dans ce sport, nous remarquons que l'apport offensif est inégalement répartis.
Comme nous pouvons le voir sur l'histogramme des PPG, la grande majorité des joueurs marquent en moyenne entre 0 et 7 points par match. Sachant qu'une équipe NBA marque en moyenne 110 points par match, on se rend compte que l'apport offensif est très faible pour la majorité de ces joueurs. C'est encore plus flagrant pour les passes où plus de la moitié des joueurs effectue entre 0 et 1,5 passes par match (une équipe effectue en moyenne 25 passes). Ces graphiques montrent l'hétérogénéité du niveau des joueurs NBA et la montée en puissance de l'héliocentrisme des stars qui deviennent indispensable pour leur équipe car seulement 0,08% des joueurs NBA marquent plus de 20 points par match. 

La map nous montre une repartition homogène des meilleurs joueurs. En effet, les meilleurs scoreurs sont équitablements repartis entre les deux conférences avec 5 joueurs à l'Est, et 5 joueurs à l'Ouest.
Cela montre un niveau homogène entre ces deux conférences, ce qui n'était pas aussi juste quelques années auparavant où la conférence Ouest regroupait plus de stars et où le niveau y était bien plus rélevé.
  
## Guide de développement

### Structure du projet

Le projet est divisé en plusieurs fichiers.
* **create_dataFrame.py** regroupe les fonctions de scrapping, l'url du site, la création et le traitement de la dataFrame. Les fonctions sont utilisées au début du fichier main.py
* **create_map.py** contient les fonctions et le code liés à la création de la map.
* **main.py**  contient le programme principal. Il initialise les composants, récupère les données sur le site, crée la dataFrame et le DashBoard.
* **map.html** est le fichier de la map affiché sur le DashBoard.
* **README.md** est le fichier de présentation du projet que vous êtes actuellement en train de lire.
* **requirments.txt** contient le nom des modules et leurs versions nécessaire au bon fonctionnement du projet.
* **style.py** regroupe les styles CSS des composants du DashBoard. Ces styles sont initialisés sous forme de disctionnaire et importé dans le programme principale main.py

La structure du programme peut-être résumé avec le graphique suivant:  

[![](https://mermaid.ink/img/pako:eNpNUDEOgzAM_ErkiUq0D2DoUtStEx0jVVZiChIJKJgB0T6o7-jH6gBFZLByzt3ZuQlMawkyeAbsKnXPtVdyTN8nPY8NnbrxoI7Hs3rNUF2K4uWw9kks8XHh2zIxgZDpYZHxGtDtlFtrVq4DMDCJSXeq2DUrUeCeIvDvGombnwnfD3LdehUFs5P2kIKjIGorn5migwauyJGGTK6WShwa1qD9W6g4cFuM3kDGYaAUhk6WpLxGicFBVmLTS5dszW24LQHNOb1_r9JnQA?type=png)](https://mermaid-js.github.io/mermaid-live-editor/edit#pako:eNpNUDEOgzAM_ErkiUq0D2DoUtStEx0jVVZiChIJKJgB0T6o7-jH6gBFZLByzt3ZuQlMawkyeAbsKnXPtVdyTN8nPY8NnbrxoI7Hs3rNUF2K4uWw9kks8XHh2zIxgZDpYZHxGtDtlFtrVq4DMDCJSXeq2DUrUeCeIvDvGombnwnfD3LdehUFs5P2kIKjIGorn5migwauyJGGTK6WShwa1qD9W6g4cFuM3kDGYaAUhk6WpLxGicFBVmLTS5dszW24LQHNOb1_r9JnQA)


### Le programme principale main.py
Le programme principale peut se diviser en parties distinctes. N'hésitez pas à utiliser les régions implémentées au début de chaque section pour faciliter la lecture du code:

* Scrapping et création de la dataFrame: Le programme utiliser les fonctions *create_dataframe*, *stat_to_integer* et *traitement_dataFrame* pour respectivement scrapping le site et crée la dataFrame, convertir les statistiques qui represente des chiffres en integer et nettoyer les données de la dataFrame.
* Création des graphiques plotly: ici  nous initialisons les graphiques utilisés dans le dashBoard (le tableau et les deux histogrammes).
* Création des composants Dash: Cette section initialise les composants relatif à la bibliothèque Dash (titres, radioItem, map, graph).
* Création du DashBoard: Nous créeons ici le DashBoard en implémentant dans le bon ordre les composants dans des conteneurs Div et Tabs.
* Définition des méthodes de callback

La création de la map utilise le module Nominatim. Le programme est disponible dans le fichier create_map.py. Néanmoins, le programme ne marche pas à chaque fois pour une raison inconnue. La map est donc déjà construite dans le fichier map.html et est utilisé dans le DashBoadrd. 
Vous pouvez lancer le programme avec la commande suivant:
```
$ python create_map.py
```
Si le programme fonctionne, la map créée ecrasera la map actuelle et sera utilisé dans le DashBoard.

