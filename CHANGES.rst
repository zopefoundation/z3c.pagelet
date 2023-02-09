=======
CHANGES
=======

3.0 (2023-02-09)
----------------

- Drop support for Python 2.7, 3.4, 3.5, 3.6.

- Add support for Python 3.8, 3.9, 3.10, 3.11.


2.1 (2018-11-12)
----------------

- Claim support for Python 3.5, 3.6, 3.7, PyPy and PyPy3.

- Drop support for Python 2.6 and 3.3.

- Drop support for ``python setup.py test``.


2.0.0 (2015-11-09)
------------------

- Standardize namespace __init__.

- Claim support for Python 3.4.


2.0.0a1 (2013-02-28)
--------------------

- Added support for Python 3.3.

- Replaced deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Dropped support for Python 2.4 and 2.5.


1.3.1 (2012-09-15)
------------------

- Fix ``IPageletDirective`` after a change in
  ``zope.component.zcml.IBasicViewInformation``


1.3.0 (2011-10-29)
------------------

- Moved z3c.pt include to extras_require chameleon. This makes the package
  independent from chameleon and friends and allows to include this
  dependencies in your own project.

- Upgrade to chameleon 2.0 template engine and use the newest z3c.pt and
  z3c.ptcompat packages adjusted to work with chameleon 2.0.

  See the notes from the z3c.ptcompat package:

  Update z3c.ptcompat implementation to use component-based template engine
  configuration, plugging directly into the Zope Toolkit framework.

  The z3c.ptcompat package no longer provides template classes, or ZCML
  directives; you should import directly from the ZTK codebase.

  Note that the ``PREFER_Z3C_PT`` environment option has been
  rendered obsolete; instead, this is now managed via component
  configuration.

  Also note that the chameleon CHAMELEON_CACHE environment value changed from
  True/False to a path. Skip this property if you don't like to use a cache.
  None or False defined in buildout environment section doesn't work. At least
  with chameleon <= 2.5.4

  Attention: You need to include the configure.zcml file from z3c.ptcompat
  for enable the z3c.pt template engine. The configure.zcml will plugin the
  template engine. Also remove any custom built hooks which will import
  z3c.ptcompat in your tests or other places.


1.2.2 (2011-08-18)
------------------

- Change request interface in pagelet adapter signature e.g.
  (context, request, pagelet). Switch from IBrowserRequest to IHTTPRequest.
  This allows to use the pagelet pattern for jsonrpc request which doesn't
  provide IBrowserRequest. Also reflect the changes in configure.zcml


1.2.1 (2010-07-29)
------------------

- ``zope.app.pagetemplate.metaconfigure.registerType`` was moved to
  ``zope.browserpage``, so it gets now imported from there.

- Dropped test dependency on ``zope.app.security``, it is no longer
  needed.

- Using python's ``doctest`` instead of deprecated
  ``zope.testing.doctest[unit]``.


1.2.0 (2009-08-27)
------------------

- Fix untrusted redirect to google.com in tests. It's now forbidden by default
  by newer zope.publisher versions.

- Change ``zope.app.publisher`` dependency to new ``zope.browserpage``, as it
  has much less dependencies.

1.1.0 (2009-05-28)
------------------

* Got rid of dependency on ``zope.app.component`` by requiring
  ``zope.component >= 3.7``.

* Removed hard dependency on ``zope.formlib``: the pagelet forms now
  only get defined when ``zope.formlib`` is available. Tests still
  depend on ``zope.formlib``, so it got a test dependency.

* Made sure long_description renders fine on pypi.


1.0.3 (2009-02-27)
------------------

* Allow use of ``z3c.pt`` using ``z3c.ptcompat`` compatibility layer.

* Add support for context-specific layout and content template lookup,
  using (view, request, context) discriminator. This is compatible with
  context-specific templates introduced in z3c.template 1.2.0.

* Don't do rendering in pagelet's __call__ method when request is a redirection.

* Add sphinx-based HTML documentation building part to the buildout.


1.0.2 (2008-01-21)
------------------

* Added a `form.zcml` which can be included to have a template for
  ``PageletAddForm``, ``PageletEditForm`` and ``PageletDisplayForm``.


1.0.1 (2007-10-08)
------------------

* Added ``update()`` and ``render()`` method to ``IPagelet`` which was
  not specified but used.

* Fixed a infinite recursion bug when a layout template was registered for "*"
  but no content template was registered for a pagelet.
