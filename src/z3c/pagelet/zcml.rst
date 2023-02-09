=================
Pagelet directive
=================

Show how we can use the pagelet directive. Register the meta configuration for
the directive.

  >>> import sys
  >>> from zope.configuration import xmlconfig
  >>> import z3c.pagelet
  >>> context = xmlconfig.file('meta.zcml', z3c.pagelet)

We need also a custom pagelet class:

  >>> from z3c.pagelet.browser import BrowserPagelet
  >>> class MyPagelet(BrowserPagelet):
  ...     """Custom pagelet"""

Make them available under the fake package ``custom``:

  >>> sys.modules['custom'] = type(
  ...     'Module', (),
  ...     {'MyPagelet': MyPagelet})()

To register a pagelet we need a class:

  >>> context = xmlconfig.string("""
  ... <configure
  ...     xmlns:z3c="http://namespaces.zope.org/z3c">
  ...   <z3c:pagelet
  ...       name="index.html"
  ...       permission="zope.Public"
  ...       />
  ... </configure>
  ... """, context)
  Traceback (most recent call last):
  ...
  ConfigurationError: Missing parameter: 'class'
  File "<string>", line 4.2-7.8

And we also need an interface implementing zope.interface.intefaces.IInterface:

  >>> class NonInterface(object):
  ...     """Non compliant interface."""
  >>> sys.modules['custom'].NonInterface = NonInterface
  >>> context = xmlconfig.string("""
  ... <configure
  ...     xmlns:z3c="http://namespaces.zope.org/z3c">
  ...   <z3c:pagelet
  ...       name="index.html"
  ...       class="custom.MyPagelet"
  ...       permission="zope.Public"
  ...       provides="custom.NonInterface"
  ...       />
  ... </configure>
  ... """, context)
  Traceback (most recent call last):
  ...
  ConfigurationError: Invalid value for 'provides'
  File "<string>", line 4.2-9.8
  zope.schema._bootstrapinterfaces.NotAnInterface:


Register a pagelet within the directive with minimal attributes:

  >>> context = xmlconfig.string("""
  ... <configure
  ...     xmlns:z3c="http://namespaces.zope.org/z3c">
  ...   <z3c:pagelet
  ...       name="index.html"
  ...       class="custom.MyPagelet"
  ...       permission="zope.Public"
  ...       />
  ... </configure>
  ... """, context)

Let's get the pagelet

  >>> import zope.component
  >>> from zope.publisher.browser import TestRequest
  >>> pagelet = zope.component.queryMultiAdapter((object(), TestRequest()),
  ...     name='index.html')

and check them:

  >>> pagelet
  <z3c.pagelet.zcml.MyPagelet object at ...>

  >>> pagelet.context
  <object object at ...>

Register the pagelet with a different name and more attributes provided from
the directive. We also use a custom attribute called label here. Let's define
some more components...

  >>> class SecondPagelet(BrowserPagelet):
  ...     label = ''

  >>> import zope.interface
  >>> class IContent(zope.interface.Interface):
  ...     """Content interface."""
  >>> @zope.interface.implementer(IContent)
  ... class Content(object):
  ...     pass

register the new classes in the custom module...

  >>> sys.modules['custom'].IContent = IContent
  >>> sys.modules['custom'].Content = Content
  >>> sys.modules['custom'].SecondPagelet = SecondPagelet

and use them in the directive:

  >>> context = xmlconfig.string("""
  ... <configure
  ...     xmlns:z3c="http://namespaces.zope.org/z3c">
  ...   <z3c:pagelet
  ...       name="custom.html"
  ...       class="custom.SecondPagelet"
  ...       for="custom.IContent"
  ...       permission="zope.Public"
  ...       label="my Label"
  ...       />
  ... </configure>
  ... """, context)

Get the pagelet for the new content object

  >>> import zope.component
  >>> pagelet = zope.component.queryMultiAdapter((Content(), TestRequest()),
  ...     name='custom.html')

and check them:

  >>> pagelet
  <z3c.pagelet.zcml.SecondPagelet object at ...>

  >>> pagelet.label
  'my Label'

We also can provide another interface then the IPagelet within the directive.
Such a interface must be inherited from IPagelet.

  >>> class NewPagelet(BrowserPagelet):
  ...     """New pagelet"""
  >>> sys.modules['custom'] = type(
  ...     'Module', (),
  ...     {'NewPagelet': NewPagelet})()

Now register the pagelet within a interface which isn't inherited from IPagelet.

  >>> context = xmlconfig.string("""
  ... <configure
  ...     xmlns:z3c="http://namespaces.zope.org/z3c">
  ...   <z3c:pagelet
  ...       name="new.html"
  ...       class="custom.NewPagelet"
  ...       permission="zope.Public"
  ...       provides="zope.interface.Interface"
  ...       />
  ... </configure>
  ... """, context)
  Traceback (most recent call last):
  ...
  ConfigurationError: Provides interface must inherit IPagelet.
  File "<string>", line 4.2-9.8

If we use a correct interface, we can register the pagelet:

  >>> from z3c.pagelet import interfaces
  >>> class INewPagelet(interfaces.IPagelet):
  ...     """New pagelet interface."""
  >>> sys.modules['custom'] = type(
  ...     'Module', (),
  ...     {'INewPagelet': INewPagelet, 'NewPagelet': NewPagelet})()

  >>> context = xmlconfig.string("""
  ... <configure
  ...     xmlns:z3c="http://namespaces.zope.org/z3c">
  ...   <z3c:pagelet
  ...       name="new.html"
  ...       class="custom.NewPagelet"
  ...       permission="zope.Public"
  ...       provides="custom.INewPagelet"
  ...       />
  ... </configure>
  ... """, context)

And if we get the pagelet, we can see that the object provides the new
pagelet interface:

  >>> pagelet = zope.component.queryMultiAdapter((object(), TestRequest()),
  ...     name='new.html')
  >>> pagelet
  <z3c.pagelet.zcml.NewPagelet object at ...>

  >>> INewPagelet.providedBy(pagelet)
  True

Register a pagelet for a layer:

  >>> class SkinnedPagelet(BrowserPagelet):
  ...     """Custom pagelet"""

  >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer
  >>> class IMyPageletLayer(IDefaultBrowserLayer):
  ...     """Custom layer"""

  >>> sys.modules['custom'] = type(
  ...     'Module', (),
  ...     {'SkinnedPagelet': SkinnedPagelet,
  ...      'IMyPageletLayer': IMyPageletLayer})()

  >>> context = xmlconfig.string("""
  ... <configure
  ...     xmlns:z3c="http://namespaces.zope.org/z3c">
  ...   <z3c:pagelet
  ...       name="skinned.html"
  ...       layer="custom.IMyPageletLayer"
  ...       class="custom.SkinnedPagelet"
  ...       permission="zope.Public"
  ...       />
  ... </configure>
  ... """, context)


  >>> from zope.publisher.skinnable import applySkin
  >>> req = TestRequest()
  >>> applySkin(req, IMyPageletLayer)
  >>> pagelet = zope.component.queryMultiAdapter((object(), req),
  ...     name='skinned.html')

and check them:

  >>> pagelet
  <z3c.pagelet.zcml.SkinnedPagelet object at ...>

  >>> pagelet.context
  <object object at ...>



Cleanup
--------

Now we need to clean up the custom module.

  >>> del sys.modules['custom']
