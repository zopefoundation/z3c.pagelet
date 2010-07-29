##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
"""Pagelet mixin classes

$Id$
"""
__docformat__ = 'restructuredtext'

import zope.interface
import zope.component
from zope.publisher import browser

from z3c.template.interfaces import ILayoutTemplate, IContentTemplate
from z3c.pagelet import interfaces

REDIRECT_STATUS_CODES = (301, 302, 303)

# default pagelet base implementation
class BrowserPagelet(browser.BrowserPage):
    """Content generating pagelet with layout template support."""

    zope.interface.implements(interfaces.IPagelet)

    template = None
    layout = None

    def update(self):
        pass

    def render(self):
        # render content template
        if self.template is None:
            template = zope.component.queryMultiAdapter(
                (self, self.request, self.context), IContentTemplate)
            if template is None:
                template = zope.component.getMultiAdapter(
                    (self, self.request), IContentTemplate)
            return template(self)
        return self.template()

    def __call__(self):
        """Calls update and returns the layout template which calls render."""
        self.update()

        if self.request.response.getStatus() in REDIRECT_STATUS_CODES:
            # don't bother rendering when redirecting
            return ''

        if self.layout is None:
            layout = zope.component.queryMultiAdapter(
                (self, self.request, self.context), ILayoutTemplate)
            if layout is None:
                layout = zope.component.getMultiAdapter(
                    (self, self.request), ILayoutTemplate)
            return layout(self)
        return self.layout()

try:
    from zope.formlib import form
except ImportError:
    pass
else:
    # formlib based pagelet mixin classes
    class PageletForm(form.FormBase, BrowserPagelet):
        """Fomr mixin for pagelet implementations."""

        zope.interface.implements(interfaces.IPageletForm)

        template = None
        layout = None

        __init__ = BrowserPagelet.__init__

        __call__ = BrowserPagelet.__call__

        def render(self):
            # if the form has been updated, it will already have a result
            if self.form_result is None:
                if self.form_reset:
                    # we reset, in case data has changed in a way that
                    # causes the widgets to have different data
                    self.resetForm()
                    self.form_reset = False
                if self.template is None:
                    template = zope.component.queryMultiAdapter(
                        (self, self.request, self.context), IContentTemplate)
                    if template is None:
                        template = zope.component.getMultiAdapter(
                            (self, self.request), IContentTemplate)
                    self.form_result = template(self)
                else:
                    self.form_result = self.template()

            return self.form_result


    class PageletAddForm(PageletForm, form.AddFormBase):
        """Add form mixin for pagelet implementations."""

        zope.interface.implements(interfaces.IPageletAddForm)

        def render(self):
            if self._finished_add:
                self.request.response.redirect(self.nextURL())
                return ""
            # render content template
            if self.template is None:
                template = zope.component.queryMultiAdapter(
                    (self, self.request, self.context), IContentTemplate)
                if template is None:
                    template = zope.component.getMultiAdapter(
                        (self, self.request), IContentTemplate)
                return template(self)
            return self.template()


    class PageletEditForm(PageletForm, form.EditFormBase):
        """Edit form mixin for pagelet implementations."""

        zope.interface.implements(interfaces.IPageletEditForm)


    class PageletDisplayForm(PageletForm, form.DisplayFormBase):
        """Display fomr mixin for pagelet implementations."""

        zope.interface.implements(interfaces.IPageletDisplayForm)
