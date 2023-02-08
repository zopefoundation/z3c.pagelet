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
"""ZCML Directives
"""
import zope.component
import zope.component.zcml
import zope.configuration.fields
import zope.interface
import zope.schema
import zope.security.checker
import zope.security.zcml
from zope.browserpage import metaconfigure as viewmeta
from zope.configuration.exceptions import ConfigurationError
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from z3c.pagelet import browser
from z3c.pagelet import interfaces


class IPageletDirective(zope.component.zcml.IBasicViewInformation):
    """A directive to register a new pagelet.

    The pagelet directive also supports an undefined set of keyword arguments
    that are set as attributes on the pagelet after creation.
    """

    name = zope.schema.TextLine(
        title="The name of the pagelet.",
        description="The name shows up in URLs/paths. For example 'foo'.",
        required=True)

    class_ = zope.configuration.fields.GlobalObject(
        title="Class",
        description="A class that provides attributes used by the pagelet.",
        required=True,
    )

    permission = zope.security.zcml.Permission(
        title="Permission",
        description="The permission needed to use the pagelet.",
        required=True
    )

    layer = zope.configuration.fields.GlobalObject(
        title="The request interface or class this pagelet is for.",
        description=(
            "Defaults to"
            " zope.publisher.interfaces.browser.IDefaultBrowserLayer."),
        required=False
    )

    for_ = zope.configuration.fields.GlobalObject(
        title="Context",
        description="The content interface or class this pagelet is for.",
        required=False
    )

    provides = zope.configuration.fields.GlobalInterface(
        title="The interface this pagelets provides.",
        description="""
        A pagelet can provide an interface.  This would be used for
        views that support other views.""",
        required=False,
        default=interfaces.IPagelet,
    )


# Arbitrary keys and values are allowed to be passed to the pagelet.
IPageletDirective.setTaggedValue('keyword_arguments', True)


# pagelet directive
def pageletDirective(
        _context, class_, name, permission, for_=zope.interface.Interface,
        layer=IDefaultBrowserLayer, provides=interfaces.IPagelet,
        allowed_interface=None, allowed_attributes=None, **kwargs):

    # Security map dictionary
    required = {}

    # Get the permission; mainly to correctly handle CheckerPublic.
    permission = viewmeta._handle_permission(_context, permission)

    ifaces = list(zope.interface.Declaration(provides).flattened())
    if interfaces.IPagelet not in ifaces:
        raise ConfigurationError("Provides interface must inherit IPagelet.")

    # Build a new class that we can use different permission settings if we
    # use the class more then once.
    cdict = {}
    cdict['__name__'] = name
    cdict.update(kwargs)
    new_class = type(class_.__name__, (class_, browser.BrowserPagelet), cdict)

    # Set up permission mapping for various accessible attributes
    viewmeta._handle_allowed_interface(
        _context, allowed_interface, permission, required)
    viewmeta._handle_allowed_attributes(
        _context, allowed_attributes, permission, required)
    viewmeta._handle_allowed_attributes(
        _context, kwargs.keys(), permission, required)
    viewmeta._handle_allowed_attributes(
        _context, ('__call__', 'browserDefault', 'update', 'render',
                   'publishTraverse'), permission, required)

    # Register the interfaces.
    viewmeta._handle_for(_context, for_)

    # provide the custom provides interface if not allready provided
    if not provides.implementedBy(new_class):
        zope.interface.classImplements(new_class, provides)

    # Create the security checker for the new class
    zope.security.checker.defineChecker(
        new_class,
        zope.security.checker.Checker(required))

    # register pagelet
    _context.action(
        discriminator=('pagelet', for_, layer, name),
        callable=zope.component.zcml.handler,
        args=('registerAdapter',
              new_class, (for_, layer), provides, name, _context.info),)
