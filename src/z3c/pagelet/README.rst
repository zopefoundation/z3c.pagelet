========
Pagelets
========

.. contents::

This package provides a very flexible base implementation that can be used
to write view components which can be higly customized later in custom projects.
This is needed if you have to write reusable components like those needed
in a framework. Pagelets are BrowserPages made differently and can be used
to replace them.

What does this mean?

We separate the python view code from the template implementation. And we also
separate the template in at least two different templates - the content
template and the layout template.

This package uses z3c.template and offers an implementaton for this
template pattern. Additionaly this package offers a ``pagelet`` directive
wich can be used to register pagelets.

Pagelets are views which can be called and support the update and render
pattern.


How do they work
----------------

A pagelet returns the rendered content without layout in the render method and
returns the layout code if we call it. See also z3c.template which shows
how the template works. These samples will only show how the base implementation
located in the z3c.pagelet.browser module get used.


BrowserPagelet
--------------

The base implementation called BrowserPagelet offers builtin __call__ and
render methods which provide the different template lookups. Take a look at the
BrowserPagelet class located in z3c.pagelet.browser and you can see that the render
method returns a IContentTemplate and the __call__ method a ILayoutTemplate
defined in the z3c.layout package.

  >>> import os, tempfile
  >>> temp_dir = tempfile.mkdtemp()

  >>> import zope.interface
  >>> import zope.component
  >>> from z3c.pagelet import interfaces
  >>> from z3c.pagelet import browser

We start by defining a page template rendering the pagelet content.

  >>> contentTemplate = os.path.join(temp_dir, 'contentTemplate.pt')
  >>> with open(contentTemplate, 'w') as file:
  ...     _ = file.write('''
  ...   <div class="content">
  ...     my template content
  ...   </div>
  ... ''')

And we also define a layout template rendering the layout for a pagelet.
This template will call the render method from a pagelet:

  >>> layoutTemplate = os.path.join(temp_dir, 'layoutTemplate.pt')
  >>> with open(layoutTemplate, 'w') as file:
  ...     _ = file.write('''
  ...   <html>
  ...     <body>
  ...       <div class="layout" tal:content="structure view/render">
  ...         here comes the content
  ...       </div>
  ...     </body>
  ...   </html>
  ... ''')

Let's now register the template for the view and the request. We use the
TemplateFactory directly from the z3c.template package. This is commonly done
using the ZCML directive called ``z3c:template``. Note that we do use the
generic Interface as the view base interface to register the template. This
allows us to register a more specific template in the next sample:

  >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer
  >>> from z3c.template.interfaces import IContentTemplate
  >>> from z3c.template.template import TemplateFactory
  >>> factory = TemplateFactory(contentTemplate, 'text/html')
  >>> zope.component.provideAdapter(
  ...     factory, (zope.interface.Interface, IDefaultBrowserLayer),
  ...     IContentTemplate)

And register the layout template using the ``Interface`` as registration base:

  >>> from z3c.template.interfaces import ILayoutTemplate
  >>> factory = TemplateFactory(layoutTemplate, 'text/html')
  >>> zope.component.provideAdapter(factory,
  ...     (zope.interface.Interface, IDefaultBrowserLayer), ILayoutTemplate)

Now define a view marker interface. Such a marker interface is used to let
us register our templates:

  >>> class IMyView(zope.interface.Interface):
  ...     pass

And we define a view class inherited from BrowserPagelet and implementing the
view marker interface:

  >>> @zope.interface.implementer(IMyView)
  ... class MyView(browser.BrowserPagelet):
  ...     pass

Now test the view class providing the view and check the output:

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> myView = MyView(root, request)
  >>> print(myView())
  <html>
    <body>
      <div class="layout">
        <div class="content">
          my template content
        </div>
      </div>
    </body>
  </html>

You can see the render method generates only the content:

  >>> print(myView.render())
  <div class="content">
    my template content
  </div>


Redirection
-----------

The pagelet doesn't bother rendering itself and its layout when request is a
redirection as the rendering doesn't make any sense with browser requests in
that case. Let's create a view that does a redirection in its update method.

  >>> class RedirectingView(MyView):
  ...     def update(self):
  ...         self.request.response.redirect('.')

It will return an empty string when called as a browser page.

  >>> redirectRequest = TestRequest()
  >>> redirectView = RedirectingView(root, redirectRequest)
  >>> redirectView() == ''
  True

However, the ``render`` method will render pagelet's template as usual:

  >>> print(redirectView.render())
  <div class="content">
    my template content
  </div>


