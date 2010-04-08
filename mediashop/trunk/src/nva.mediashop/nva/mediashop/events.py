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

    filename="/tmp/order-%s.pdf" %obj.id
   
    # Mail an Besteller
    try:
        to = obj.shipping_information.email 
        sMail(to=to,
	      sender="medienversand@bg-verkehr.de",
              cc="",
	      subject="Ihre Medienbestellung bei der BG Verkehr",
	      text="In der Anlage zu dieser E-Mail finden Sie das PDF-Dokument mit Ihrer Medienbestellung bei Ihrer BG-Verkehr. ",
	       path=filename,
	       filename="Bestellung.pdf")
    except:
        pass
    # Mail an  GSV GmbH
    sMail(to="christian.hanf@bg-verkehr.de",
          sender="medienversand@bg-verkehr.de",
          cc="",
          subject="Medienshop: Neue Bestellung",
          text=textmail,
          path=filename,
          filename="Bestellung.pdf")
