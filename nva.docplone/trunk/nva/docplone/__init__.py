#
from Products.CMFCore.DirectoryView import registerDirectory
from zope.i18nmessageid import MessageFactory
messagedomain = MessageFactory('nva.docplone')


GLOBALS = globals()
registerDirectory('skins', GLOBALS)

def initialize(context):
    """Intializer called when used as a Zope 2 product."""
