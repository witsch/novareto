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
    pass
    #sMail(to="cklinger@novareto.de",
    #      sender="cklinger@novareto.de",
    #      cc="cklinger@novareto.de",
    #      subject="Neue Bestellung",
    #      text="WAREN",
    #      path="/Users/cklinger/Desktop/order.pdf",
    #      filename="order.pdf")
