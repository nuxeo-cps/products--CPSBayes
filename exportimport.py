# -*- encoding: iso-8859-15 -*-
# (C) Copyright 2006 Nuxeo SAS <http://nuxeo.com>
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
""" CPSBayes XML Adapter.
"""
from Acquisition import aq_base
from zope.component import adapts
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import ObjectManagerHelpers
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.interfaces import ISetupEnviron

from Products.CPSBayes.interfaces import ICPSBayes

_marker = object()

TOOL = 'portal_bayes'
NAME = 'cpsbayes'

def exportCPSBayes(context):
    """Export user folder configuration as a set of XML files.

    Does not export the users themselves.
    """
    site = context.getSite()
    if getattr(aq_base(site), TOOL, None) is None:
        logger = context.getLogger(NAME)
        logger.info("Nothing to export.")
        return
    tool = getToolByName(site, TOOL)
    exportObjects(tool, '', context)

def importCPSBayes(context):
    """Import user folder configuration from XML files.
    """
    site = context.getSite()
    if getattr(aq_base(site), TOOL, None) is None:
        logger = context.getLogger(NAME)
        logger.info("Cannot import into missing acl_users.")
        return
    tool = getToolByName(site, TOOL)
    importObjects(tool, '', context)


class CPSBayesXMLAdapter(XMLAdapterBase, ObjectManagerHelpers):
    """XML importer and exporter for Standard User Folder.
    """

    adapts(ICPSBayes, ISetupEnviron)
    implements(IBody)

    _LOGGER_ID = NAME
    name = NAME

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        node.appendChild(self._extractCPSBayesProperties())
        self._logger.info("CPSBayes exported.")
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        meta_type = str(node.getAttribute('meta_type'))
        if meta_type != self.context.meta_type:
            self._logger.error("Cannot import %r into %r." %
                               (meta_type, self.context.meta_type))
            return
        if self.environ.shouldPurge():
            self._purgeCPSBayesProperties()
        self._initCPSBayesProperties(node)
        self._logger.info("CPSBayes imported.")

    node = property(_exportNode, _importNode)
    elements = ('backend_type', 'backend_parameters')

    def _extractCPSBayesProperties(self):
        portal_bayes = self.context
        fragment = self._doc.createDocumentFragment()

        for element in self.elements:
            child = self._doc.createElement('property')
            child.setAttribute('name', element)
            value = getattr(portal_bayes, element)
            text = self._doc.createTextNode(str(value))
            child.appendChild(text)
            fragment.appendChild(child)
        return fragment

    def _purgeCPSBayesProperties(self):
        return

    def _initCPSBayesProperties(self, node):
        portal_bayes = self.context

        for child in node.childNodes:
            if child.nodeName != 'property':
                continue
            name = child.getAttribute('name')
            value = self._getNodeText(child)
            if name in self.elements:
                setattr(portal_bayes, name, value)
