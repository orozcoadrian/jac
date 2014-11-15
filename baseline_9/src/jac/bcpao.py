#import sys
#import os
import requests
#from time import strftime
#import re
import pprint
import urllib
# from urllib import parse
# from html.parser import HTMLParser
from HTMLParser import HTMLParser
# import html.parser
from bs4 import BeautifulSoup

from contextlib import closing
from urllib2 import urlopen
#import html5lib
import unittest
import bclerk

class TestUM(unittest.TestCase):
    def test_house(self):
        # case_number	            case_title	                    foreclosure_sale_date	brevard clerk	count	address	                            zip code	latest_amount_due	liens	                    defendants	bcpao acct	frame code	latest market value total	total base area	sq feet	year built
        # 05-2007-CA-030452-XXXX-XX	DEUTSCHE BANK VS ROLANDO PEREZ	06/04/2014	            link	        1	    1123 FLOWER ST NW , PALM BAY 32907	32907	    237,804.43	        05-2007-CA-030452-XXXX-XX	 	        2807459

        i=get_bcpaco_item('2807459')
        #https://www.bcpao.us/asp/Show_parcel.asp?acct=2807459&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Owner
        pprint.pprint(i)
        self.assertEqual(i['address'] , '1123 FLOWER ST NW , PALM BAY 32907')
        self.assertEqual(i['latest market value total'] , '$49,910')
        self.assertEqual(i['zip_code'] , '32907')
        self.assertEqual(i['frame code'] , '04')
        self.assertEqual(i['year built'] , '1985')
        # self.assertEqual(i['sq feet'] , '')
        self.assertEqual(i['total base area'] , '1,173')
        self.assertEqual(i['use code']['use_code'] , '110')
        self.assertEqual(i['use code']['use_code_str'] , 'R-SINGLE FAMILY RESIDENCE')

    def test_condo(self):
        # case_number	            case_title	                    foreclosure_sale_date	brevard clerk	count	address	                                    zip code	latest_amount_due	liens	                    defendants	bcpao acct	frame code	latest market value total	total base area	sq feet	year built
        # 05-2014-CA-013327-XXXX-XX	BANK AMERICA VS ERNEST FINNEY	06/05/2014	            link	        208	    7667 N WICKHAM RD  1009, MELBOURNE 32940	32940	    202,665.14	        05-2014-CA-013327-XXXX-XX	 	        2630481		            $58,030		                                1,256	1990

        i=get_bcpaco_item('2630481')
        #https://www.bcpao.us/asp/Show_parcel.asp?acct=2630481&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Owner
        pprint.pprint(i)
        self.assertEqual(i['address'] , '7667 N WICKHAM RD  1009, MELBOURNE 32940')
        self.assertEqual(i['latest market value total'] , '$83,000')
        self.assertEqual(i['zip_code'] , '32940')
        # self.assertEqual(i['frame code'] , '04')
        #self.assertEqual(i['year built'] , '1990') # broken
        #self.assertEqual(i['sq feet'] , '1,256') # broken
        # self.assertEqual(i['total base area'] , '1,173')

    def test_legal(self):
#                       T  R  S  SUBID    BLK
#         Parcel ID:    28-36-26-KN-02134.0-0028.00
        #                     sub,                   lot, block,   pb,   pg
        i=get_acct_by_legal(('PORT MALABAR UNIT 42', '28', '2134', '21','105', '26', '28', '35', '00'))
        pprint.pprint(i)
        self.assertEqual(i , '2807459')

    def test_legal_2(self):
        # LT 20 PB 21 PG 45 HIGH ACRES ESTATES UNIT NO 1 S 19 T 21 R 35 SUBID 25:
        # {'subid': '25', 'subd': 'HIGH ACRES ESTATES UNIT NO 1', 'pb': '21', 'lt': '20', 'pg': '45', 'blk': None}
        #                     sub,                           lot,  block,   pb,   pg
        i=get_acct_by_legal(('HIGH ACRES ESTATES UNIT NO 1', '20', None, '21','45', '19', '21', '35', '25'))
        pprint.pprint(i)
        self.assertEqual(i , '2104215')

    def test_bclerk_then_bcpao1(self):
        legal_str = 'LT 3 BLK A PB 28 PG 2 COUNTRY LAKE ESTS S 1/2 OF S 30 T 24 R 36 SUBID 54'
        legal=bclerk.get_legal_from_str(legal_str)
        print('legal='+str(legal))
        acct=str(get_acct_by_legal((legal['subd'],legal['lt'],legal['blk'],legal['pb'],legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])))
        print(acct)
        self.assertEqual(acct, '2423677')

    def test_bclerk_then_bcpao2(self):
        legal_str='LT 36 PB 29 PG 46 SHERWOOD FOREST P.U.D. II, REPLAT OF STAGE ONE, TRACT A S 24 T 21 R 34 SUBID 05'
        legal=bclerk.get_legal_from_str(legal_str)
        print('legal='+str(legal))
        acct=str(get_acct_by_legal((legal['subd'],legal['lt'],legal['blk'],legal['pb'],legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])))
        print(acct)
        self.assertEqual(acct, '2101315')

    def test_bclerk_then_bcpao3(self):
        legal_str='BLK 8S U 3103 NE 1/4 OF NE 1/4 EX E 50 FT & EX CYPRESS SPRINGS CONDO ORB 5620/2802 S 16 T 28 R 37 SUBID 00'
        legal=bclerk.get_legal_from_str(legal_str)
        print('legal='+str(legal))
        self.assertEqual(legal['blk'], '8S')
        self.assertEqual(legal['s'], '16')
        self.assertEqual(legal['r'], '37')
        self.assertEqual(legal['t'], '28')
        self.assertEqual(legal['subid'], '00')
        acct=str(get_acct_by_legal((legal['subd'],legal['lt'],legal['blk'],legal['pb'],legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])))
        print(acct)
        self.assertEqual(acct, '2864518')

    def test_bclerk_then_bcpao4(self):
        legal_str='LT 1928 PB 10 PG 21 U 401 WINSLOW RESERVE SUBD THE MERIDIAN, A CONDOMINIUM PH I ORB 5782/5772 S 26 T 24 R 37 SUBID 27'
        legal=bclerk.get_legal_from_str(legal_str)
        print('legal='+str(legal))
        self.assertEqual(legal['blk'], None)
        self.assertEqual(legal['s'], '26')
        self.assertEqual(legal['r'], '37')
        self.assertEqual(legal['t'], '24')
        self.assertEqual(legal['subid'], '27')
        acct=str(get_acct_by_legal((legal['subd'],legal['lt'],legal['blk'],legal['pb'],legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])))
        print(acct)