PageletRenderer
---------------

There is also a standard pattern for calling the render method on pagelet.
Using the pagelet renderer which is a IContentProvider makes it possible to
reuse existing layout template without the pagelet. If you want to reuse a
layout template without a pagelet you simply have to provide another content
provider. It's flexible isn't it? As next let's show a sample using the
pagelet renderer.

We define a new layout template using the content provider called ```pagelet``


  >>> providerLayout = os.path.join(temp_dir, 'providerLayout.pt')
  >>> with open(providerLayout, 'w') as file:
  ...     _ = file.write('''
  ...   <html>
  ...     <body>
  ...       <div class="layout" tal:content="structure provider:pagelet">
  ...         here comes the content
  ...       </div>
  ...     </body>
  ...   </html>
  ... ''')

and register them. Now we use the specific interface defined in the view:

  >>> factory = TemplateFactory(providerLayout, 'text/html')
  >>> zope.component.provideAdapter(factory,
  ...     (zope.interface.Interface, IDefaultBrowserLayer), ILayoutTemplate)

Now let's call the view:

  >>> try:
  ...     myView()
  ... except Exception as e:
  ...     print(repr(e))
  ContentProviderLookupError('pagelet'...)

That's right, we need to register the content provider ``pagelet`` before we
can use it.

  >>> from zope.contentprovider.interfaces import IContentProvider
  >>> from z3c.pagelet import provider
  >>> zope.component.provideAdapter(provider.PageletRenderer,
  ...     provides=IContentProvider, name='pagelet')

Now let's call the view again:

  >>> print(myView())
  <html>
    <body>
      <div class="layout">
        <div class="content">
          my template content
        </div>
      </div>
    </body>
  </html>


Context-specific templates
--------------------------

Pagelets are also able to lookup templates using their context object
as an additional discriminator, via (self, self.request, self.context)
lookup. It's useful when you want to provide a custom template for
some specific content objects. Let's check that out.

First, let's define a custom content type and make an object to work with:

  >>> class IContent(zope.interface.Interface):
  ...     pass
  >>> @zope.interface.implementer(IContent)
  ... class Content(object):
  ...     pass

  >>> content = Content()

Let's use our view class we defined earlier. Currently, it will use
the layout and content templates we defined for (view, request) before:

  >>> myView = MyView(content, request)
  >>> print(myView())
  <html>
    <body>
      <div class="layout">
        <div class="content">
          my template content
        </div>
      </div>
    </body>
  </html>

Let's create context-specific layout and content templates and register
them for our IContent interface:

  >>> contextLayoutTemplate = os.path.join(temp_dir, 'contextLayoutTemplate.pt')
  >>> with open(contextLayoutTemplate, 'w') as file:
  ...     _ = file.write('''
  ...   <html>
  ...     <body>
  ...       <div class="context-layout" tal:content="structure provider:pagelet">
  ...         here comes the context-specific content
  ...       </div>
  ...     </body>
  ...   </html>
  ... ''')
  >>> factory = TemplateFactory(contextLayoutTemplate, 'text/html')
  >>> zope.component.provideAdapter(
  ...     factory, (zope.interface.Interface, IDefaultBrowserLayer, IContent),
  ...     ILayoutTemplate)

  >>> contextContentTemplate = os.path.join(temp_dir, 'contextContentTemplate.pt')
  >>> with open(contextContentTemplate, 'w') as file:
  ...     _ = file.write('''
  ...   <div class="context-content">
  ...     my context-specific template content
  ...   </div>
  ... ''')
  >>> factory = TemplateFactory(contextContentTemplate, 'text/html')
  >>> zope.component.provideAdapter(
  ...     factory, (zope.interface.Interface, IDefaultBrowserLayer, IContent),
  ...     IContentTemplate)

Now, our view should use context-specific templates for rendering:

  >>> print(myView())
  <html>
    <body>
      <div class="context-layout">
        <div class="context-content">
          my context-specific template content
        </div>
      </div>
    </body>
  </html>


Add, Edit and Display forms (formlib)
-------------------------------------

What would the pagelet be without any formlib based implementations?
We offer base implementations for add, edit and display forms based on
the formlib. **Note:** To make sure these classes get defined, you
should have ``zope.formlib`` already installed, as ``z3c.pagelet``
does not directly depend on ``zope.formlib`` because there are other
form libraries.

For the next tests we provide a generic form template
like those used in formlib. This template is registered within this package
as a default for the formlib based mixin classes:

  >>> from z3c import pagelet
  >>> baseDir = os.path.split(pagelet.__file__)[0]
  >>> formTemplate = os.path.join(baseDir, 'form.pt')
  >>> factory = TemplateFactory(formTemplate, 'text/html')
  >>> zope.component.provideAdapter(
  ...     factory,
  ...     (interfaces.IPageletForm, IDefaultBrowserLayer), IContentTemplate)

And we define a new interface including a text attribute:

  >>> import zope.schema
  >>> class IDocument(zope.interface.Interface):
  ...     """A document."""
  ...     text = zope.schema.TextLine(title=u'Text', description=u'Text attr.')

Also define a content object which implements the interface:

  >>> @zope.interface.implementer(IDocument)
  ... class Document(object):
  ...     text = None
  >>> document = Document()

PageletAddForm
~~~~~~~~~~~~~~

Now let's define an add from based on the PageletAddForm class:

  >>> from zope.formlib import form
  >>> class MyAddForm(browser.PageletAddForm):
  ...     form_fields = form.Fields(IDocument)
  ...     def createAndAdd(self, data):
  ...         title = data.get('title', u'')
  ...         doc = Document()
  ...         doc.title = title
  ...         root['document'] = doc
  ...         return doc

Now render the form:

  >>> addForm = MyAddForm(root, request)
  >>> print(addForm())
  <html>
    <body>
      <div class="layout">
        <form action="http://127.0.0.1" method="post"
              enctype="multipart/form-data" class="edit-form"
              id="zc.page.browser_form">
          <table class="form-fields">
            <tr>
              <td class="label">
                <label for="form.text">
                <span class="required">*</span><span>Text</span>
                </label>
              </td>
              <td class="field">
                <div class="form-fields-help"
                     id="field-help-for-form.text">Text attr.</div>
                <div class="widget"><input class="textType" id="form.text"
                     name="form.text" size="20" type="text" value=""  /></div>
              </td>
            </tr>
          </table>
        <div class="form-controls">
          <input type="submit" id="form.actions.add" name="form.actions.add"
                 value="Add" class="button" />
        </div>
      </form>
    </div>
    </body>
  </html>


PageletEditForm
~~~~~~~~~~~~~~~

Now let's define an edit form based on the PageletEditForm class:

  >>> class MyEditForm(browser.PageletEditForm):
  ...     form_fields = form.Fields(IDocument)

and render the form:

  >>> document.text = u'foo'
  >>> editForm = MyEditForm(document, request)
  >>> print(editForm())
  <html>
    <body>
      <div class="layout">
        <form action="http://127.0.0.1" method="post"
              enctype="multipart/form-data" class="edit-form"
              id="zc.page.browser_form">
          <table class="form-fields">
              <tr>
                <td class="label">
                  <label for="form.text">
                  <span class="required">*</span><span>Text</span>
                  </label>
                </td>
                <td class="field">
                  <div class="form-fields-help"
                       id="field-help-for-form.text">Text attr.</div>
                  <div class="widget"><input class="textType" id="form.text"
                       name="form.text" size="20" type="text" value="foo"
                       /></div>
                </td>
              </tr>
          </table>
          <div class="form-controls">
            <input type="submit" id="form.actions.apply"
                   name="form.actions.apply" value="Apply" class="button" />
          </div>
        </form>
      </div>
    </body>
  </html>


PageletDisplayForm
~~~~~~~~~~~~~~~~~~

Now let's define a display form based on the PageletDisplayForm class...

  >>> class MyDisplayForm(browser.PageletDisplayForm):
  ...     form_fields = form.Fields(IDocument)

and render the form:

  >>> document.text = u'foo'
  >>> displayForm = MyDisplayForm(document, request)
  >>> print(displayForm())
  <html>
    <body>
      <div class="layout">
        <form action="http://127.0.0.1" method="post"
              enctype="multipart/form-data" class="edit-form"
              id="zc.page.browser_form">
          <table class="form-fields">
              <tr>
                <td class="label">
                  <label for="form.text">
                  <span>Text</span>
                  </label>
                </td>
                <td class="field">
                  <div class="form-fields-help"
                       id="field-help-for-form.text">Text attr.</div>
                  <div class="widget">foo</div>
                </td>
              </tr>
          </table>
        </form>
      </div>
    </body>
  </html>


Cleanup
-------

  >>> import shutil
  >>> shutil.rmtree(temp_dir)
