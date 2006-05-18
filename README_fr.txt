CPSBayes
========
$Id$

CPSBayes fourni un outil de classification bayésien, basé sur BayesCore.

Stockage des données
--------------------

CPSBayes fourni un tool CMF appelé portal_bayes.

Ce tool permet de gérèr via la zmi une connection vers un backend sql
en fonction des bibliothèques installées (MySQL, PostgreSQL, SQLite)

La configuration de la connection se fait par URIs.

Exemples:

- Un backend MySQL: mysql://login:password@myhost/database_name
- Un backend postgresql: postgres://user@host/database?debug=&cache;=
- Un fichier SQLite: sqlite:///full/path/to/database

Un stockage ZODB est également fourni, sans aucune configuration requise.

Interface ZMI
-------------

La ZMI permet de gérer la connection et les catégories (liste, ajout,
suppression)

APIS fournies
-------------

CPSBayes fourni les APIs suivantes:

- getCategoryList() : liste des catégories
- addCategory(name, label='', description=''): ajout d'une catégorie
- delCategory(name) : suppression d'une catégorie
- learn(data, category): apprend au système à reconnaitre `data` pour la
  catégorie donnée
- guess(data): renvoie une séquence de tuples (categorie, probabilité),
  de la plus probalble à la moins probable, pour `data`.

Exemple d'utilisation
---------------------

Exemple (repris de Reverend)::

  >>> bayes_tool = self.portal.portal_bayes
  >>> bayes_tool.learn('le la les du un une je il elle de en', 'french')
  >>> bayes_tool.learn('der die das ein eine', 'german')
  >>> bayes_tool.learn('el uno una las de la en', 'spanish')
  >>> bayes_tool.learn('the rain in spain falls mainly on the plain', 'english')
  >>> bayes_tool.learn('the it she he they them are were to', 'english')
  >>> res = bayes_tool.guess('they went to el cantina')
  [('english', 0.9...), ('spanish', 0.9...)]
  >>> res = bayes_tool.guess('they were flying planes')
  [('english', 0.9...)]

