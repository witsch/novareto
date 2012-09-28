from Products.CMFCore.utils import getToolByName

def setupView(portal, out):
    """ Add plone-views to folder types """

    typesTool = getToolByName(portal, 'portal_types')

    typedocument = typesTool['Document']
    viewlist = typedocument.getProperty('view_methods', d=None)
    if 'documentgallery_view' not in viewlist:
        viewlist = viewlist + ('documentgallery_view',)
    typedocument.manage_changeProperties(view_methods = viewlist)

    out.append("Successfully installed novareto galleryview")

def importVarious(context):
    """Miscellanous steps import handle """

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('nva.galleryview_various.txt') is None:
        return
    out = []
    portal = context.getSite()
    setupView(portal, out)
    logger = context.getLogger("nva.galleryview")
