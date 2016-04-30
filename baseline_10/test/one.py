# http://askubuntu.com/questions/116020/python-https-requests-urllib2-to-some-sites-fail-on-ubuntu-12-04-without-proxy
import ssl
ssl.PROTOCOL_SSLv23 = ssl.PROTOCOL_TLSv1

import logging
import re
import itertools
import urllib
from bs4 import BeautifulSoup
import requests




def get_legal_from_str(the_str):
    legal_desc = the_str.replace(u'\xc2',u'')
    logging.info('get_legal_from_str('+legal_desc+')')
    ret={}

    m = re.search('(LT (?P<lt>[0-9a-zA-Z]+) )?(BLK (?P<blk>[0-9a-zA-Z]+) )?(PB (?P<pb>\d+) PG (?P<pg>\d+))?(?P<subd>.*) S (?P<s>\d+) T (?P<t>\d+G?) R (?P<r>\d+)( SUBID (?P<subid>[0-9a-zA-Z]+))?', the_str)
    if m:
        ret = dict(itertools.chain(ret.items(), m.groupdict().items()))
    elif 'condo'.upper() in the_str.upper():
        ret['condo']=True
#     print('ret='+str(ret))
    ret['legal_desc']=legal_desc
    return ret

def get_legacy_acct_by_legal(legal):
    sub, lot, block, pb, pg, s, t, r, subid = legal
    sub = sub.replace(u'\xc2', u'').encode('utf-8')
    logging.info('get_legacy_acct_by_legal(sub="'+sub+'", lot='+str(lot)+', block='+str(block)+', pb='+str(pb)+', pg='+str(pg)+', s='+str(s)+', t='+str(t)+', r='+str(r)+', subid='+str(subid)+')')
    ret=''

    # url = 'https://legacy.bcpao.us/asp/find_property.asp'
    url = 'https://legacy.bcpao.us/asp/find_property.asp'
    headers = {
        # 'Cookie': 'CFID='+cfid+'; CFTOKEN='+cftoken,
        'Cookie': 'ASPSESSIONIDQABRBBSS=ELGLAMBAELLCGOLCONGKOFHE',
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    if not ret:
        data=None
        offset=82
        if pg is not None:
            data='SearchBy=Sub&sub='+urllib.quote(sub)+'&pg='+str(pg)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
        print('request:')
        print(' url: '+url)
        print(' headers: '+str(headers))
        print(' data: '+str(data))
        req = requests.post(url, headers=headers, data=data, verify=False)
        soup = BeautifulSoup(req.text.encode('utf-8'), 'html.parser')
        rers_cell = soup.find(text="Real Estate Records Search")
        aerials = soup.find_all('a', text="Aerial")
        if aerials and len(aerials) > 1:
            # need to ignore this whole page if we have more than one result. can search for how many "Aerial" there are
            print('ignoring this whole page because we have more than one result (tax ids)')
            rers_cell = None
        if rers_cell is not None:
            ret=str(list(rers_cell.parent.parent.parent.parent.parent.descendants)[offset])
    if not ret:
        print('no bcpao acct, no address')

    return ret

def convertBlock(block):
    blk_str = block
    if block:
        m = re.search('^(?P<num>[\0-9]+)(?P<letter>[A-Z])$', block)
        if m:
            block = m.group('num') + '.' + m.group('letter')
        if block:
            blk_str = block
    return blk_str

def convertLot(lot):
    lot_str = ''
    if lot and len(lot) == 4 and '.' not in lot:
        print 'lot is length 4'
        lot = lot[0:2] + '.' + lot[2:4]
    if lot:
        lot_str = lot
    return lot_str



import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        legal_str = 'LT 29 PB 35 PG 87 ISLAND OAKS SUBDIVISION S 26 T 24 R 36 SUBID 60'
        print(legal_str)
        legal = get_legal_from_str(legal_str)
        print(legal)
        acct = get_legacy_acct_by_legal((legal['subd'], legal['lt'], legal['blk'], legal['pb'], legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid']))
        print(acct)
        self.assertEqual('2420533', acct)


if __name__ == '__main__':
    unittest.main()



