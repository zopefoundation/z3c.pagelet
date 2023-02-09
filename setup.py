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

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


tests_require = [
    'zope.formlib',
    'zope.site',
    'zope.testing',
    'zope.testrunner',
    'zope.traversing',
    'lxml',
    'z3c.pt >= 2.1',
    'z3c.ptcompat >= 1.0',
]


setup(
    name='z3c.pagelet',
    version='3.0',
    author="Roger Ineichen and the Zope Community",
    author_email="zope-dev@zope.dev",
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3',
    ],
    url='https://github.com/zopefoundation/z3c.pagelet',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    python_requires='>=3.7',
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
    include_package_data=True,
    zip_safe=False,
)
