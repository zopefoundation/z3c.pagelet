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
"""
$Id$
"""
__docformat__ = "reStructuredText"

import unittest
import itertools

import zope.component
import zope.schema
import zope.traversing.adapters
import zope.app.form.interfaces
import zope.app.form.browser
import zope.app.form.browser.exception
import zope.app.form.browser.interfaces
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite
from zope.app.form.interfaces import IInputWidget
from zope.app.testing import setup
from zope.formlib import form
from zope.configuration import xmlconfig

import z3c.pt.compat.testing

def setUp(test):
    root = setup.placefulSetUp(site=True)
    test.globs['root'] = root

    zope.component.provideAdapter(
        zope.traversing.adapters.DefaultTraversable,
        [None],
        )

    # setup widgets
    zope.component.provideAdapter(zope.app.form.browser.TextWidget,
        [zope.schema.interfaces.ITextLine, IBrowserRequest],
        IInputWidget)

    zope.component.provideAdapter(
        zope.app.form.browser.exception.WidgetInputErrorView,
        [zope.app.form.interfaces.IWidgetInputError,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.app.form.browser.interfaces.IWidgetInputErrorView,
        )
    zope.component.provideAdapter(
        zope.app.form.browser.UnicodeDisplayWidget,
        [zope.schema.interfaces.ITextLine,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.app.form.interfaces.IDisplayWidget,
        )
    zope.component.provideAdapter(form.render_submit_button, name='render')

def setUpZPT(test):
    z3c.pt.compat.config.disable()
    setUp(test)

    # register provider TALES
    from zope.app.pagetemplate import metaconfigure
    from zope.contentprovider import tales
    metaconfigure.registerType('provider', tales.TALESProviderExpression)

def setUpZ3CPT(suite):
    z3c.pt.compat.config.enable()
    setUp(suite)
    xmlconfig.XMLConfig('configure.zcml', z3c.pt)()

def tearDown(test):
    setup.placefulTearDown()

def test_suite():
    checker = z3c.pt.compat.testing.OutputChecker()
    
    tests = ((
        DocFileSuite('README.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            checker=checker,
            ),
        DocFileSuite('zcml.txt', setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ) for setUp in (setUpZPT, setUpZ3CPT, ))

    return unittest.TestSuite(itertools.chain(*tests))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
