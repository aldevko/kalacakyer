import sqlite3 as sql
apprreq = 2
apreeq = sql.connect('kalacakyer.db')
introcursor = apreeq.cursor()
introcursor.row_factory = sql.Row
introappsel = introcursor.execute(f"SELECT * FROM kalacakyer WHERE id = {apprreq} ").fetchall()
"""apreeq.commit()
userid = introappsel[0]
username = introappsel[1]
usercount = introappsel[2]
userphon = introappsel[3]
userloc = introappsel[4]

print(userid)"""

ttlcount = []
totalcount = introcursor.execute("SELECT countof FROM kabulet").fetchall()
for i in totalcount:
    ttlcount.extend(i)
sumcount = [i for i in ttlcount]
countt = 0

for i in sumcount:
    countt += i

print(countt)
