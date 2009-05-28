import pysqlite2.dbapi2 as sqlite
from string import split, strip, replace 

conn = sqlite.connect('dz.db')
cursor = conn.cursor()

i=1
for x in open('docz.txt','r').readlines()[1:]:
    if not x.startswith('\t\r\n'): 
        dz, bez = split(strip(x),'\t')
        dz = replace(dz,'.','')
	sp1 = sp2 = sp3 = rest = "-"
	if len(dz) == 1:
           sp1 = dz[0]
	elif len(dz) == 2:
           sp1 = dz[0]
           sp2 = dz[1]
	if len(dz) == 3:
           sp1 = dz[0]
           sp2 = dz[1]
           sp3 = dz[2]
	if len(dz) > 3:
           sp1 = dz[0]
           sp2 = dz[1]
           sp3 = dz[2]
	   rest = dz[3:]
        sql = "insert into doczeichen (sp1,sp2,sp3,rest,bez) values ('%s', '%s', '%s', '%s', '%s')" %(sp1, sp2, sp3, rest, bez)
	i+=1
        try:
            cursor.execute(sql)
	except:
            print x
conn.commit()
print conn
