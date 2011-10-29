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

import re
import unittest
import itertools
import doctest

import lxml.etree
import lxml.doctestcompare

import zope.component
import zope.schema
import zope.traversing.adapters
import zope.app.form.interfaces
import zope.app.form.browser
import zope.app.form.browser.exception
import zope.app.form.browser.interfaces
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.form.interfaces import IInputWidget
from zope.app.testing import setup
from zope.formlib import form
from zope.configuration import xmlconfig


class OutputChecker(lxml.doctestcompare.LHTMLOutputChecker):
    """Doctest output checker which is better equippied to identify
    HTML markup than the checker from the ``lxml.doctestcompare``
    module. It also uses the text comparison function from the
    built-in ``doctest`` module to allow the use of ellipsis."""

    _repr_re = re.compile(r"^<([A-Z]|[^>]+ (at|object) |[a-z]+ \'[A-Za-z0-9_.]+\'>)")

    def __init__(self, doctest=doctest):
        self.doctest = doctest
        # make sure these optionflags are registered
        doctest.register_optionflag('PARSE_HTML')
        doctest.register_optionflag('PARSE_XML')
        doctest.register_optionflag('NOPARSE_MARKUP')

    def _looks_like_markup(self, s):
        s = s.replace('<BLANKLINE>', '\n').strip()
        return (s.startswith('<')
                and not self._repr_re.search(s))

    def text_compare(self, want, got, strip):
        if want is None: want = ""
        if got is None: got = ""
        checker = self.doctest.OutputChecker()
        return checker.check_output(
            want, got, self.doctest.ELLIPSIS|self.doctest.NORMALIZE_WHITESPACE)

    def get_parser(self, want, got, optionflags):
        NOPARSE_MARKUP = self.doctest.OPTIONFLAGS_BY_NAME.get(
            "NOPARSE_MARKUP", 0)
        PARSE_HTML = self.doctest.OPTIONFLAGS_BY_NAME.get(
            "PARSE_HTML", 0)
        PARSE_XML = self.doctest.OPTIONFLAGS_BY_NAME.get(
            "PARSE_XML", 0)
        parser = None
        if NOPARSE_MARKUP & optionflags:
            return None
        if PARSE_HTML & optionflags:
            parser = lxml.doctestcompare.html_fromstring
        elif PARSE_XML & optionflags:
            parser = lxml.etree.XML
        elif (want.strip().lower().startswith('<html')
              and got.strip().startswith('<html')):
            parser = lxml.doctestcompare.html_fromstring
        elif (self._looks_like_markup(want)
              and self._looks_like_markup(got)):
            parser = self.get_default_parser()
        return parser


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
    setup.placefulTearDown()

def test_suite():
    checker = OutputChecker()

    tests = ((
        doctest.DocFileSuite('README.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            checker=checker,
            ),
        doctest.DocFileSuite('zcml.txt', setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ) for setUp in (setUpZPT, setUpZ3CPT, ))

    return unittest.TestSuite(itertools.chain(*tests))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
