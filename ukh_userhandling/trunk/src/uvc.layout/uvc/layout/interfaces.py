# -*- coding: utf-8 -*-

from zope.interface import Interface


class IPageTop(Interface):
    """Marker For the area that sits at the top of the page.
    """


class IAboveContent(Interface):
    """Marker For the area that sits above the page body.
    """


class IBelowContent(Interface):
    """Marker For the area that sits under the page body.
    """


class IHeaders(Interface):
    """Marker For Headers
    """


class IToolbar(Interface):
    """Marker for Toolbar
    """


class IDocumentActions(Interface):
    """Marker for DocumentActions
    """


class IPersonalPreferences(Interface):
    """Marker for PersonalPreferences
    """


class IGlobalMenu(Interface):
    """Marker for GlobalMenu
    """


class IPersonalMenu(Interface):
    """Marker for PersonalMenu
    """


class ISidebar(Interface):
    """Marker for Sitebar
    """


class IFooter(Interface):
    """Marker for Footer
    """


class IPanels(Interface):
    """Marker interface for the panels display.
    """


class IHelp(Interface):
    """Marker for Help
    """


class IExtraInfo(Interface):
    """Marker for ExtraInfo in Forms
    """


class IExtraViews(Interface):
    """Marker for additional Views for Folders
       Objects etc...
    """
