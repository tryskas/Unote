# UNOTE - Groupe 6 (Antropius - Ben Charnia - Carbon - Jabri - Ouidir - Oumaloul - Routier)

Projet de groupe ENSISA gestion absences et notes.
Lien du projet Github : [https://github.com/tryskas/Unote](https://github.com/tryskas/Unote)

## Attention

Ce projet est utilisable dans tous les navigateurs excepté Safari dû à un problème de compatibilité au niveau du CSS.

## Connexion

Pour vous connecter, un administrateur est disponible avec :
- **Identifiant**: 00000000
- **Mot de passe**: password123

À partir de cet administrateur, vous pouvez créer n'importe quel autre utilisateur.

Tous les autres comptes (00000001 à 00000008) utilisent le même mot de passe `password123` :
- 00000001 et 00000002 : Professeurs
- 00000003 et + : Étudiants

## Remarques concernant l'utilisation du site

- À la connexion, suivant son type (étudiant, professeur ou administrateur), l'utilisateur est renvoyé vers des pages différentes.
- La plupart des pages requièrent d'être connecté et sont restreintes à un type d'utilisateur en particulier. En cas de déconnexion, une page de connexion est donc d'abord présentée avant de rediriger, une fois connecté, vers la page demandée.
- Lorsqu'un utilisateur est créé par un administrateur, son identifiant et son mot de passe sont automatiquement créés puis envoyés au mail indiqué. L'administrateur n'a accès à aucun moment au mot de passe de l'utilisateur créé.
- Si vous créez toute une liste d'utilisateurs à partir d'un CSV, gardez ce fichier pour pouvoir tous les supprimer d'un coup une fois qu'ils n'étudient plus à l'école.
- En tant qu'étudiant ou professeur, les liens "Emploi du temps", "Absences" et "Notes" pour les élèves et "Emploi du temps", "Faire l'appel" et "Notes" pour les professeurs permettent d'accéder aux vues plus spécifiques correspondant à chacune des actions nommées. (Par exemple, la page principale des élèves affiche les 3 dernières notes reçues mais toutes sont consultables sur la page "Notes".)

Pour peupler la base de donnée en cas de destruction de celle-ci, nous joignons au projet un "script pour BDD". Pour l'utiliser, il faut effectuer la commande python manage.py shell au niveau du manage.py puis coller le contenu de ce fichier dans le shell.
Le dossier contient 2 csv permettant de créer des élèves et des groupes automatiquement.

## Lancer le serveur avec debug = false:

/ ! \ Prérequis : avoir installé un distributeur de fichiers statiques, ici whitenoise ( voir requirement.txt )

D'abord centraliser les fichiers statiques avec la commande :
- python manage.py collectstatic
Puis on lance le serveur :
- python manage.py runserver


## Connexion Github - Pycharm:

Pour utiliser Github avec Pycharm, suivez ces vidéos (dans le nouvel 
affichage Pycharm, le menu en haut à gauche s'obtient en cliquant sur les 4 
barres horizontales en haut à gauche de la fenêtre) :
- https://www.youtube.com/watch?v=cAnWazo5pFU pour connecter un projet 
  Github existant avec votre Pycharm.
- https://www.youtube.com/watch?v=8ZEssR8VTKo pour importer sur Github un 
  projet local que vous avez sur Pycharm.

Rmq : une fois le projet lié, soyez bien sûrs d'avoir ajouté un 
interpréteur Python puis installez les packages requis du fichier 
"requirements.txt" si Pycharm ne l'a pas déjà fait. (En ouvrant ce fichier, 
Pycharm vous proposera automatiquement de les installer.)

### Add

Si vous créez un nouveau fichier, qui n'était pas encore sur Github, il 
faut l'ajouter si vous voulez qu'il soit pris en compte dans votre prochain 
push. Pour cela :
1. Clic droit (dans l'arborescence) sur le dossier/fichier à ajouter
2. Clic sur "Git"
3. Clic sur "Add"

### Update project - Commit - Push

Une fois Github lié, un nouveau menu déroulant a dû apparaître en haut à 
gauche de Pycharm, à côté du nom du projet. Ce menu permet, entre autres, 
de récupérer une copie du projet sur Github (update), de commit et de push.

#### Commit et push

1. Dans le menu à gauche de la fenêtre, sélectionnez les fichiers à commit 
(ceux modifiés et ceux que vous avez ajoutés avec "Add"). 
2. Ajoutez un message dans la section en dessous.
3. Vous pouvez alors "Commit and Push" pour ajouter directement les 
   fichiers sur Github ou "Commit" pour vérifier le commit, faire d'autres 
   modifications etc... et push plus tard.
4. Vous trouverez alors, en cliquant sur l'icône en forme d'embranchement 
   en bas à gauche de Pycharm (à côté de l'icône pour accéder au terminal), 
   une section "git" contenant un historique des pushs déjà effectués et 
   l'éventuel commit en cours.
   Dans le dossier "local" (toujours au même endroit), vous pouvez, si vous 
   n'avez pas déjà push, faire un clic droit et push les changements.

#### Annuler un commit pas encore push

Vous pouvez aussi annuler le commit en faisant un clic droit sur l'élément 
précédent le commit dans l'historique des modifications puis "Reset Current 
Branch To Here" avec l'option "soft".

### Avant un commit

Si vous avez installé une nouvelle dépendance à une bibliothèque sur votre 
machine, pensez à mettre à jour le fichier "requirements.txt" en exécutant 
la commande `pip freeze > ./requirements.txt` au plus haut niveau.

## Éditer README.md

Par défaut, la vue Pycharm permet seulement la lecture des fichiers .md. 
Lorsqu'un fichier .md est ouvert, en haut à droite de la fenêtre se 
trouvent 3 boutons permettant de modifier la vue du fichier (preview seule, 
édition seule, édition + preview à côté).

## Pages Django utiles

Page du user management : https://docs.djangoproject.com/en/4.2/topics/auth/default/

Pour la création de vues en dérivant une des classes View : https://docs.djangoproject.com/en/4.2/ref/class-based-views/

Pour des exemples de dérivation de classes View : https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/#formview

Pour la création de formulaires en dérivant la classe ModelForm : https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/

Pour tout ce qui concerne le type User (et équivalents) : https://docs.djangoproject.com/en/4.2/ref/contrib/auth/
