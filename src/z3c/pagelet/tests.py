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
"""Tests
"""
import doctest
import itertools
import unittest

import zope.component
import zope.formlib.exception
import zope.formlib.interfaces
import zope.formlib.textwidgets
import zope.schema
import zope.traversing.adapters
from zope.configuration import xmlconfig
from zope.formlib import form
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.site.testing import siteSetUp
from zope.site.testing import siteTearDown

from z3c.pagelet import outputchecker


checker = outputchecker.OutputChecker(patterns=[])


def setUp(test):
    root = siteSetUp(True)
    test.globs['root'] = root

    zope.component.provideAdapter(
        zope.traversing.adapters.DefaultTraversable,
        [None],
    )

    # setup widgets
    zope.component.provideAdapter(
        zope.formlib.textwidgets.TextWidget,
        [zope.schema.interfaces.ITextLine, IBrowserRequest],
        zope.formlib.interfaces.IInputWidget)

    zope.component.provideAdapter(
        zope.formlib.exception.WidgetInputErrorView,
        [zope.formlib.interfaces.IWidgetInputError,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.formlib.interfaces.IWidgetInputErrorView,
    )
    zope.component.provideAdapter(
        zope.formlib.widget.UnicodeDisplayWidget,
        [zope.schema.interfaces.ITextLine,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.formlib.interfaces.IDisplayWidget,
    )
    zope.component.provideAdapter(form.render_submit_button, name='render')


def setUpZPT(test):
    setUp(test)

    # register provider TALES
    from zope.browserpage import metaconfigure
    from zope.contentprovider import tales
    metaconfigure.registerType('provider', tales.TALESProviderExpression)


def setUpZ3CPT(suite):
    setUp(suite)
    import z3c.pt
    import z3c.ptcompat
    xmlconfig.XMLConfig('configure.zcml', z3c.pt)()
    xmlconfig.XMLConfig('configure.zcml', z3c.ptcompat)()


def tearDown(test):
    siteTearDown()


def test_suite():
    flags = (
        doctest.NORMALIZE_WHITESPACE
        | doctest.ELLIPSIS
        | doctest.IGNORE_EXCEPTION_DETAIL
    )
    tests = ((
        doctest.DocFileSuite(
            'README.rst',
            setUp=setUp, tearDown=tearDown,
            optionflags=flags, checker=checker),
        doctest.DocFileSuite(
            'zcml.rst',
            setUp=setUp, tearDown=tearDown,
            optionflags=flags, checker=checker),
    ) for setUp in (setUpZPT, setUpZ3CPT, ))

    return unittest.TestSuite(itertools.chain(*tests))
