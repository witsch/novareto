# -*- coding: utf-8 -*-
# Copyright (c) 2004-2009 novareto GmbH
# lwalther@novareto.de
from Products.CMFCore.utils import getToolByName

def setupView(portal, out):
    """ Add plone-views to folder types """

    typesTool = getToolByName(portal, 'portal_types')

    # install abc folder listing view for folders
    typefolder = typesTool['Folder']
    viewlist = typefolder.getProperty('view_methods', d=None)
    if 'wwwhandlungshilfe_view' not in viewlist:
        viewlist = viewlist + ('wwwhandlungshilfe_view',)
    if 'grundbetreuung_view' not in viewlist:
        viewlist = viewlist + ('grundbetreuung_view',)
    if 'spezifischebetreuung_view' not in viewlist:
        viewlist = viewlist + ('spezifischebetreuung_view',)
    typefolder.manage_changeProperties(view_methods = viewlist)
    out.append("Successfully installed novareto betreuungsmodell views for plone folder.")

    typedocument = typesTool['Document']
    viewlist = typedocument.getProperty('view_methods', d=None)
    if 'bsb_start_view' not in viewlist:
        viewlist = viewlist + ('bsb_start_view',)
    if 'bsb_final_view' not in viewlist:
        viewlist = viewlist + ('bsb_final_view',)
    typedocument.manage_changeProperties(view_methods = viewlist)
    out.append("Successfully installed Startseite betriebsspezifische Betreuung for plone document.")

def importBsBetreuungViews(context):
    """Miscellanous steps import handle """

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('nva.bsbetreuungviews.txt') is None:
        return

    out = []

    portal = context.getSite()

    setupView(portal, out)
    logger = context.getLogger("nva.bsbetreuung")

