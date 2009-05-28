from Products.TextIndexNG3.adapters.cmf_adapters import CMFContentAdapter 
from textindexng.content import IndexContentCollector as ICC


class TNGWrapper(CMFContentAdapter):

     def indexableContent(self, fields):
         icc = ICC()
         if 'getId' in fields:
             self.addIdField(icc)
         if 'Title' in fields:
             self.addTitleField(icc)
         if 'Description' in fields:
             self.addDescriptionField(icc)
         if 'SearchableText' in fields:
             self.addSearchableTextField(icc)
         if 'searchdoczeichen' in fields:
             self.addSearchDocZeichen(icc)
         return icc

     def addSearchDocZeichen(self,icc):
         dzt = getattr(self.context, 'doczeichen', ['',]) 
	 dz = self._c('DOK '.join(dzt))
         icc.addContent('searchdoczeichen', dz, self.language)

