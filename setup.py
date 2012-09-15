##############################################################################
#
# Copyright (c) 2007-2009 Zope Foundation and Contributors.
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
"""Setup

$Id$
"""
import os
import xml.sax.saxutils
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.3.2.dev0'

setup(
    name='z3c.pagelet',
    version=version,
    author = "Roger Ineichen and the Zope Community",
    author_email = "zope-dev@zope.org",
    description = "Pagelets are way to specify a template without the O-wrap.",
    long_description=(
        read('README.txt')
        + '\n\n' +
        read('src', 'z3c', 'pagelet', 'README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    license = "ZPL 2.1",
    keywords = "zope3 template pagelet layout zpt pagetemplate",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
    url = 'http://pypi.python.org/pypi/z3c.pagelet',
    packages = find_packages('src'),
    package_dir = {'':'src'},
    namespace_packages = ['z3c'],
    extras_require = dict(
        test = [
            'zope.app.testing',
            'zope.app.form',
            'zope.testing',
            'zope.traversing',
            'lxml>=2.1.1',
            'z3c.pt >= 2.1',
            'z3c.ptcompat>=1.0',
            'zope.formlib',
            ],
        chameleon = [
            'z3c.pt >= 2.1',
            'z3c.ptcompat',
            ],
        docs = [
            'z3c.recipe.sphinxdoc'
            ],
        ),
    install_requires = [
        'setuptools',
        'z3c.template>=1.2.0',
         # TODO: this is only needed for ZCML directives, so can copy
        'zope.browserpage', # things we use from there and get rid of the dependencies.
        'zope.component>=3.7.0',
        'zope.configuration',
        'zope.contentprovider',
        'zope.interface',
        'zope.publisher',
        'zope.schema',
        'zope.security',
        ],
    include_package_data = True,
    zip_safe = False,
    )
