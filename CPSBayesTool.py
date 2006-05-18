# -*- encoding: iso-8859-15 -*-
# (C) Copyright 2006 Nuxeo SARL <http://nuxeo.com>
# Author: Tarek Ziadé <tz@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
# $Id$
from OFS.Folder import Folder
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import View
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from zope.interface import implements

from Products.BayesCore.storage import getStorage
from Products.BayesCore.tokenizer.filters import AllFilters
from Products.BayesCore.classifier.classifier import BayesClassifier

from interfaces import ICPSBayes

class CPSBayesTool(UniqueObject, Folder):
    """ CPSBayesTool presents BayesCore apis to a CPS portal
        and let the user configure the backend.
    """
    id = 'portal_bayes'
    meta_type = 'CPS Bayes Tool'
    security = ClassSecurityInfo()

    _propertiesBaseClass = Folder
    _properties = Folder._properties + \
        ({'id': 'max_guess_res', 'type': 'int', 'mode': 'w',
          'label': "Maximum number of results returned by guess()"},)


    backend_types = ('sql', 'zodb')
    backend_type = 'zodb'
    backend_parameters = ''
    max_guess_res = 3

    implements(ICPSBayes)

    #
    #  ZMI tabs
    #
    security.declareProtected(ManagePortal, 'manage_backend')
    manage_backend = PageTemplateFile('www/backend_manager.pt', globals())

    security.declareProtected(ManagePortal, 'manage_categories')
    manage_categories = PageTemplateFile('www/categories_manager.pt', globals())

    manage_options = (
            Folder.manage_options[:1] + (
            {'label': 'Backend managment', 'action':'manage_backend'},
            {'label': 'Categories managment', 'action':'manage_categories'}) +
            Folder.manage_options[1:])

    #
    # private apis
    #
    def _getBackend(self):
        if self.backend_type == 'zodb':
            # we are in charge of keeping the zodb storage in the tool
            if getattr(self, '_single', None) is None:
                # creating zodb storage
                storage = getStorage(self.backend_type,
                                     parameters=self.backend_parameters)
                # hooking it here
                self._single = storage
            return self._single

        # other kind of storages (sql, etc.) are just instances
        # that make a link to another backend
        return getStorage(self.backend_type,
                          parameters=self.backend_parameters)

    def _getClassifier(self, language='fr'):
        backend = self._getBackend()
        tokenizer = AllFilters()
        # XXXX hardcoded lang at this time
        # we will eventually provide lang feature,
        # wich exists in BayesCore later
        return BayesClassifier(language, backend, tokenizer)

    #
    # ZMI APIs
    #
    security.declareProtected(ManagePortal, 'manage_changeBackend')
    def manage_changeBackend(self, backend_type, backend_parameters,
                             REQUEST=None):
        """ changes the backend parameters:

            o backend_type: type of backend (zodb, sql, etc.)
            o backend_parameters: parameters, when a given type needs it
        """
        if self.backend_type != backend_type:
            self.backend_type = backend_type
        if self.backend_parameters != backend_parameters:
            self.backend_parameters = backend_parameters
        if REQUEST is not None:
            psm = 'Changes saved.'
            url = 'manage_backend?manage_tabs_message=%s' % psm
            REQUEST.RESPONSE.redirect(url)

    security.declareProtected(ManagePortal, 'manage_addCategory')
    def manage_addCategory(self, category, label='', description='', REQUEST=None):
        """ add a category within the ZMI
        """
        self.addCategory(category, label, description)
        if REQUEST is not None:
            psm = 'Category added.'
            url = 'manage_categories?manage_tabs_message=%s' % psm
            REQUEST.RESPONSE.redirect(url)

    security.declareProtected(ManagePortal, 'manage_addCategory')
    def manage_deleteCategories(self, categories, REQUEST=None):
        """ remove categories within the ZMI
        """
        for category in categories:
            self.delCategory(category)
        if REQUEST is not None:
            psm = 'Categories removed.'
            url = 'manage_categories?manage_tabs_message=%s' % psm
            REQUEST.RESPONSE.redirect(url)

    #
    # Tool APIs
    #
    security.declareProtected(View, 'getCategoryList')
    def getCategoryList(self):
        """ return list of categories """
        backend = self._getBackend()
        categories = backend.listCategories()
        # zpt-friendly structure
        def _mapit(element):
            result = {}
            result['name'] = element
            more = backend.getCategory(element)
            result['label'] = more[0]
            result['description'] = more[1]
            return result

        return [_mapit(category) for category in categories]

    # XXX will change permission later
    security.declareProtected(ManagePortal, 'addCategory')
    def addCategory(self, name, label='', description=''):
        """ add a category """
        name = name.replace(' ', '_').lower()
        backend = self._getBackend()
        backend.addCategory(name, label, description)

    # XXX will change permission later
    security.declareProtected(ManagePortal, 'delCategory')
    def delCategory(self, name):
        """ remove a category """
        backend = self._getBackend()
        backend.delCategory(name)

    security.declareProtected(View, 'getCategory')
    def getCategory(self, name):
        """ remove a category """
        backend = self._getBackend()
        return backend.getCategory(name)

    # XXX will change permission later
    security.declareProtected(ManagePortal, 'learn')
    def learn(self, data, category, language='fr'):
        """ learn

        XXX at this time data is a text
        but we need to implement adapters
        for document mappings
        """
        classifier = self._getClassifier(language)
        classifier.learn(data, category)

    # XXX will change permission later
    security.declareProtected(ManagePortal, 'learn')
    def unlearn(self, data, category, language='fr'):
        """ unlearn

        XXX at this time data is a text
        but we need to implement adapters
        for document mappings
        """
        classifier = self._getClassifier(language)
        classifier.unlearn(data, category)

    security.declareProtected(View, 'guess')
    def guess(self, data, language='fr'):
        """ guess

        XXX at this time data is a text
        but we need to implement adapters
        for document mappings
        """
        return self._getClassifier(language).guess(data)[:self.max_guess_res]

InitializeClass(CPSBayesTool)

def addCPSBayesTool(container, REQUEST=None, **kw):
    """Add a CPS Bayes Tool."""
    container = container.this() # For FactoryDispatcher.
    t = CPSBayesTool()
    id = t.getId()
    container._setObject(id, t)
    if REQUEST is not None:
        t = container._getOb(id)
        REQUEST.RESPONSE.redirect(t.absolute_url()+'/manage_overview')
