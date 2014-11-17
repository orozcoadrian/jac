'''
Created on Nov 2, 2014

@author: Adrian
'''
import sys
import csv, pyodbc
import pprint
import logging


def fetch_bcpao_by_parcel_id(cur, twp, rng, sec, sub, blk, lot):
    logging.debug('fetch_bcpao_by_parcel_id(lot='+str(lot)+', blk='+str(blk)+', s='+str(sec)+', t='+str(twp)+', r='+str(rng)+', subid='+str(sub)+')')
    rows=None
    if blk and lot:
        print('blk and lot')
        rows = cur.execute("SELECT TaxAcct, SiteHouseNo, SiteStreetname, SiteType, SiteDir, SiteAptNo, SiteCity, SiteZip5, MarketValueCurr FROM Property WHERE Twp=? AND Rng=? AND Sec=? AND Sub=? AND Blk=? AND Lot=?", twp, rng, sec, sub, blk, lot).fetchall()
    elif lot:
        print('lot')
        rows = cur.execute("SELECT TaxAcct, SiteHouseNo, SiteStreetname, SiteType, SiteDir, SiteAptNo, SiteCity, SiteZip5, MarketValueCurr FROM Property WHERE Twp=? AND Rng=? AND Sec=? AND Sub=? AND Blk is NULL AND Lot=?", twp, rng, sec, sub, lot).fetchall()
    elif blk:
        print('blk')
        rows = cur.execute("SELECT TaxAcct, SiteHouseNo, SiteStreetname, SiteType, SiteDir, SiteAptNo, SiteCity, SiteZip5, MarketValueCurr FROM Property WHERE Twp=? AND Rng=? AND Sec=? AND Sub=? AND Blk=? AND Lot is NULL", twp, rng, sec, sub, blk).fetchall()
#     rows = cur.execute(SQL).fetchall()
    pprint.pprint(rows)
    return rows

def fetch_bldng_by_taxacct(cur, taxacct):
    logging.debug('fetch_bldng_by_taxacct(taxacct='+str(taxacct)+')')
    rows = cur.execute("SELECT BaseArea, YearBuilt, FrameCode FROM Buildings WHERE TaxAcct=?", taxacct).fetchall()
#     rows = cur.execute(SQL).fetchall()
    pprint.pprint(rows)
    return rows

def fetch_item_by_parcel_id2(cur, twp, rng, sec, sub, blk, lot):
    ret = {}
    rows = fetch_bcpao_by_parcel_id(cur, twp=twp, rng=rng, sec=sec, sub=sub, blk=blk, lot=lot)
    if rows:
        ret['TaxAcct']=rows[0][0]
        ret['MarketValueCurr']=float(str(rows[0][8]))
        addr_parts=[]
        if rows[0][1]:
            addr_parts.append(str(rows[0][1]))
        if rows[0][2]:
            addr_parts.append(str(rows[0][2]))
        if rows[0][3]:
            addr_parts.append(str(rows[0][3]))
        if rows[0][4]:
            addr_parts.append(str(rows[0][4]))
        if rows[0][5]:
            addr_parts.append(str(rows[0][5]))
        if rows[0][6]:
            addr_parts.append(',')
            addr_parts.append(str(rows[0][6]))
        if rows[0][7]:
            addr_parts.append(str(rows[0][7]))
        ret['address']=' '.join(addr_parts)
        rows = fetch_bldng_by_taxacct(cur, rows[0][0])
        try:
            ret['BaseArea']=rows[0][0]
            ret['YearBuilt']=rows[0][1]
            ret['FrameCode']=rows[0][2].replace(',','').replace(' ','')
        except:
            print('exception caught!!!!!!!')

        return ret

def fetch_item_by_parcel_id(twp, rng, sec, sub, blk, lot):
    logging.debug('fetch_item_by_parcel_id('+'twp='+str(twp)+', rng='+str(rng)+', sec='+str(sec)+', sub='+str(sub)+', blk='+str(blk)+', lot='+str(lot)+')')
    MDB = 'C:/Users/Adrian/Downloads/Web97/web97 - Copy.mdb'; DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = 'pw'

    # connect to db
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()

    blk_to_use = ''
    if blk:
        blk_to_use = blk
    if blk_to_use.endswith('U'):
        blk_to_use = blk_to_use[:-1]+'.U'
    i = fetch_item_by_parcel_id2(cur, twp=twp, rng=rng, sec=sec, sub=sub, blk=blk_to_use, lot=lot)
#     pprint.pprint(i)
#     rows = cur.execute("SELECT TaxAcct, SiteHouseNo, SiteStreetname, SiteType, SiteDir, SiteAptNo, SiteCity, SiteZip5 FROM Property WHERE BookPg=? AND Lot=?", '00260077', '286').fetchall()
#     rows = cur.execute(SQL).fetchall()
#     pprint.pprint(rows)
    cur.close()
    con.close()

    return i

def main():
    print('hi')
    # set up some constants
    # C:\Users\Adrian\Downloads\MDBPlus
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
#     rows = fetch_bcpao_by_parcel_id(cur, twp='23', rng='35', sec='14', sub='JZ', blk='320', lot='16')
#     fetch_bldng_by_taxacct(cur, rows[0][0])
#     i = fetch_item_by_parcel_id2(cur, twp='23', rng='35', sec='14', sub='JZ', blk='320', lot='16')
#     try:
#         i = fetch_item_by_parcel_id2(cur, twp='28', rng='37', sec='15', sub='81', blk='', lot='95')
#     except:
#         print('exception caught!')
    try:
        i = fetch_item_by_parcel_id2(cur, twp='28', rng='37', sec='15', sub='81', blk=None, lot='95')
    except:
        print('exception caught!')
        raise
#     try:
#         i = fetch_item_by_parcel_id2(cur, twp='28', rng='37', sec='15', sub='81', blk=' ', lot='95')
#     except:
#         print('exception caught!')
#     i = fetch_item_by_parcel_id2(cur, twp='28', rng='37', sec='15', sub='81', blk='', lot='95')
#     pprint.pprint(i)
#     rows = cur.execute("SELECT TaxAcct, SiteHouseNo, SiteStreetname, SiteType, SiteDir, SiteAptNo, SiteCity, SiteZip5 FROM Property WHERE BookPg=? AND Lot=?", '00260077', '286').fetchall()
#     rows = cur.execute(SQL).fetchall()
#     pprint.pprint(rows)
    cur.close()
    con.close()

    # you could change the mode from 'w' to 'a' (append) for any subsequent queries
#     with open('mytable.csv', 'wb') as fou:
#         csv_writer = csv.writer(fou) # default field-delimiter is ","
#         csv_writer.writerows(rows)

if __name__ == '__main__':
    sys.exit(main())