#         self.assertEqual(acct, '---')

    def test_bclerk_then_bcpao5(self):
        legal_str='BLK 283F U 706 N 7.5 FT OF S 632.5 FT OF LOT 2 CANAVERAL BAY CONDO PH VII ORB 2648/2338 S 22 T 24 R 37 SUBID 00'
        legal=bclerk.get_legal_from_str(legal_str)
        print('legal='+str(legal))
        self.assertEqual(legal['blk'], '283F')
        self.assertEqual(legal['s'], '22')
        self.assertEqual(legal['r'], '37')
        self.assertEqual(legal['t'], '24')
        self.assertEqual(legal['subid'], '00')
        acct=str(get_acct_by_legal((legal['subd'],legal['lt'],legal['blk'],legal['pb'],legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])))
        print(acct)
        self.assertEqual(acct, '2441816')

    def test_bclerk_then_bcpao6(self):
        legal_str='LT 7804 PB 29 PG 71 U 3 LA CITA SECTION 5 SWEET MAGNOLIA CONDO ORB 2732/2040 S 16 T 22 R 35 SUBID MR'
#         Parcel ID:    22-35-16-MR-00000.0-0078.04
        legal=bclerk.get_legal_from_str(legal_str)
        print('legal='+str(legal))
        acct=str(get_acct_by_legal((legal['subd'],legal['lt'],legal['blk'],legal['pb'],legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])))
        print(acct)
        self.assertEqual(acct, '2207771')

    def test_bclerk_then_bcpao7(self):
        legal_str='LT 5 BLK 66 PB 4 PG 12 INDIAN RIVER CITY, REVISED PLAT OF S 22 T 22 R 35 SUBID 75'
#         Parcel ID:    22-35-16-MR-00000.0-0078.04
        legal=bclerk.get_legal_from_str(legal_str)
        print('legal='+str(legal))
        acct=str(get_acct_by_legal((legal['subd'],legal['lt'],legal['blk'],legal['pb'],legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])))
        print(acct)
#         self.assertEqual(acct, '---') # this one fails because there's a bcpao account only for lot 4 not 5

    def test_bclerk_then_bcpao8(self):
        legal_str='BLK 750J U 1-205 PART OF NE 1/4 OF NE 1/4 AS DES BELLA VISTA CONDO PHASE I ORB 5595/8053 S 20 T 25 R 36 SUBID 00'
#         Parcel ID:    22-35-16-MR-00000.0-0078.04
        legal=bclerk.get_legal_from_str(legal_str)
        print('legal='+str(legal))
        acct=str(get_acct_by_legal((legal['subd'],legal['lt'],legal['blk'],legal['pb'],legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])))
        print(acct)
        self.assertEqual(acct, '2537717')

    def test_bclerk_then_bcpao9(self):
        legal_str='BLK 7797 U 259 E 150 FT OF N 170 FT OF NE 1/4 CASA VERDE CLUB CONDO PH V ORB 2625/2765 BLDG N S 05 T 25 R 36 SUBID 00'
