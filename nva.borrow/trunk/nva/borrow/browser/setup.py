import os
from DateTime.DateTime import DateTime
from Products.Five.browser import BrowserView
from plone.namedfile import NamedImage

def makeNamedImage(filename):
    return NamedImage(file(os.path.join(os.path.dirname(__file__), 'data', filename), 'rb').read())

class Setup(BrowserView):

    def setupPFG(self, id_=None):
        """ Setup 'Bestellformular' as PFG instance """

        # fix allowed_content_types for FormFolder
        allowed = self.context.portal_types.FormFolder.allowed_content_types
        if not 'Dexterity Content Adapter' in allowed:
            self.context.portal_types.FormFolder.allowed_content_types = tuple(list(allowed) + ['Dexterity Content Adapter'])

        self.context.invokeFactory('Folder', id='buchungen', title='Buchungen')
        buchungen = self.context['buchungen']

        if not id_:
            id_ = 'bestellformular-%s' % DateTime().strftime('%Y%m%dT%H%M%S')
        if id_ in self.context.objectIds():
            self.context.manage_delObjects(id_)

        self.context.invokeFactory('FormFolder', id=id_, title='Bestellformular')
        form = self.context[id_]                                                    
        form.manage_delObjects(['replyto', 'topic', 'comments'])

        # content adapter
        form.invokeFactory('Dexterity Content Adapter', id='dexterity-adapter', title='Dexterity Adapter')
        adapter = form['dexterity-adapter']
        adapter.setCreatedType('nva.borrow.borrowrequest')
        adapter.setTargetFolder(buchungen)
        adapter.setFieldMapping([dict(form='vorname', content='firstName'),
                                 dict(form='nachname', content='lastName'),
                                 dict(form='adresse', content='address'),
                                 dict(form='plz', content='zip'),
                                 dict(form='stadt', content='city'),
                                 dict(form='telefon', content='phone'),
                                 dict(form='email', content='email'),
                                 dict(form='buchungStart', content='borrowFrom'),
                                 dict(form='buchungEnde', content='borrowTo'),
                                 dict(form='kommentar', content='comment'),
            ])

        form.invokeFactory('FormStringField', id='vorname', title='Vorname', required=True)
        form.invokeFactory('FormStringField', id='nachname', title='Nachname', required=True)
        form.invokeFactory('FormStringField', id='adresse', title='Adresse', required=True)
        form.invokeFactory('FormStringField', id='plz', title='Postleitzahl')
        form.invokeFactory('FormStringField', id='stadt', title='Stadt')
        form.invokeFactory('FormStringField', id='telefon', title='Telefon')
        form.invokeFactory('FormStringField', id='email', title='E-Mail Adresse')
        form.invokeFactory('FormStringField', id='mitgliedsnr', title='Mitgliedsnummer')
        form.invokeFactory('FormDateField', id='buchungStart', title='Buchen von', required=True)
        form.invokeFactory('FormDateField', id='buchungEnde', title='Buchen bis', required=True)
        form.invokeFactory('FormTextField', id='kommentar', title='Kommentar')

        self.request.response.redirect(form.absolute_url())

    def demo(self):

        if 'aktionsmittel-demo' in self.context.contentIds():
            self.context.manage_delObjects('aktionsmittel-demo')

        self.context.invokeFactory('Folder', id='aktionsmittel-demo', title='Aktionsmittel Demo')
        demo = self.context['aktionsmittel-demo']

        demo.restrictedTraverse('@@setupPFG')()

        demo.invokeFactory('nva.borrow.borrowableitems', id='sicherheit-druckmaschinen', title='Sicherheit bei Druckmaschinen')
        druck = demo['sicherheit-druckmaschinen']
        druck.image = makeNamedImage('druckmaschine.png')

        demo.invokeFactory('nva.borrow.borrowableitems', id='sicherheit-atomkraftwerk', title='Sicherheit in Atomkraftwerken')
        atom = demo['sicherheit-atomkraftwerk']
        atom.image = makeNamedImage('atom.png')

        self.request.response.redirect(demo.absolute_url())


    def createBookingRequest(self):

        form_folder = self.context.portal_catalog(portal_type='FormFolder')[0].getObject()
        self.request.response.redirect(form_folder.absolute_url())
