Functional Doctest
==================

:Test-Layer: functional

Setup
-----

Befor we can start to test the StandardLayout and the ViewletManagers
we have to setup a "kind of a" to access the layout with a TestRequest.

Here we create the Simple Site:

   >>> import grok
   >>> from grokcore.component.testing import grok_component
 
   >>> from zope.app.container import btree
   >>> class Uvcsite(grok.Application):
   ...     """Sample container."""
   ...     __name__ = u'container'


Here we create a simple View for this Site:

   >>> from megrok.layout import Page
   >>> class Index(Page):
   ...    grok.context(Uvcsite)
   ...    def render(self):
   ...        return "klaus"


   >>> grok_component('Index', Index)
   True

We persist the Site:

   >>> root = getRootFolder()
   >>> uvcsite = Uvcsite()
   >>> root['app'] = uvcsite

We made it a s Site
   
   >>> from zope.site.hooks import setSite
   >>> setSite(uvcsite)


The Layout
----------

Now we are able to access the Index View via the Site and a TestRequest

   >>> from zope.publisher.browser import TestRequest
   >>> from zope.component import getMultiAdapter

   >>> view = getMultiAdapter((uvcsite, TestRequest()), name="index")
   >>> view
   <uvc.layout.Index object at ...>
