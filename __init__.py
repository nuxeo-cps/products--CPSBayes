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
# $Id$
from AccessControl.Permissions import add_user_folders as AddUserFolders

from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

from Products.CPSCore.interfaces import ICPSSite

from bayesvocabulary import CPSBayesVocabulary
import CPSBayesTool

def initialize(registrar):

    registrar.registerClass(
        CPSBayesTool.CPSBayesTool,
        permission=AddUserFolders,
        constructors=(CPSBayesTool.addCPSBayesTool,))


    profile_registry.registerProfile('default',
                                     'CPSBayes',
                                     "Profile for CPSBayes.",
                                     'profiles/default',
                                     'CPSBayes',
                                     EXTENSION,
                                     for_=ICPSSite)