#         Parcel ID:    22-35-16-MR-00000.0-0078.04
        legal=bclerk.get_legal_from_str(legal_str)
        print('legal='+str(legal))
        acct=str(get_acct_by_legal((legal['subd'],legal['lt'],legal['blk'],legal['pb'],legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])))
        print(acct)
        self.assertEqual(acct, '2503567')


    def assertAcctFromLegal(self, legal_str, expectedAcct):
        legal = bclerk.get_legal_from_str(legal_str)
        print 'legal=' + str(legal)
        acct = str(get_acct_by_legal((legal['subd'], legal['lt'], legal['blk'], legal['pb'], legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])))
        print acct
        self.assertEqual(acct, expectedAcct)

    def test_bclerk_then_bcpao10(self):
        self.assertAcctFromLegal('LT 14 BLK 3 PB 19 PG 58 MARLIN SUBD S 05 T 25 R 36 SUBID 52', '2504233')
    def test_bclerk_then_bcpao11(self):
        #self.assertAcctFromLegal('LT 16 BLK D PB 44 PG 23 VIERA CENTRAL PUD TRACT 12 UNIT 1 PARCELS 1-3, PHASE 2B S 16 T 26 R 36 SUBID RF', '---')
        #self.assertAcctFromLegal('LT 6 PB 1 PG 164 FLORIDA INDIAN RIVER LAND CO PARCEL 1 FROM S QUARTER CNR BEING INTERSEC OF CENLN OF ST RD 9 S 33 T 28 R 37', '---')
        #self.assertAcctFromLegal('LT 710 BLK 48 PB 3 PG 7 U 10C2 AVON BY THE SEA OCEAN PARK CONDO NORTH ORB 2024/745 S 23 T 24 R 37 SUBID CG', '---') # LT 7.10
        #self.assertAcctFromLegal('LT 36 PB 26 PG 103 INDUSTRIAL PLAZA UNIT 1 TRACT C COMM @ INTERSEC OF N R/W OF ELLIS RD & CENTERLN OF E DR S 26 T 27 R 36 SUBID 75', '---')
        self.assertAcctFromLegal('LT 95 PB 48 PG 69 EAGLE LAKE EAST PHASE 1 S 15 T 28 R 37 SUBID 81', '2859710')
        #self.assertAcctFromLegal('LT 3 BLK G PB 10 PG 22 GOLF PARK SUBD S 20 FT S 04 T 28 R 37 SUBID 51', '---')
        self.assertAcctFromLegal('LT 14 BLK 3 PB 19 PG 58 MARLIN SUBD S 05 T 25 R 36 SUBID 52', '2504233')
#         self.assertAcctFromLegal('LT 6 PB 1 PG 164 FLORIDA INDIAN RIVER LAND CO PARCEL 1 FROM S QUARTER CNR BEING INTERSEC OF CENLN OF ST RD 9 S 33 T 28 R 37', '---')
        self.assertAcctFromLegal('BLK 20U U A21 N 227.29 FT OF E 128 FT OF W 778 TREASURE COAST HARBOUR VILLAS CONDO ORB 5741/5541 S 31 T 24 R 37 SUBID 00', '2461077')

    def test_bclerk_then_bcpao12(self):
        self.assertAcctFromLegal('LT 14 BLK 180 PB 23 PG 53 PORT ST JOHN UNIT 6 COMM @ NW CNR S 21 T 23 R 35 SUBID JX', '2322639') # not 2306233 !!!

    def test_one(self):
        i=get_bcpaco_item('2724389')
        pprint.pprint(i)
        self.assertEqual(i['address'] , '800  BALLARD DR , MELBOURNE 32935')
        self.assertEqual(i['latest market value total'] , '$76,150')
        self.assertEqual(i['zip_code'] , '32935')
        self.assertEqual(i['frame code'] , '03')
        self.assertEqual(i['year built'] , '1951')
        # self.assertEqual(i['sq feet'] , '1,256')
        self.assertEqual(i['total base area'] , '1,272')

    def test_2613083(self):
        i=get_bcpaco_item('2613083')
        pprint.pprint(i)
        self.assertEqual(i['address'] , '320  LEE AVE , SATELLITE BEACH 32937')
        self.assertEqual(i['latest market value total'] , '$150,850')
        self.assertEqual(i['zip_code'] , '32937')
        self.assertEqual(i['frame code'] , '03')
        self.assertEqual(i['year built'] , '1974')
        # self.assertEqual(i['sq feet'] , '1,256')
        self.assertEqual(i['total base area'] , '1,545')

def get_use_code_str(use_code):
    #https://www.bcpao.us/asp/Show_code.asp?numeric=t&table=UseCodes&ValColName=UseCode&DescColName=UseDesc&value=110
    the_map={}
    the_map['110']='R-SINGLE FAMILY RESIDENCE'
    the_map['212']='M-MANUFACTURED HOUSING - SINGLE WIDE'
    the_map['213']='M-MANUFACTURED HOUSING - DOUBLE WIDE'
    the_map['214']='M-MANUFACTURED HOUSING - TRIPLE WIDE'
    if use_code in the_map:
        return the_map[use_code]

def get_bcpao_query_url_by_acct(acct):
    return 'https://www.bcpao.us/asp/Show_parcel.asp?acct='+acct+'&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Owner'

def get_cpao_query_link_by_acct(acct):
    return '<br><a href='+get_bcpao_query_url_by_acct(acct)+'>'+acct+'</a>'


