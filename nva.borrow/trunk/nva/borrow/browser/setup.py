import os
import loremipsum
from random import randrange
import urllib2
from DateTime.DateTime import DateTime
from Products.Five.browser import BrowserView
from plone.namedfile import NamedImage
from plone.app.textfield.value import RichTextValue

def makeNamedImage(filename, data=None):
    return NamedImage(file(os.path.join(os.path.dirname(__file__), 'data', filename), 'rb').read())

def makeNamedImageFromData(data=None):
    return NamedImage(data)

def _invokeFactory(context, portal_type, id, **kw):
    context.invokeFactory(portal_type, id=id, **kw)
    obj = context[id]
    if not 'title' in kw:
        obj.title = gen_sentence(80)
    if not 'description' in kw:
        obj.description = gen_sentences(2)

    if obj.portal_type in ('nva.borrow.borrowableitems', 'nva.borrow.borrowableitem'):
        if not 'text' in kw:
            obj.text = RichTextValue(gen_sentences(20), 'text/plain', 'text/html')

    try:
        obj.portal_workflow.doActionFor(obj, 'publish')
    except:
        pass
    return obj

def gen_sentence(max_words=None):
    text = loremipsum.Generator().generate_sentence()[-1]
    if max_words:
        return u' '.join(text.split(' ')[:max_words])
    return text

def random_image(width, height):
    url = 'http://lorempixel.com/%d/%d/' % (width, height)
    return urllib2.urlopen(url).read()


def gen_sentences(length=80):
    return u' '.join([s[2] for s in loremipsum.Generator().generate_sentences(length)])


class Setup(BrowserView):

    def setupPFG(self, id_=None):
        """ Setup 'Bestellformular' as PFG instance """

        # fix allowed_content_types for FormFolder
        allowed = self.context.portal_types.FormFolder.allowed_content_types
        if not 'Dexterity Content Adapter' in allowed:
            self.context.portal_types.FormFolder.allowed_content_types = tuple(list(allowed) + ['Dexterity Content Adapter'])

        buchungen = _invokeFactory(self.context, 'Folder', id='buchungen', title='Buchungen')

        if not id_:
            id_ = 'bestellformular-%s' % DateTime().strftime('%Y%m%dT%H%M%S')
        if id_ in self.context.objectIds():
            self.context.manage_delObjects(id_)

        form = _invokeFactory(self.context, 'FormFolder', id=id_, title='Bestellformular')
        form.manage_delObjects(['replyto', 'topic', 'comments'])

        # content adapter
        adapter = _invokeFactory(form, 'Dexterity Content Adapter', id='dexterity-adapter', title='Dexterity Adapter')
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

        _invokeFactory(form, 'FormStringField', id='vorname', title='Vorname', required=True)
        _invokeFactory(form, 'FormStringField', id='nachname', title='Nachname', required=True)
        _invokeFactory(form, 'FormStringField', id='adresse', title='Adresse', required=True)
        _invokeFactory(form, 'FormStringField', id='plz', title='Postleitzahl', required=True)
        _invokeFactory(form, 'FormStringField', id='stadt', title='Stadt', required=True)
        _invokeFactory(form, 'FormStringField', id='telefon', title='Telefon')
        _invokeFactory(form, 'FormStringField', id='email', title='E-Mail Adresse')
        _invokeFactory(form, 'FormStringField', id='mitgliedsnr', title='Mitgliedsnummer', required=True)
        booked_items = _invokeFactory(form, 'FormDataGridField', id='buchungen', title='Buchungen', required=True)
        booked_items.setColumnDefs([
            {'columnDefault': '0', 'columnType': 'String', 'columnVocab': '', 'columnId': 'numberItems', 'columnTitle': 'Anzahl'},
            {'columnDefault': '', 'columnType': 'SelectVocabulary', 'columnVocab': ['@@getData'], 'columnId': 'itemId', 'columnTitle': 'ID des zu buchenden Objekts'},
            ])

        _invokeFactory(form, 'FormDateField', id='buchungStart', title='Buchen von', required=True)
        _invokeFactory(form, 'FormDateField', id='buchungEnde', title='Buchen bis', required=True)
        _invokeFactory(form, 'FormTextField', id='kommentar', title='Kommentar')

        self.request.response.redirect(form.absolute_url())

    def demo(self):

        if 'aktionsmittel-demo' in self.context.contentIds():
            self.context.manage_delObjects('aktionsmittel-demo')

        demo = _invokeFactory(self.context, 'Folder', id='aktionsmittel-demo', title='Aktionsmittel Demo')

        demo.restrictedTraverse('@@setupPFG')()

        druck = _invokeFactory(demo, 'nva.borrow.borrowableitems', id='sicherheit-druckmaschinen', title='Sicherheit bei Druckmaschinen')
        druck.image = makeNamedImage('druckmaschine.png')
        druck.individualItemBooking = True
        for i in range (3):
            item = _invokeFactory(druck, 'nva.borrow.borrowableitem', str(i))
            item.image = makeNamedImageFromData(random_image(200, 200))
            item.itemsAvailable = randrange(1, 5)

        atom = _invokeFactory(demo, 'nva.borrow.borrowableitems', id='sicherheit-atomkraftwerk', title='Sicherheit in Atomkraftwerken')
        atom.image = makeNamedImage('atom.png')
        atom.individualItemBooking = False
        for i in range (3):
            item = _invokeFactory(atom, 'nva.borrow.borrowableitem', str(i))
            item.image = makeNamedImageFromData(random_image(200, 200))
            item.itemsAvailable = randrange(1, 5)

        self.request.response.redirect(demo.absolute_url())


    def createBookingRequest(self):

        form_folder = self.context.portal_catalog(portal_type='FormFolder')[0].getObject()
        self.request.response.redirect(form_folder.absolute_url())
