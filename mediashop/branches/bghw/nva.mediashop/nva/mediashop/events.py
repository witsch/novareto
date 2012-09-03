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

    obj.asPDF()
    textmail = obj.asText()

    filename  = "/tmp/order-%s.pdf" %obj.id
    besteller = obj.shipping_information.email 
    if not besteller:
        besteller = 'bghwportal@bghw.de'  
 
    # Mail an Besteller
    try:
        to = obj.shipping_information.email 
        sMail(to=besteller,
	      sender="medien@bghw.de",
              cc="",
	      subject="Ihre Medienbestellung bei der BGHW",
	      text="In der Anlage zu dieser E-Mail finden Sie das PDF-Dokument mit Ihrer Medienbestellung bei der BGHW. ",
	       path=filename,
	       filename="Bestellung.pdf")
    except:
        pass

    sMail(to="medien@bghw.de",
          sender=besteller,
          cc="",
          subject="Medienshop: Neue Bestellung",
          text=textmail,
          path=filename,
          filename="Bestellung.pdf")
