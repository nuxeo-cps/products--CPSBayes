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
#"
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
import unittest
from CPSBayesTestCase import CPSBayesTestCase
from Products.CPSBayes.bayesvocabulary import CPSBayesVocabulary

class FakeRequest:
    pass

class TestCPSBayesVocabulary(CPSBayesTestCase):

    def test_getCategories(self):
        bayes_tool = self.portal.portal_bayes
        bayes_tool.addCategory('My category', 'My Label', 'My description')

        vocab = self.portal.portal_vocabularies.cpsbayes_categories
        categories = vocab._getCategories()
        self.assertEquals(categories, (('my_category', 'My Label'),))

    def test_getCategory(self):
        bayes_tool = self.portal.portal_bayes
        bayes_tool.addCategory('My category', 'My Label', 'My description')

        vocab = self.portal.portal_vocabularies.cpsbayes_categories
        categories = vocab._getCategories(key='my_category')
        self.assertEquals(categories, 'My Label')

def test_suite():
    suites = [unittest.makeSuite(TestCPSBayesVocabulary)]
    return unittest.TestSuite(suites)

if __name__=="__main__":
    unittest.main(defaultTest='test_suite')
