#!/usr/bin/python
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
#
from Testing import ZopeTestCase
from Products.CPSDefault.tests.CPSTestCase import CPSTestCase, MANAGER_ID

ZopeTestCase.installProduct('CPSBayes')

class CPSBayesTestCase(CPSTestCase):

    def afterSetUp(self):
        CPSTestCase.afterSetUp(self)
        self.login(MANAGER_ID)

        if 'portal_bayes' not in self.portal.objectIds():
            factory = self.portal.manage_addProduct['CPSBayes']
            factory.addCPSBayesTool()

        vocabs = self.portal.portal_vocabularies

        if 'cpsbayes_categories' not in vocabs.objectIds():
            from Products.CPSBayes.bayesvocabulary import CPSBayesVocabulary
            vocab = CPSBayesVocabulary('cpsbayes_categories')
            vocabs._setObject('cpsbayes_categories', vocab)

        self.logout()
