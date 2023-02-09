##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Pagelet Content Providers
"""
import zope.component
import zope.interface
import zope.publisher.interfaces.http

import z3c.pagelet.interfaces


@zope.interface.implementer(z3c.pagelet.interfaces.IPageletRenderer)
class PageletRenderer:
    """Render the adapted pagelet."""

    zope.component.adapts(zope.interface.Interface,
                          zope.publisher.interfaces.http.IHTTPRequest,
                          z3c.pagelet.interfaces.IPagelet)

    def __init__(self, context, request, pagelet):
        self.__updated = False
        self.__parent__ = pagelet
        self.context = context
        self.request = request

    def update(self):
        pass

    def render(self):
        return self.__parent__.render()
