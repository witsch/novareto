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
    filename="/tmp/order-%s.pdf" %obj.id
    try:
        to = obj.shipping_information.email 
        sMail(to=to,
	      sender="medienversand@bg-verkehr.de",
	      cc="cklinger@novareto.de",
	      subject="Neue Bestellung",
	      text="Sie haben bestellt ... ",
	       path=filename,
	       filename="order.pdf")
    except:
        pass
    sMail(to="christian.hanf@bg-verkehr.de",
          sender="medienversand@bg-verkehr.de",
          cc="cklinger@novareto.de",
          subject="Neue Bestellung",
          text="WAREN",
          path=filename,
          filename="order.pdf")
