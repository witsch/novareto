from Products.CMFCore.utils import getToolByName

def setupView(portal, out):
    """ Add plone-views to folder types """

    typesTool = getToolByName(portal, 'portal_types')

    typefolder = typesTool['Fernlehrgang']
    viewlist = typefolder.getProperty('view_methods', d=None)
    if 'flgdesktop' not in viewlist:
        viewlist = viewlist + ('flgdesktop',)
    typefolder.manage_changeProperties(view_methods = viewlist)

    out.append("Successfully installed novareto download")

def importVarious(context):
    """Miscellanous steps import handle """

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('nva.flgdesktop_various.txt') is None:
        return

    out = []

    portal = context.getSite()

    setupView(portal, out)
    logger = context.getLogger("nva.download")

