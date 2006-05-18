CPSBayes
========
$Id$

CPSBayes fourni un outil de classification bay�sien, bas� sur BayesCore.

Stockage des donn�es
--------------------

CPSBayes fourni un tool CMF appel� portal_bayes.

Ce tool permet de g�r�r via la zmi une connection vers un backend sql
en fonction des biblioth�ques install�es (MySQL, PostgreSQL, SQLite)

La configuration de la connection se fait par URIs.

Exemples:

- Un backend MySQL: mysql://login:password@myhost/database_name
- Un backend postgresql: postgres://user@host/database?debug=&cache;=
- Un fichier SQLite: sqlite:///full/path/to/database

Un stockage ZODB est �galement fourni, sans aucune configuration requise.

Interface ZMI
-------------

La ZMI permet de g�rer la connection et les cat�gories (liste, ajout,
suppression)

APIS fournies
-------------

CPSBayes fourni les APIs suivantes:

- getCategoryList() : liste des cat�gories
- addCategory(name, label='', description=''): ajout d'une cat�gorie
- delCategory(name) : suppression d'une cat�gorie
- learn(data, category): apprend au syst�me � reconnaitre `data` pour la
  cat�gorie donn�e
- guess(data): renvoie une s�quence de tuples (categorie, probabilit�),
  de la plus probalble � la moins probable, pour `data`.

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

