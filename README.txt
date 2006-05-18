CPSBayes
========
$Id$

CPSBayes is a tool to perform naive bayesian inference based on the BayesCore
package.

Data storage
------------

CPSBayes provides a CMF tool that holds the connection parameters to an
external SQL storage server (MySQL, PostgreSQL or SQLite).

Sample setups:

- MySQL: mysql://login:password@myhost/database_name
- PostgreSQL: postgres://user@host/database?debug=&cache;=
- SQLite: sqlite:///full/path/to/database

A ZODB storage is also provided and requires no external adapter nor setup.

ZMI screen
-----------

Two ZMI tabs are provided:

 - storage setup
 - categories definitions (listing, adding, deleting)

API
---

The CPSBayes tool defines the following methods:

- getCategoryList() : list existing categories
- addCategory(name, label='', description=''): add a new category
- delCategory(name) : delete a category
- learn(data, category): learn to guess `category` for the given `data`
- guess(data): return a sorted list of tuple (category_name, probability)

Sample usage
------------

Example (from Reverend)::

  >>> bayes_tool = self.portal.portal_bayes
  >>> bayes_tool.learn('le la les du un une je il elle de en', 'french')
  >>> bayes_tool.learn('der die das ein eine', 'german')
  >>> bayes_tool.learn('el uno una las de la en', 'spanish')
  >>> bayes_tool.learn('the rain in spain falls mainly on the plain', 'english')
  >>> bayes_tool.learn('the it she he they them are were to', 'english')
  >>> res = bayes_tool.guess('they went to el cantina')
  [('english', 0.9..), ('spanish', 0.9..)]
  >>> res = bayes_tool.guess('they were flying planes')
  [('english', 0.9..)]

