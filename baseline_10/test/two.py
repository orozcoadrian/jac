import logging
import unittest
import itertools
import re
import urllib
from bs4 import BeautifulSoup
import requests


def get_legal_from_str(the_str):
    legal_desc = the_str.replace(u'\xc2',u'')
    # logging.info('get_legal_from_str('+legal_desc+')')
    ret={}

    m = re.search('(LT (?P<lt>[0-9a-zA-Z]+) )?(BLK (?P<blk>[0-9a-zA-Z]+) )?(PB (?P<pb>\d+) PG (?P<pg>\d+))?(?P<subd>.*) S (?P<s>\d+) T (?P<t>\d+G?) R (?P<r>\d+)( SUBID (?P<subid>[0-9a-zA-Z]+))?', the_str)
    if m:
        ret = dict(itertools.chain(ret.items(), m.groupdict().items()))
    elif 'condo'.upper() in the_str.upper():
        ret['condo']=True
#     print('ret='+str(ret))
    ret['legal_desc']=legal_desc
    return ret

def get_new_acct_by_legal(legal):
    sub, lot, block, pb, pg, s, t, r, subid = legal
    sub = sub.replace(u'\xc2', u'').encode('utf-8')
    logging.info('get_legacy_acct_by_legal(sub="'+sub+'", lot='+str(lot)+', block='+str(block)+', pb='+str(pb)+', pg='+str(pg)+', s='+str(s)+', t='+str(t)+', r='+str(r)+', subid='+str(subid)+')')

    ret=''
    url = 'https://www.bcpao.us/asp/find_property.asp'
    # headers = {
    #     # 'Cookie': 'CFID='+cfid+'; CFTOKEN='+cftoken,
    #     'Cookie': 'ASPSESSIONIDQABRBBSS=ELGLAMBAELLCGOLCONGKOFHE',
    #     'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    if not ret:
        data=None
        offset=82
        if pg is not None:
            data='SearchBy=Sub&sub='+urllib.quote(sub)+'&pg='+str(pg)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
        print('request:')
        print(' url: '+url)
        # print(' headers: '+str(headers))
        print(' data: '+str(data))
        req = requests.post(url, data=data, verify=False)
        soup = BeautifulSoup(req.text.encode('utf-8'), 'html.parser')
        print(soup)
        print(soup.prettify())

