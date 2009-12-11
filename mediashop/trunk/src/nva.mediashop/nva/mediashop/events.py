import five.grok as grok
from zope.app.container.interfaces import IObjectAddedEvent
from nva.mediashop.interfaces.artikel import IArtikel
from nva.plone.cart import IOrder
from nva.mediashop.pdf.pdfgenMS import createpdf
from nva.mediashop.pdf.utils import sMail 


def nN(v):
    if not v:
        return ''
    return v    


@grok.subscribe(IOrder, IObjectAddedEvent)
def printMessage(obj, event):
    si = obj.shipping_information
    artikel = []
    for item in obj.cart.itervalues():
        bestellung = {}
        bestellung['Anzahl'] = item.quantity
        bestellung['Artikel'] = item.title
        bestellung['Preis'] = item.price
        artikel.append(bestellung)
    daten = {}
    daten['Bestellung']  = artikel 
    daten['Mwst']        = 'zzgl. Versandkosten und gesetzl. MwSt.' 
    daten['VornameName'] = si.vorname + ' ' + si.name
    daten['Mitglnr']     = nN(si.mitgliedsnummer)
    daten['Firma']       = si.firma
    daten['Strasse']     = si.strasse
    daten['PlzOrt']      = si.plz + ' ' + si.ort
    daten['Telefon']     = nN(si.telefon)
    daten['Telefax']     = nN(si.telefax)
    daten['Email']       = si.email
    createpdf('/Users/cklinger/Desktop/order.pdf', daten)
    sMail(to="cklinger@novareto.de",
          sender="cklinger@novareto.de",
          cc="cklinger@novareto.de",
          subject="Neue Bestellung",
          text="WAREN",
          path="/Users/cklinger/Desktop/order.pdf",
          filename="order.pdf")
