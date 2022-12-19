# DashBoard_NBA
## Introduction
Ce projet s'effectue dans le cadre de l'unité E3FI-PR2 créé par Daniel Courivau. L'objectif de ce projet est d'utiliser des outils de base pour créer un DashBoard interactif sur un jeu de donnée de notre choix. Nous avons choisis de baser notre projet sur les statistiques des joueurs NBA. Le DashBoard contient un histogramme sur le nombre total de points marqués par les joueurs NBA et une representation géolocalisée des 20 meilleurs scoreurs de la ligue (point par match).

Les données des joueurs ont été récupérer sur le site  [basketball reference](https://www.basketball-reference.com) dans l'onglet 'Leader' -> '2022-2023 NBA' -> 'Points'.
Pour chaque joueur, 30 données statistiques différentes par joueurs sont disponibles sur le site. Par exemple, nous avons acc_s à leur poste, leur équipe, le nombre de points marqué, le nombre de passe, leur pourcentage de reussite et leur nombre de match joué.

## User Guide
### Installation des modules et du dépôt GIT
Pour utiliser le DashBoard sur votre machine, vous devez tout d'abord vous assurer d'avoir correctement installer Git. Pour installer les packages nécessaire à la bonne excecution du code, entrer la commande suivante dans un terminal:
``` 
$ python -m pip install -r requirements.txt
```

Pour cloner le depôt sur votre machine, entrez la commande suivante dans un terminal:
```
$ cd Votre_Repertoire_De_Travail
$ git clone https://github.com/vyyyn93/DashBoard_Marvyn_Mehdi.git
```

Pour lancer le scrapping des données et créer le DashBoard, excecutez cette commande dans le terminal.
```
$ python main.py
```

Vous pouvez consultez le DashBoard [ici](http://127.0.0.1:8050/) 

### Utilisation du DashBoard
Le DashBoard est composé de 2 pages distinctes. Pour passer d'une page à l'autre, cliquez sur le bouton 'Map' ou 'Histogramme'. La bouton de la page où vous vous trouvez change de couleur et deviens plus sombre.  

Sur la page 'Histogramme', vous trouvez d'abord l'histogramme du nombre de point par match. Pour visualiser l'histogramme des passes par match, cliquez sur le bouton 'Assists Per Game' situé en dessous de l'histogramme.

Sur la page 'Map', vous trouvez la géolocalisation des 10 meilleurs scoreurs NBA classé via la statistique Point par Match. Cliquez sur le PopUp rouge pour découvrir le joueur évoluant à cette endroit, son classement et son nombre de PPG.
En dessous de la map, vous pourrez visualiser le classement en détail des 20 meilleurs scoreurs, ainsi que leur poste.

## Rapport d'analyse
Comme nous pouvons le voir sur l'histogramme des PPG, la grande majorité des joueurs marquent en moyenne entre 0 et 7 points par match. C'est encore plus flagrant pour les passes où plus de la moitié des joueurs effectue entre 0 et 1,5 passes par match. Ces graphiques montre l'hétérogénéité du niveau des joueurs NBA. En effet, seulement 0,08% ds joueurs NBA marque plus de 20 points par match. On voit donc l'héliocentrisme nautour des superstars, ce qui n'était pas autant le cas il y a 20 ans où la marque était mieux repartis entre les membres de l'équipe.  

La map nous montre en repartition homogène des meilleurs joueurs. En effet, les meilleurs scoreurs sont équitablements repartis entre les deux conférences avec 5 joueurs à l'Eat, et 5 joueurs à l'Ouest.
Cela montre un niveau homogène entre ces deux conférences, ce qui n'était pas aussi juste quelques années auparavent où la conférence Ouest regroupait plus de stars et où le niveau y  était bien plus relevé.
  
## Developper Guide
### Structure du projet
Le projet est divisé en plusieurs fichiers.
* create_dataFrame regroupe les fonctions de scrapping, l'url du site, la création et le traitement de la dataFrame. Les fonctions sont utilisés au début du fichier main.py
* create_map.py contient les fonctions et le coe liés à la création de la map des meilleurs scoreurs NBA.
* main.py contient le programme principal. Il initialise les composants, scrap le site, crée la dataFrame et le DashBoard.
* map.html est le fichier de la map affiché sur le DashBoard.
* README.md est le fichier de présentation du projet que vous êtes actuellement en train de lire.
* requirmeents.txt contient le nom des modules et leurs versions nécessaire au bon fonctionnement du projet.
* style.py regroupe les styles CSS des composants du DashBoard. Ces styles sont initialisés sous forme de disctionnaire et importé dans le programme principale main.py

La structure du programme peut-être résumé avec le graphique suivant:
[![](https://mermaid.ink/img/pako:eNpNUDEOgzAM_ErkiUq0D2DoUtStEx0jVVZiChIJKJgB0T6o7-jH6gBFZLByzt3ZuQlMawkyeAbsKnXPtVdyTN8nPY8NnbrxoI7Hs3rNUF2K4uWw9kks8XHh2zIxgZDpYZHxGtDtlFtrVq4DMDCJSXeq2DUrUeCeIvDvGombnwnfD3LdehUFs5P2kIKjIGorn5migwauyJGGTK6WShwa1qD9W6g4cFuM3kDGYaAUhk6WpLxGicFBVmLTS5dszW24LQHNOb1_r9JnQA?type=png)](https://mermaid-js.github.io/mermaid-live-editor/edit#pako:eNpNUDEOgzAM_ErkiUq0D2DoUtStEx0jVVZiChIJKJgB0T6o7-jH6gBFZLByzt3ZuQlMawkyeAbsKnXPtVdyTN8nPY8NnbrxoI7Hs3rNUF2K4uWw9kks8XHh2zIxgZDpYZHxGtDtlFtrVq4DMDCJSXeq2DUrUeCeIvDvGombnwnfD3LdehUFs5P2kIKjIGorn5migwauyJGGTK6WShwa1qD9W6g4cFuM3kDGYaAUhk6WpLxGicFBVmLTS5dszW24LQHNOb1_r9JnQA)


### Le programme principale main.py
Le programme principale peut se diviser en partie distincte:
* Définition des fonctions
* Récupération des données et création de la DataFrame
* Nettoyage des données
* Initialisation des style CSS du DashBoard
* Création des graphiques plotly des des composents Dash
* Création du DashBoars

La création de la map utilise le module Nominatim. Le programme est disponible dans le fichier create_map.py. Neanmoins, le programme ne marche à chaque fois pour une raison inconnue. La map est donc déjà construite dans le fichier map.html et est utilisé dans le DashBoadrd. 
Vous pouvez lancer le programme avec la commande suivant:
```
$ python create_map.py
```
Si le programme fonctionne, la map crée ecrasera la map actuel et sera utilisé dans le DashBoard.

## Problème rencontré