class MyTestCase(unittest.TestCase):
    def test_something(self):
        legal_str = 'LT 29 PB 35 PG 87 ISLAND OAKS SUBDIVISION S 26 T 24 R 36 SUBID 60'
        print(legal_str)
        legal = get_legal_from_str(legal_str)
        print(legal)
        acct = get_new_acct_by_legal((legal['subd'], legal['lt'], legal['blk'], legal['pb'], legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid']))
        print(acct)
        self.assertEqual('2420533', acct)


if __name__ == '__main__':
    unittest.main()


    ### 1
    # bclerk:
    # http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=1%2F1%2F1981&ed=5%2F31%2F2015&n=&bt=OR&d=5%2F31%2F2014&pt=-1&cn=05-2009-CA-070435-XXXX-XX&dt=ALL%20DOCUMENT%20TYPES&st=casenumber&ss=ALL%20DOCUMENT%20TYPES
    # scheme: http
    # Host	web1.brevardclerk.us
    # Path	/oncoreweb/search.aspx
    # Query String
    # bd=1%2F1%2F1981
    # ed=5%2F31%2F2015
    # n=
    # bt=OR
    # d=5%2F31%2F2014
    # pt=-1
    # cn=05-2009-CA-070435-XXXX-XX
    # dt=ALL%20DOCUMENT%20TYPES
    # st=casenumber
    # ss=ALL%20DOCUMENT%20TYPES
    # Filename	search.aspx
    # LT 29 PB 35 PG 87 ISLAND OAKS SUBDIVISION S 26 T 24 R 36 SUBID 60

    # bcpao search:
    # Plat Book: 35
    # Page: 87
    # Block: <blank>
    # Lot: 29
    # result: 2420533

    # bcpao:
    # https://www.bcpao.us/PropertySearch/#/parcel/basic/2420533
    #                T  R  S Subid bl lot
    # Parcel ID:	24-36-26-60-*-29
    # Query: group=subdivision&code=24 362660&twp=24&rng=36&sec=26
    # https://www.bcpao.us/propertysearch/#/search/advanced/group=subdivision&code=24%20362660&twp=24&rng=36&sec=26
    # 24-36-26-60-00000.0-0029.00
    # bcpao result: 320 ISLAND OAKS PL , MERRITT ISLAND 32953

    # tax:
    # https://brevard.county-taxes.com/public/real_estate/parcels/2420533
    # 24 362660 29 320 ISLAND OAKS PL ISLAND OAKS SUBDIVISION MERRITT ISLAND LOT 29
    # geo number: 24 362660 29
    # block: 00000.0
    # lot: 0029.00

    # searching in the tax website with the legal description seems promising. the format seems to be: t,space,r,s,subid,space,block,space,lot
    #                T  RSSubid bl lot
    # tax legal:	24 362660 29

    # parcel id:
    # Township-Range-Section-Subdivision-Block-lot/tract (for subdivision parcels)
    # Township-Range-Section-00-parcel (for meets & bounds parcels).



    ### 2
    # foreclosures:
    # http://vweb2.brevardclerk.us/Foreclosures/foreclosure_sales.html
    # CITIMORTGAGE VS GREG BURDETTE
    # 05-2010-CA-027087-XXXX-XX


    # bclerk:
    # http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=1%2F1%2F1981&ed=3%2F5%2F2016&bt=OR&d=3%2F5%2F2016&pt=-1&cn=05-2010-CA-027087-XXXX-XX&st=casenumber
    # LT 12 BLK 269 PB 14 PG 142 PORT MALABAR UNIT 8 S 32 T 28 R 37 SUBID FS
    # orig mtg: http://199.241.8.220/ImageView/ViewImage.aspx?barcodeid=SkPlYNX0Xc+ruRYv4suKxg==&theKey=JmZL5mBWkwqoRWZhuAtjXA==&theIV=UGxDS2V5V1NQbENLZXlXUw==&uid=999999997
    # address: 785 crestline lane ne palm bay, fl 32907

    # bcpao
    # Parcel ID: T  R  S Subid bl lot
    #           28 37 32 FS 269 12
    #           28-37-32-FS-269-12
    # Account: 2841896
    # Site Address:	785 Crestline Ln Ne Palm Bay 32907
    # Parcel ID:	28-37-32-FS-269-12
    # EX: 20-34-04-00-00002.0-000X.XX

    # taxes:
    # https://brevard.county-taxes.com/public/real_estate/parcels/2841896
    # 28 3732FS 269 12 NE 785 CRESTLINE LN PORT MALABAR UNIT 8 PALM BAY LOT 12 BLK 269
    # geo: 28 3732FS 269 12



    ## 3

    # foreclosures:
    # http://vweb2.brevardclerk.us/Foreclosures/foreclosure_sales.html
    # 05-2010-CA-034261-XXXX-XX
    # BAC HOME VS MANSFIELD GOTT

    # case search:
    # orig mtg: http://199.241.8.220/ImageView/ViewImage.aspx?barcodeid=4CEMgriFdaC+Op0pNqEBZQ==&theKey=6Ym3cwMbkkaYqRX6xw8vYg==&theIV=UGxDS2V5V1NQbENLZXlXUw==&uid=999999997
    # 775 jacaranda st, merritt island, fl 32952

    # bclerk:
    # http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=1%2F1%2F1981&ed=3%2F5%2F2016&bt=OR&d=3%2F5%2F2016&pt=-1&cn=05-2010-CA-034261-XXXX-XX&st=casenumber
    # LT 30 BLK B PB 16 PG 132 VETTER ISLES ESTS SEC 2 S 30 T 24 R 37 SUBID 88

    # Parcel ID: T  R  S Subid bl lot
    #           24 37 30 88   B  30

    # bcpao:
    # https://www.bcpao.us/PropertySearch/#/parcel/basic/2438102
    # Parcel ID:	24-37-30-88-B-30
    # Parcel ID:	24 37 30 88 B 30



    ### 4:
    # 05-2011-CA-042139-XXXX-XX	CITIMORTGAGE VS G PENNINGTON
    # tract of land?

    ### 5:
    # 05-2011-CA-042188-XXXX-XX	WELLS FARGO VS FRANK GUARAGNO

    # orig mtg: http://199.241.8.220/ImageView/ViewImage.aspx?barcodeid=4U4QbE714gqnnViSaj17wg==&theKey=7Z2nJL8YB8UZCRWTLG2tKQ==&theIV=UGxDS2V5V1NQbENLZXlXUw==&uid=999999997
    # 602 wedelia dr barefoot bay fl 32976

    # LT 2 BLK 75 PB 22 PG 116 BAREFOOT BAY UNIT 2 PART 11 S 10 T 30 R 38 SUBID JT
    # Parcel ID: T  R  S Subid bl lot
    #           30 38 10 JT 75 2
    #           30-38-10-JT-75-2


    # 22-35-03-XY-4251-12.3
    # 22 35 03 XY 4251 12.3
    # 22-35-03-00-123
    # 22 35 03 00 123.4