from Products.CMFCore.DirectoryView import registerDirectory

GLOBALS = globals()
registerDirectory('cmf_fsdirectory_view', GLOBALS)


from nva.mediashop.browser.interfaces import IMediashopLayer
