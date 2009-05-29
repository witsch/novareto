from zope.interface import implements
from nva.docplone.interfaces import IDocZeichenUtility
import pysqlite2.dbapi2 as sqlite
from string import split, strip, replace 
from nva.docplone import messagedomain as _

pfad = '/'.join(__file__.split('/')[:-1])+"/dz.db"


class DocZeichenUtility(object):
    implements(IDocZeichenUtility)

    def pointing(self, bz):
        """Setzt immer nach 3 Ziffern einen Trennpunkt in die DOK-Zahl"""
        count=3
        ret=''
        for i in bz:
            if count == 0:
                ret=ret+'.'+i
                count=2
            else:
                ret=ret+i
                count=count-1
        return ret

    def execute(self, sql):
        """Ausfuehrung des SQL-Selects fuer DOC-Zahlen"""
        conn = sqlite.connect(pfad)
        cursor = conn.cursor()
	cursor.execute(sql)
	res = cursor.fetchall()
        cursor.close()
	rc=[('',_(u'bitte auswaehlen'))]
	for x in res:
            bez = x[4]
            bz=""
            #nur mit mit dem Slice [0:4] kommen mehr als 3 Ziffern mit
	    #for y in x[0:3]:
	    for y in x[0:4]:
                if y != '-':
                   bz+=y
            #Formatierung der DOC-Zahl
            bz=self.pointing(bz)
	    bez = "( %s ) %s" %(bz, bez[:60])
            rc.append(( bz, bez[:60] ))
	return rc

    def execute1(self, sql):
        """Ausfuehrung des SQL-Selects fuer Anhaengezahlen und -Begriffe"""
        conn = sqlite.connect(pfad)
        cursor = conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        rc=[('',_(u'bitte auswaehlen'))]
        for x in res:
            bz= x[0]
            bez = x[1]
#            bz=self.pointing(bz)
            bez = "( %s ) %s" %(bz, bez[:60])
            rc.append(( bz, bez[:60] ))
        return rc

    def getHG(self):
        sql = "select * from doczeichen where sp2 = '-' and sp3 = '-'"
        return self.execute(sql)

    def getOG(self, v1):
        sql = "select * from doczeichen where sp3 = '-' and sp1 = '%s'" %(v1)
        return self.execute(sql)

    def getG(self, v1, v2):
	print v1, v2
        sql = "select * from doczeichen where sp1 = '%s' and sp2 = '%s' and sp3 != '-'" %(v1,v2)
        return self.execute(sql)

    def getRest(self, v1, v2, v3):
        sql = "select * from doczeichen where sp1 = '%s' and sp2 = '%s' and sp3 = '%s'" %(v1,v2,v3)
        return self.execute(sql)

    def getAnhangzahlen(self):
	sql = "select * from anhangzahlen"
        return self.execute1(sql)

    def getAnhangbegriffe(self):
	sql = "select * from anhangbegriff"
        return self.execute1(sql)
