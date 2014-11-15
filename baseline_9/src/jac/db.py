'''
Created on Nov 2, 2014

@author: Adrian
'''
import sys
import csv, pyodbc
import pprint


def fetch_bcpao_by_parcel_id(cur, twp, rng, sec, sub, blk, lot):
    rows = cur.execute("SELECT TaxAcct, SiteHouseNo, SiteStreetname, SiteType, SiteDir, SiteAptNo, SiteCity, SiteZip5 FROM Property WHERE Twp=? AND Rng=? AND Sec=? AND Sub=? AND Blk=? AND Lot=?", twp, rng, sec, sub, blk, lot).fetchall()
#     rows = cur.execute(SQL).fetchall()
    pprint.pprint(rows)

def main():
    print('hi')
    # set up some constants
    MDB = 'C:/Users/Adrian/Downloads/Web97/web97 - Copy.mdb'; DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = 'pw'
    
    # connect to db
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()
    
    # run a query and get the results 
#     SQL = 'SELECT * FROM Property where LegalDescLine1 like '+"'LT 14 BLK 3 PB 19 PG 58 MARLIN SUBD S 05 T 25 R 36 SUBID 52'"+' ;' # your query goes here
#     print(SQL)
    ld = 'LT 14 BLK 3 PB 19 PG 58 MARLIN SUBD S 05 T 25 R 36 SUBID 52'
    ld = 'LOT 14 BLK 3'
#     ld = 'E 1/2 OF SW 1/4 OF TRACT 1 BLK 6'
    sql='SELECT TaxAcct, LegalDescLine1, LegalDescLine2, LegalDescLine3 FROM Property WHERE LegalDescLine1 LIKE ?'
    sql='SELECT * FROM Property WHERE LegalDescLine1 LIKE ?'
    ld = '2504233'
    sql='SELECT * FROM Property WHERE TaxAcct LIKE ?'
#     args=[ld]
#     rows = cur.execute(sql,(ld+'%')).fetchall()

#     fetch_bcpao_by_parcel_id(cur, twp='26', rng='37', sec='31', sub='OL', blk='1', lot='21')
#     fetch_bcpao_by_parcel_id(cur, twp='27', rng='36', sec='36', sub='25', blk='4', lot='104')
#     fetch_bcpao_by_parcel_id(cur, twp='28', rng='37', sec='25', sub='FO', blk='83', lot='20')
#     fetch_bcpao_by_parcel_id(cur, twp='26', rng='36', sec='16', sub='RF', blk='D', lot='16')
#     fetch_bcpao_by_parcel_id(cur, twp='28', rng='37', sec='33', sub=None, blk=None, lot='6')
#     fetch_bcpao_by_parcel_id(cur, twp='24', rng='37', sec='14', sub='84', blk='', lot='286')
#     fetch_bcpao_by_parcel_id(cur, twp='24', rng='37', sec='14', sub='84', blk=None, lot='286')
    rows = cur.execute("SELECT TaxAcct, SiteHouseNo, SiteStreetname, SiteType, SiteDir, SiteAptNo, SiteCity, SiteZip5 FROM Property WHERE BookPg=? AND Lot=?", '00260077', '286').fetchall()
#     rows = cur.execute(SQL).fetchall()
    pprint.pprint(rows)
    cur.close()
    con.close()
    
    # you could change the mode from 'w' to 'a' (append) for any subsequent queries
#     with open('mytable.csv', 'wb') as fou:
#         csv_writer = csv.writer(fou) # default field-delimiter is ","
#         csv_writer.writerows(rows)

if __name__ == '__main__':
    sys.exit(main())