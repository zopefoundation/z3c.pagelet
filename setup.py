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
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


tests_require = [
    'zope.formlib',
    'zope.site',
    'zope.testing',
    'zope.traversing',
    'lxml',
    'z3c.pt >= 2.1',
    'z3c.ptcompat >= 1.0',
]


setup(
    name='z3c.pagelet',
    version='2.0.0',
    author="Roger Ineichen and the Zope Community",
    author_email="zope-dev@zope.org",
    description="Pagelets are way to specify a template without the O-wrap.",
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('src', 'z3c', 'pagelet', 'README.rst')
        + '\n\n' +
        read('CHANGES.rst')
    ),
    license="ZPL 2.1",
    keywords="zope3 template pagelet layout zpt pagetemplate",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
    url='http://pypi.python.org/pypi/z3c.pagelet',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    extras_require=dict(
        test=tests_require,
        chameleon=[
            'z3c.pt >= 2.1',
            'z3c.ptcompat',
        ],
        forms=[
            'zope.formlib'
        ],
        docs=[
            'z3c.recipe.sphinxdoc'
        ],
    ),
    install_requires=[
        'setuptools',
        'z3c.template>=1.2.0',
        'zope.browserpage',
        'zope.component>=3.7.0',
        'zope.configuration',
        'zope.contentprovider',
        'zope.interface',
        'zope.publisher',
        'zope.schema',
        'zope.security',
    ],
    tests_require=tests_require,
    test_suite='z3c.pagelet.tests.test_suite',
    include_package_data=True,
    zip_safe=False,
)
