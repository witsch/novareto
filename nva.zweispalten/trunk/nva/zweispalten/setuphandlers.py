from Products.CMFCore.utils import getToolByName

def setupView(portal, out):
    """ Add plone-views to folder types """

    typesTool = getToolByName(portal, 'portal_types')

    # install abc folder listing view for folders
    typefolder = typesTool['Folder']
    viewlist = typefolder.getProperty('view_methods', d=None)
    if 'zweispalten_view' not in viewlist:
        viewlist = viewlist + ('zweispalten_view',)
    typefolder.manage_changeProperties(view_methods = viewlist)

    typetopic = typesTool['Topic']
    viewlist = typetopic.getProperty('view_methods', d=None)
    if 'zweispalten_view' not in viewlist:
        viewlist = viewlist + ('zweispalten_view',)
    typetopic.manage_changeProperties(view_methods = viewlist)

    out.append("Successfully installed nva.zweispalten")

def importVarious(context):
    """Miscellanous steps import handle """

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('nva.zweispalten_various.txt') is None:
        return

    out = []
    portal = context.getSite()
    setupView(portal, out)
    logger = context.getLogger("nva.zweispalten")