def get_acct_by_legal(legal):
    sub, lot, block, pb, pg, s, t, r, subid = legal
    sub = sub.replace(u'\xc2', u'').encode('utf-8')
    print('get_acct_by_legal(sub="'+sub+'", lot='+str(lot)+', block='+str(block)+', pb='+str(pb)+', pg='+str(pg)+', s='+str(s)+', t='+str(t)+', r='+str(r)+', subid='+str(subid)+')')
    ret=''

    url = 'https://www.bcpao.us/asp/find_property.asp'
    headers = {
        # 'Cookie': 'CFID='+cfid+'; CFTOKEN='+cftoken,
        'Cookie': 'ASPSESSIONIDQABRBBSS=ELGLAMBAELLCGOLCONGKOFHE',
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    if not ret:
        data=None
        offset=82
#         if pb is not None and pg is not None and lot is not None and block is not None:
#             data='SearchBy=Plat&book='+str(pb)+'&page='+str(pg)+'&blk='+str(block)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
#             offset=86
        if sub is not None and pg is not None and lot is not None and block is not None:
            data='SearchBy=Sub&sub='+urllib.quote(sub)+'&blk='+str(block)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
#         elif pb is not None and pg is not None and lot is not None:
#             data='SearchBy=Plat&book='+str(pb)+'&page='+str(pg)+'&blk=&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
#             offset=86
        elif pg is not None:
            data='SearchBy=Sub&sub='+urllib.quote(sub)+'&pg='+str(pg)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
        # r = requests.post(url, data, stream=True)
        req = requests.post(url, headers=headers, data=data)
        # the_url="https://www.bcpao.us/asp/find_property.asp?"+'SearchBy=Sub&sub='+urllib.quote(sub)+'&blk='+str(block)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
        # print(the_url)
        soup = BeautifulSoup(req.text.encode('utf-8'), 'html.parser')
        # print_headers(the_url, 'html.parser')
        rers_cell = soup.find(text="Real Estate Records Search")

#         for a in soup.find_all('a'):
#             pprint.pprint(a)
        aerials = soup.find_all('a', text="Aerial")
        if aerials and len(aerials) > 1:
            # need to ignore this whole page if we have more than one result. can search for how many "Aerial" there are
            print('ignoring this whole page because we have more than one result (tax ids)')
            rers_cell = None
        # print_small_texts(list(rers_cell.parent.parent.parent.parent.parent.descendants), max=50)
        # print_headers(soup, 'Real Estate Records Search')
        if rers_cell is not None:
            # print_small_texts(list(rers_cell.parent.parent.parent.parent.parent.descendants))
        # print(bi_cell.parent.parent.parent.parent)
        # # print(list(bi_cell.parent.parent.parent.parent.descendants))
        # for index, item in enumerate(list(bi_cell.parent.parent.parent.parent.parent.descendants)):
            # try:
                # print('list(bi_cell.parent.parent.parent.parent.descendants)['+str(index)+']: ' + str(item).decode('utf-8').replace(u'\xa0', u''))
            # except:
                # pass
            # ret=str(list(rers_cell.parent.parent.parent.parent.parent.descendants)[82])
            ret=str(list(rers_cell.parent.parent.parent.parent.parent.descendants)[offset])

    if not ret:
        print('trying condo')

        data=None
        offset=82
        if block and block.endswith('S'):
            block = block[:-1]+'.S'
        elif block and block.endswith('F'):
            block = block[:-1]+'.F'
        elif block and block.endswith('J'):
            block = block[:-1]+'.J'
        elif block and block.endswith('L'):
            block = block[:-1]+'.L'
        elif block and block.endswith('U'):
            block = block[:-1]+'.U'
        if lot and len(lot) == 4 and '.' not in lot:
            print('lot is length 4')
            lot = lot[0:2]+'.'+lot[2:4]
        if block and len(block) == 4 and '.' not in block:
            print('block is length 4')
            block = block[0:3]+'.'+block[3:4]
        blk_str=''
        if block:
            blk_str = block
        lot_str=''
        if lot:
            lot_str = lot
        data='SearchBy=PID&twp='+str(t)+'&rng='+str(r)+'&sec='+str(s)+'&subn='+str(subid)+'&blk='+str(blk_str)+'&lot='+str(lot_str)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
        req = requests.post(url, headers=headers, data=data)
        # the_url="https://www.bcpao.us/asp/find_property.asp?"+'SearchBy=Sub&sub='+urllib.quote(sub)+'&blk='+str(block)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
        print(data)
        soup = BeautifulSoup(req.text.encode('utf-8'), 'html.parser')
#         print(soup.prettify())
#         print_headers(the_url, 'html.parser')
        rers_cell = soup.find(text="Real Estate Records Search")
        #print_small_texts(list(rers_cell.parent.parent.parent.parent.parent.descendants), max=50)
        if rers_cell is not None:
            ret=str(list(rers_cell.parent.parent.parent.parent.parent.descendants)[offset])

    if not ret:
        print('no bcpao acct, no address')

    return ret

def get_acct_by_name(name):
    print("get_acct_by_name('"+name+"')")
    url = 'https://www.bcpao.us/asp/find_property.asp'
    headers = {
        # 'Cookie': 'CFID='+cfid+'; CFTOKEN='+cftoken,
        'Cookie': 'ASPSESSIONIDQABRBBSS=ELGLAMBAELLCGOLCONGKOFHE',
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    data='SearchBy=Owner'
    data+='&owner='+urllib.quote(name)
    data+='&owner2='
    data+='&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
    # r = requests.post(url, data, stream=True)
    r = requests.post(url, headers=headers, data=data)
    # print(r.text.encode('utf-8'))

    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            # print('handle_starttag: '+tag)
            if 'tr' in tag and len(self.rows) < self.limit and self.table_count == 3:
                self.in_tr = True
                self.current_row = {}
            if 'table' in tag and len(self.tables) < self.limit_tables:
                self.current_table = {}
                self.table_count +=1

            # elif 'th' in tag:
                # self.current_table['headers'].append(tag)
        def handle_endtag(self, tag):
            if 'td' in tag:
                self.td_count += 1
            if 'tr' in tag:
                self.rows.append(self.current_row)
                self.current_row = None
                self.in_tr = False
            if 'table' in tag:
                self.tables.append(self.current_table)
                self.current_table = None
                # if self.td_count > 0:
                    # self.current_row['count']=len(self.rows)
                    # self.rows.append(self.current_row)
                    # self.td_count = 0
                    # self.current_row = {}
        def handle_data(self, data):
            # print('handle_data: ' + data)
            if self.table_count == 3:
                if self.in_tr:
                    if self.td_count == 0:
                        self.current_row['a']=data
                    elif self.td_count == 1:
                        self.current_row['b']=data
                    elif self.td_count == 2:
                        self.current_row['c']= data
                    elif self.td_count == 3:
                        self.current_row['d']=data
                    elif self.td_count == 4:
                        self.current_row['e']=data
                    elif self.td_count == 5:
                        self.current_row['f']=data
                    elif self.td_count == 6:
                        self.current_row['g']=data

    parser = MyHTMLParser()
    parser.limit_tables = 2
    parser.limit = 5
    parser.rows = []
    parser.current_row = None
    parser.in_tr = False
    parser.tables = []
    parser.table_count = 0
    parser.td_count = 0
    parser.current_table = None
    parser.current_table_headers = None
    # parser.feed(str(r.text.encode('utf-8')))
    parser.feed(str(r.text.encode('utf-8')))
    # pprint.pprint(parser.tables)
    # pprint.pprint(parser.rows)
    print('rows: '+str(len(parser.rows)))
    for r in parser.rows:
        try:
            print(r['e']+' | '+r['f']+' | '+r['g'])
            return r['e']
        except:
            pass

def print_small_texts(the_list,max2=20):
    for index, item in enumerate(the_list):
        # print('the_list['+str(index)+']: ' + item.encode('utf-8'))
        if len(item.encode('utf-8').strip()) > 0 and len(item.encode('utf-8')) < max2:
            print('the_list['+str(index)+']: ' + item.encode('utf-8'))

def get_bcpaco_item(acct):
    print("get_bcpaco_item('"+acct+"')")
    # don't do anything if acct is blank (same in bcpao_radius
    ret={}
    if acct is None or len(acct) == 0:
        return ret
    # https://www.bcpao.us/asp/Show_parcel.asp?acct=2713420&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Address
    # url = 'https://www.bcpao.us/asp/Show_parcel.asp'
    # headers = {
        # 'Cookie': 'ASPSESSIONIDQABRBBSS=ELGLAMBAELLCGOLCONGKOFHE',
        # 'Content-Type': 'application/x-www-form-urlencoded'
        # }
    # data='acct='+acct+'&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Address'
    # r = requests.post(url, headers=headers, data=data)

    # with closing(urlopen("https://www.bcpao.us/asp/Show_parcel.asp?"+'acct='+acct+'&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Address')) as f:
        # document = html5lib.parse(f, encoding=f.info().getparam("charset"))
        # print(document)

    # print(str(r.text.encode('utf-8'))[8000:9000])
    # print(str(r.text))
    the_url="https://www.bcpao.us/asp/Show_parcel.asp?"+'acct='+acct+'&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Address'


    try:
        soup = BeautifulSoup(urlopen(the_url))
        # print(soup.prettify())
        #gpc = soup.find(text="General Parcel Information")
        # print_small_texts(list(soup.descendants), max=500)
        sa = soup.find(text="Site Address:")
        if sa is not None:
            # print_small_texts(list(sa.parent.parent.descendants), max=50)
            # # for index,item in enumerate(list(gpc.parent.parent.parent.descendants)):
                # # print('list(gpc.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
                # # if str(item).startswith('7667'):
                    # # print('list(gpc.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
            ret['address']=str(list(sa.parent.parent.descendants)[5].replace('\\r\\n','').strip())
            ret['zip_code']=ret['address'][-5:]
    except:
        raise

    try:
        with closing(urlopen(the_url)) as f:
            html = f.read().replace(u'\xa0', u'').encode('utf-8')
            filtered=[]
            for l in html.split('\n'):
                if 'javascript:void(0);' not in l and 'px;"' not in l and '&nbsp;' not in l:
                    to_append=l.replace(u'\xa0', u'').encode('utf-8')
                    filtered.append(to_append)
                    # print(to_append)
                # else:
                    # print('filtering: '+l)
            data=''.join(filtered)
            soup = BeautifulSoup(data, 'html.parser')
        # soup = BeautifulSoup(urlopen(the_url))
        # print(soup.prettify())
            vs_cell = soup.find(text="Value Summary")
            # print_small_texts(list(soup.descendants), max=50)
        # print_headers(the_url, 'html.parser')
        # print_headers(the_url, 'html5lib')
            # print(str(soup.find(text='110')))
        # print(BeautifulSoup(urlopen(the_url)).prettify())
        # sa = soup.find(text="Site Address:")
            if vs_cell is not None:
                # print_small_texts(list(vs_cell.parent.parent.parent.parent.descendants))
            # # # for index,item in enumerate(list(gpc.parent.parent.parent.descendants)):
                # # # print('list(gpc.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
                # # # if str(item).startswith('7667'):
                    # # # print('list(gpc.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
                ret['latest market value total']=str(list(vs_cell.parent.parent.parent.parent.descendants)[35])
            # ret['zip_code']=ret['address'][-5:]

            bi_cell = soup.find(text="Building Information")
            # print(bi_cell)
            if bi_cell is not None:
                # print_small_texts(list(bi_cell.parent.parent.parent.parent.parent.descendants))
                use_code=list(bi_cell.parent.parent.parent.parent.parent.descendants)[52].encode('utf-8')
                ret['use code']=dict(use_code=use_code, use_code_str=get_use_code_str(use_code))
                ret['year built']=str(list(bi_cell.parent.parent.parent.parent.parent.descendants)[56])
                ret['frame code']=str(list(bi_cell.parent.parent.parent.parent.parent.descendants)[65])

            bai_cell = soup.find(text="Building Area Information")
            if bai_cell is not None:
                # print_small_texts(list(bai_cell.parent.parent.parent.parent.parent.descendants))
                ret['total base area']=str(list(bai_cell.parent.parent.parent.parent.parent.descendants)[59])
    except:
        raise

    # print(ret)

    try:
        if 'latest market value total' not in ret:
            with closing(urlopen(the_url)) as f:
                soup = BeautifulSoup(f, "html.parser")
                mvt = soup.find(text="Market Value Total:")
                # for index,item in enumerate(list(mvt.parent.parent.descendants)):
                    # print('list(gpc.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
                if mvt:
                    ret['latest market value total']=str(list(mvt.parent.parent.descendants)[13])

        if 'latest market value total' not in ret:
            with closing(urlopen(the_url)) as f:
                html = f.read().replace(u'\xa0', u'').encode('utf-8')
                filtered=[]
                for l in html.split('\n'):
                    if 'Homestead' not in l and 'tdHeader_Row_1_Col_1' not in l:
                        filtered.append(l.replace(u'\xa0', u'').encode('utf-8'))
                    # else:
                        # print('filtering: '+l)
                soup = BeautifulSoup(''.join(filtered), "html5lib")
                mvt = soup.find(text="Market Value Total:")
                # print(soup.find(text="General Parcel Information"))
                # print(soup.find(text="Owner Information"))
                # print(soup.find(text="Owner Name:"))
                # print(soup.find(text="Second  Name:"))
                # print(soup.find(text="Mailing Address:"))
                # print(soup.find(text="City, State, Zipcode:"))
                # print(soup.find(text="Taxable Value School:"))
                # print(soup.find(text="Roll Year:"))
                # print(soup.find(text="Sale Information"))
                # print(soup.find(text="Sale Date"))
                # print(soup.find(text="Land Information"))
                # print(soup.find(text="Acres"))
                # print(soup.find(text="Millage Code:"))
                # print(soup.find(text="Exemption:"))
                # print(soup.find(text="Use Code:"))
                # print(soup.find(text="Site Address:"))
                # print(soup.find(text="Tax ID:"))
                #pi = soup.find(text="Tax ID:")
                # print(pi)
                # print(soup.find(text="Owner Name:"))
                # print(soup.find(text="Roll Year:"))
                # print(soup.find(text="Assessed Value School:"))
                # for index,item in enumerate(list(pi.parent.parent.parent.parent.parent.descendants)):
                    # print('list(pi.parent.parent.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
                # for index,item in enumerate(list(soup.descendants)):
                    # print('\n\n\n\n\n\n\n\n\nlist(soup.descendants)['+str(index)+']: '+str(item))
                # b=list(soup.descendants)[26]
                # c=list(b.descendants)[9]
                # for index,item in enumerate(list(b.descendants)):
                    # print('list(\n\n\n\n\n\n\n b.descendants)['+str(index)+']: '+str(item))
                    # if '$' in str(item):
                        # print('['+str(index)+']: '+str(item))
                    # if str(item).startswith('$'):
                        # print('list(pi.parent.parent.descendants)['+str(index)+']: '+str(item))
                # if mvt:
                    # ret['latest market value total']=str(list(mvt.parent.parent.descendants)[13])

            class MyHTMLParser(HTMLParser):
                def handle_starttag(self, tag, attrs):
                    print('handle_starttag: ' + tag)
                    if 'tr' in tag:
                        self.in_tr = True
                def handle_endtag(self, tag):
                    if 'tr' in tag:
                        self.in_tr = False
                        self.in_mvt = False
                def handle_data(self, data):
                    # print('handle_data: ' + data)
                    if 'Market Value Total:' in data:
                        self.in_mvt = True
                    if self.in_mvt and '\\n' not in data:
                        self.mvt = data
                        print('handle_data: ' + data)

            parser = MyHTMLParser()
            parser.limit_tables = 20
            parser.limit = 5000
            parser.rows = []
            parser.current_row = None
            parser.in_tr = False
            parser.tables = []
            parser.table_count = 0
            parser.td_count = 0
            parser.in_table = False
            parser.current_table = None
            parser.in_mvt = False
            # print(r.text)
            # print(r.json())
            f = urlopen(the_url)
            html = f.read()
            # parser.feed(html)
            # parser.feed(urlopen(the_url).encode('utf-8'))
            # parser.feed(str(r.text))
            # pprint.pprint(parser.tables)
            # print(parser.mvt)
            # return parser.mvt
            # ret['latest market value total']=parser.mvt
    except:
        raise#print('123 ex: '+str(e))

    try:
        # year built - Condo Unit Detail
        soup = BeautifulSoup(urlopen(the_url), 'html.parser')
        bi_cell = soup.find(text="Building Information")
        if bi_cell is not None:
            # for index, item in enumerate(list(bi_cell.parent.parent.parent.parent.parent.descendants)):
                # print('list(fc_cell.parent.parent.parent.parent.parent.descendants)['+str(index)+']: ' + str(item))
                # if str(item).startswith('1,173'):
                    # break
            ret['year built']=list(bi_cell.parent.parent.parent.parent.parent.descendants)[56]

            bai_cell = soup.find(text="Building Area Information")
            # for index, item in enumerate(list(bai_cell.parent.parent.parent.parent.parent.descendants)):
                # print('list(fc_cell.parent.parent.parent.parent.parent.descendants)['+str(index)+']: ' + str(item))
                # if str(item).startswith('1,173'):
                    # break
            ret['total base area']=list(bai_cell.parent.parent.parent.parent.parent.descendants)[59]

        cud_cell = soup.find(text="Condo Unit Detail")
        if cud_cell is not None:
            # for index, item in enumerate(list(cud_cell.parent.parent.parent.parent.parent.descendants)):
                # if len(item.encode('utf-8').strip()) > 0 and len(item.encode('utf-8')) < 20:
                    # print('list(fc_cell.parent.parent.parent.parent.parent.descendants)['+str(index)+']: ' + item.encode('utf-8'))
                # if item.encode('utf-8').startswith('1990'):
                    # break
            ret['year built']=list(cud_cell.parent.parent.parent.parent.parent.descendants)[198].encode('utf-8')
            ret['sq feet']=list(cud_cell.parent.parent.parent.parent.parent.descendants)[112].encode('utf-8')

    except Exception as e:
        str(e)
        raise#print('345 ex: '+str(e))

    try:
        # print_headers2(the_url)
        # the_html=urlopen(the_url)
        soup = BeautifulSoup(urlopen(the_url), 'html.parser')
        bi_cell = soup.find(text="Building Information")
        if bi_cell is not None:
            # print_headers(the_url, 'html.parser')
            # print_headers(the_url, 'html5lib')
            # print(fc_cell.parent.parent.parent.parent.parent)
            # print(fc_cell.parent.parent.parent.parent.parent)
            # print(list(fc_cell.parent.parent.parent.parent.parent.descendants))
            # for index, item in enumerate(list(bi_cell.parent.parent.parent.parent.parent.descendants)):
                # print('list(fc_cell.parent.parent.parent.parent.parent.descendants)['+str(index)+']: ' + str(item))
            use_code=list(bi_cell.parent.parent.parent.parent.parent.descendants)[52].encode('utf-8')
            ret['use code']=dict(use_code=use_code, use_code_str=get_use_code_str(use_code))
            ret['year built']=list(bi_cell.parent.parent.parent.parent.parent.descendants)[56].encode('utf-8')
            ret['frame code']=list(bi_cell.parent.parent.parent.parent.parent.descendants)[65].encode('utf-8')
    except:
        raise#print('sdf ex: '+str(e))

    # try:
        # bai_cell = soup.find(text="Building Area Information")
        # # print(list(fc_cell.parent.parent.parent.parent.parent.descendants))
        # # for index, item in enumerate(list(bi_cell.parent.parent.parent.parent.parent.descendants)):
            # # print('list(fc_cell.parent.parent.parent.parent.parent.descendants)['+str(index)+']: ' + str(item))
        # ret['total base area']=list(bai_cell.parent.parent.parent.parent.parent.descendants)[95].encode('utf-8')
    # except:
        # pass#print('sdf ex: '+str(e))

    manuf_codes=['212','213','214']
    if 'use code' in ret and ret['use code']['use_code'] in manuf_codes:
        ret['manuf']=True

    return ret

def get_acct(number, street, type2):
    print('get_acct('+number+', '+street+', '+type2+')')
    url = 'https://www.bcpao.us/asp/find_property.asp'
    headers = {
        # 'Cookie': 'CFID='+cfid+'; CFTOKEN='+cftoken,
        'Cookie': 'ASPSESSIONIDQABRBBSS=ELGLAMBAELLCGOLCONGKOFHE',
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    data='SearchBy=Address'
    data+='&PAD_Dir='
    data+='&PAD_Street='+street
    data+='&PAD_Type='+type2
    data+='&PAD_Number='+number
    data+='&PAD_HiNumber='+number
    data+='&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
    # r = requests.post(url, data, stream=True)
    r = requests.post(url, headers=headers, data=data)
    # print(r.text.encode('utf-8'))

    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            # print('handle_starttag: '+tag)
            if 'tr' in tag and len(self.rows) < self.limit and self.table_count == 3:
                self.in_tr = True
                self.current_row = {}
            if 'table' in tag and len(self.tables) < self.limit_tables:
                self.current_table = {}
                self.table_count +=1

            # elif 'th' in tag:
                # self.current_table['headers'].append(tag)
        def handle_endtag(self, tag):
            if 'td' in tag:
                self.td_count += 1
            if 'tr' in tag:
                self.rows.append(self.current_row)
                self.current_row = None
                self.in_tr = False
            if 'table' in tag:
                self.tables.append(self.current_table)
                self.current_table = None
                # if self.td_count > 0:
                    # self.current_row['count']=len(self.rows)
                    # self.rows.append(self.current_row)
                    # self.td_count = 0
                    # self.current_row = {}
        def handle_data(self, data):
            # print('handle_data: ' + data)
            if self.table_count == 3:
                if self.in_tr:
                    if self.td_count == 0:
                        self.current_row['a']=data
                    elif self.td_count == 1:
                        self.current_row['b']=data
                    elif self.td_count == 2:
                        self.current_row['c']= data
                    elif self.td_count == 3:
                        self.current_row['d']=data
                    elif self.td_count == 4:
                        self.current_row['e']=data
                    elif self.td_count == 5:
                        self.current_row['f']=data
                    elif self.td_count == 6:
                        self.current_row['g']=data

    parser = MyHTMLParser()
    parser.limit_tables = 2
    parser.limit = 5
    parser.rows = []
    parser.current_row = None
    parser.in_tr = False
    parser.tables = []
    parser.table_count = 0
    parser.td_count = 0
    parser.current_table = None
    parser.current_table_headers = None
    # parser.feed(str(r.text.encode('utf-8')))
    parser.feed(str(r.text.encode('utf-8')))
    # pprint.pprint(parser.tables)
    # pprint.pprint(parser.rows)
    for r in parser.rows:
        try:
            print(r['e']+' | '+r['f']+' | '+r['g'])
            return r['e']
        except:
            pass
    print('')


def print_headers(the_url, parser_name=None):
    # print('print_headers(the_html, '+parser_name+')')
    soup=None
    if parser_name is None:
        print('print_headers(the_url)')
        soup = BeautifulSoup(urlopen(the_url))
    else:
        print('print_headers(the_url, '+parser_name+')')
        soup = BeautifulSoup(urlopen(the_url), parser_name)

    texts=[]
    texts.append("BCPAO - Property Details")
    texts.append("New Search")
    texts.append("General Parcel Information")
    texts.append("Millage Code:")
    texts.append("Exemption:")
    texts.append("Use Code:")
    texts.append("Site Address:")
    texts.append("Tax ID:")
    texts.append("Owner Information")
    texts.append("Abbreviated Description")
    texts.append("Owner Name:")
    texts.append("Second  Name:")
    texts.append("Mailing Address:")
    texts.append("City, State, Zipcode:")
    texts.append("Value Summary")
    texts.append("Land Information")
    texts.append("Taxable Value School:")
    texts.append("Roll Year:")
    texts.append("Sale Information")
    texts.append("Building Information")
    texts.append("Building Area Information")
    texts.append("Extra Feature Information")
    texts.append("Sale Date")
    texts.append("Acres")




    # print(texts)
    for t in texts:
        print(t.ljust(28)+': '+str(soup.find(text=t)))

def main():
    # Year Built, Frame Code, Total Base Area
    # get_acct('1122', 'cheyenne', 'DR')
    # get_acct('1305', 'tradition', 'CIR')
    # get_acct('2600', 'fields', 'AVE')
    # get_acct('331', 'royal ', 'ST')
    # get_acct('145', 'sanderling', '')

    # data = [
        # {'number':'1122', 'street':'cheyenne', 'type':'DR'},
        # {'number':'1305', 'street':'tradition', 'type':'CIR'},
        # {'number':'2600', 'street':'fields', 'type':'AVE'},
        # {'number':'331', 'street':'royal', 'type':'ST'},
        # {'number':'145', 'street':'sanderling', 'type':''}
        # ]

    # for d in data:
        # print(get_bcpaco_item(get_acct(d['number'], d['street'], d['type

    # get_bcpaco_item(get_acct_by_name('perez, rolando'))
    names=[]
    # names.append('MCINTOSH-WILLIAMS, GRETA') #house
    # names.append('FINNEY, ERNEST') #condo
    # name='FINNEY, ERNEST'
    for name in names:
        acct=get_acct_by_name(name)
        pprint.pprint(get_bcpaco_item(acct))

    legals=[]
    # legals.append(('BRYAN HELLER ESTATES', 2, 3)) #LT 2 BLK 3 PB 10 PG 89 BRYAN HELLER ESTATES SUBD S 34 T 21 R 35 SUBID 51
    # names.append('FINNEY, ERNEST')
    # name='FINNEY, ERNEST'
    for legal in legals:
        acct=get_acct_by_legal(legal)
        if acct:
            pprint.pprint(get_bcpaco_item(acct))
    # pprint.pprint(get_bcpaco_item('2630481')) # FINNEY, ERNEST  7667 N WICKHAM RD 1009, MELBOURNE 32940
    # pprint.pprint(get_bcpaco_item('2613083')) #MORGAN, MICHAEL JAMES TRUSTEE  320 LEE AVE , SATELLITE BEACH 32937
    pprint.pprint(get_bcpaco_item('2807458'))
    pprint.pprint(get_bcpaco_item('2630481'))
    # get_bcpaco_item('2613083')
    # # get_bcpaco_item('2630481')
    # print(get_cpao_query_link_by_acct(acct))


    # print('done')

if __name__ == '__main__':
    # sys.exit(main())
    unittest.main()