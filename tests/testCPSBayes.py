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

class TestCPSBayesTool(CPSBayesTestCase):

    def testEmptyTool(self):
        bayes_tool = self.portal.portal_bayes
        self.assertEquals(bayes_tool.meta_type, 'CPS Bayes Tool')

    def test_manage_changeBackend(self):
        bayes_tool = self.portal.portal_bayes
        params = 'mysql://login:password@myhos/database_name'
        bayes_tool.manage_changeBackend('sql', params)
        self.assertEquals(bayes_tool.backend_type, 'sql')
        self.assertEquals(bayes_tool.backend_parameters, params)

    def test_getBackend(self):
        bayes_tool = self.portal.portal_bayes

        self.assertEquals(getattr(bayes_tool, '_single', None), None)
        bayes_tool.backend_type = 'zodb'

        # initial getter
        storage = bayes_tool._getBackend()
        self.assertNotEquals(getattr(bayes_tool, '_single', None), None)

        # next getter
        storage2 = bayes_tool._getBackend()
        self.assert_(storage2 is storage)

        # removing for next tests
        del bayes_tool._single

    def test_addRemoveCategory(self):
        bayes_tool = self.portal.portal_bayes
        bayes_tool.backend_type = 'zodb'
        bayes_tool.addCategory('les spam', 'Les spams', 'contient les spams')

        got = list(bayes_tool.getCategoryList())
        got = [element.items() for element in got]
        got.sort()

        wanted = [[('description', 'contient les spams'),
                   ('name', 'les_spam'), ('label', 'Les spams')]]

        self.assertEquals(got, wanted)

        bayes_tool.delCategory('les_spam')
        self.assertEquals(list(bayes_tool.getCategoryList()), [])

        bayes_tool.addCategory('les spam', 'Les spams', 'contient les spams')
        bayes_tool.addCategory('les spoum', 'Les spoums', 'sai mieu')
        bayes_tool.addCategory('les spims', 'Les spims', 'ca rockz')
        bayes_tool.manage_deleteCategories(['les_spam', 'les_spims'])

        wanted = [[('description', 'sai mieu'), ('name', 'les_spoum'),
                   ('label', 'Les spoums')]]

        got = list(bayes_tool.getCategoryList())
        got = [element.items() for element in got]
        got.sort()

        self.assertEquals(got, wanted)


    def test_learn_guess(self):
        bayes_tool = self.portal.portal_bayes
        bayes_tool.learn('le la les du un une je il elle de en', 'french')
        bayes_tool.learn('der die das ein eine', 'german')
        bayes_tool.learn('el uno una las de la en', 'spanish')
        bayes_tool.learn('the rain in spain falls mainly on the plain', 'english')
        bayes_tool.learn('the it she he they them are were to', 'english')

        res = bayes_tool.guess('they went to el cantina')
        self.assertEquals([cat for cat, prob in res],
                          ['english', 'spanish'])
        res = bayes_tool.guess('they were flying planes')
        self.assertEquals([cat for cat, prob in res],
                          ['english'])

        del_words = 'le la les du un une je il elle de en'
        bayes_tool.unlearn(del_words, 'french')
        got = list(bayes_tool.getCategoryList())
        got = [element.items() for element in got]
        got.sort()

        # XXX GR: according to warning in BayesCore.storage.zodb, method
        # delWordFromLanguage, it's normal behavior that the french category
        # hasn't been purged. But it should be empty
        wanted = [[('description', ''), ('name', 'english'), ('label', 'english')],
                  [('description', ''), ('name', 'french'), ('label', 'french')],
                  [('description', ''), ('name', 'german'), ('label', 'german')],
                  [('description', ''), ('name', 'spanish'), ('label', 'spanish')]]

        self.assertEquals(got, wanted)

        # checking that words got deleted
        # GR: language is another concept than category ('fr' by default)
        all_words = set(bayes_tool._getBackend().listWords(language='fr'))
        self.assertEquals(set(del_words.split()) & all_words, set(('de', 'en')))

        # checking that remaining words are associated to the spanish category
        res = bayes_tool.guess('en')
        self.assertEquals([cat for cat, prob in res],
                          ['spanish'])
        res = bayes_tool.guess('de')
        self.assertEquals([cat for cat, prob in res],
                          ['spanish'])

    def test_languages(self):
        # make sure we can work in several languages
        # categories stay multilingual
        # so 'spam' can be used for example over several
        # languages
        # the only interest in multilingualism
        # is the tokenizing.
        #
        # if the results are not good, we will
        # make categories for each languages
        bayes_tool = self.portal.portal_bayes
        bayes_tool.learn('bonjour comment va ?', 'nospam', 'fr')
        bayes_tool.learn("How ya'll doing over yanda big daddy ?",
                         'nospam', 'en')

        bayes_tool.learn('bonjour achète mes pilules', 'spam', 'fr')
        bayes_tool.learn("buy my pills big daddy", 'spam', 'en')

        res = bayes_tool.guess('achète mes belles montres', 'fr')
        self.assertEquals([cat for cat, prob in res], ['spam'])

        res = bayes_tool.guess('How are you doing?', 'en')
        self.assertEquals([cat for cat, prob in res], ['nospam'])

def test_suite():
    suites = [unittest.makeSuite(TestCPSBayesTool)]
    return unittest.TestSuite(suites)

if __name__=="__main__":
    unittest.main(defaultTest='test_suite')
