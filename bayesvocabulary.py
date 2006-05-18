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
from Globals import InitializeClass
from Products.CMFCore.utils import getToolByName

from Products.CPSSchemas.MethodVocabulary import MethodVocabulary
from Products.CPSSchemas.VocabulariesTool import VocabularyTypeRegistry
from Products.CPSSchemas.browser import BaseVocabularyAddView

class CPSBayesVocabulary(MethodVocabulary):

    meta_type = "CPS Bayes Vocabulary"

    _properties = (
        {'id': 'title', 'type': 'string', 'mode': 'w',
         'label': 'Title'},
        {'id': 'title_msgid', 'type': 'string', 'mode': 'w',
         'label': 'Title msgid'},
        {'id': 'description', 'type': 'text', 'mode': 'w',
         'label':'Description'},
        {'id': 'add_empty_key', 'type': 'boolean', 'mode': 'w',
         'label':'Add an empty key'},
        {'id': 'empty_key_pos', 'type': 'selection', 'mode': 'w',
         'select_variable': 'empty_key_pos_select',
         'label':'Empty key position'},
        {'id': 'empty_key_value', 'type': 'string', 'mode': 'w',
         'label':'Empty key value'},
        {'id': 'empty_key_value_i18n', 'type': 'string', 'mode': 'w',
         'label':'Empty key i18n value'},
        )

    def _getMethod(self):
        return self._getCategories

    def _getCategories(self, key=None, is_i18n=None):
        """ return categories for vocabulary """
        bayes_tool = getToolByName(self, 'portal_bayes')

        if key is not None:
            category = bayes_tool.getCategory(key)
            if category is None:
                if is_i18n is None:
                    return self.get(key)
                else:
                    return self.getMsgid(key)

            return category[0]

        categories = [(category['name'], category['label'])
                      for category in bayes_tool.getCategoryList()]
        categories.sort()
        return tuple(categories)

InitializeClass(CPSBayesVocabulary)
VocabularyTypeRegistry.register(CPSBayesVocabulary)

class BayesVocabularyAddView(BaseVocabularyAddView):
    """Add view for MethodVocabulary."""
    klass = CPSBayesVocabulary

