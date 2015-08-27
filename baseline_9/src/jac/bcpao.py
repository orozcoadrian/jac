# http://askubuntu.com/questions/116020/python-https-requests-urllib2-to-some-sites-fail-on-ubuntu-12-04-without-proxy
import ssl
ssl.PROTOCOL_SSLv23 = ssl.PROTOCOL_TLSv1

# http://stackoverflow.com/questions/30904815/having-ssl-problems-with-requests-get-in-python     and     http://docs.python-requests.org/en/latest/user/advanced/
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

import requests


#import sys
#import os

#from time import strftime
import re
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
import logging
import time



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



def convertBlock(block):
    blk_str = block
    if block:
        m = re.search('^(?P<num>[\0-9]+)(?P<letter>[A-Z])$', block)
        if m:
            block = m.group('num') + '.' + m.group('letter')
    #     if block and block.endswith('S'):
    #         block = block[:-1] + '.S'
    #     elif block and block.endswith('F'):
    #         block = block[:-1] + '.F'
    #     elif block and block.endswith('J'):
    #         block = block[:-1] + '.J'
    #     elif block and block.endswith('L'):
    #         block = block[:-1] + '.L'
    #     elif block and block.endswith('U'):
    #         block = block[:-1] + '.U'
    #     elif block and block.endswith('K'):
    #         block = block[:-1] + '.K'


    #     if block and len(block) == 4 and '.' not in block:
    #         print 'block is length 4'
    #         block = block[0:3] + '.' + block[3:4]
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

def get_accts_by_legal_by_sub__subname_lot_block(legal):
    sub, lot, block, pb, pg, s, t, r, subid = legal
    sub = sub.replace(u'\xc2', u'').encode('utf-8')
    print('get_accts_by_legal_by_sub__subname_lot_block(sub="'+sub+'", lot='+str(lot)+', block='+str(block)+', pb='+str(pb)+', pg='+str(pg)+', s='+str(s)+', t='+str(t)+', r='+str(r)+', subid='+str(subid)+')')
    ret=''

#         if pb is not None and pg is not None and lot is not None and block is not None:
#             data='SearchBy=Plat&book='+str(pb)+'&page='+str(pg)+'&blk='+str(block)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
#             offset=86
    print('manual: https://www.bcpao.us/asp/real_search.asp')
    print('pull down: "Subdivision Name, Lot & Block"')
    if sub and lot and block:
        print('Sub Name: ' + sub)
        print('block: ' + block)
        print('lot: ' + lot)
        data='SearchBy=Sub&sub='+urllib.quote(sub)+'&blk='+str(block)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'

        bcpao_results_string = get_bcpao_results_string(data)
#         soup = BeautifulSoup(bcpao_results_string, 'html.parser')
        ret = get_results_from_bcpao_results_string(bcpao_results_string)
    return ret

def get_acct_by_legal_by_sub__sub_block_lot(legal):
    sub, lot, block, pb, pg, s, t, r, subid = legal
    sub = sub.replace(u'\xc2', u'').encode('utf-8')
    print('get_acct_by_legal_by_sub(sub="'+sub+'", lot='+str(lot)+', block='+str(block)+', pb='+str(pb)+', pg='+str(pg)+', s='+str(s)+', t='+str(t)+', r='+str(r)+', subid='+str(subid)+')')
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
        if sub and lot and block:
            data='SearchBy=Sub&sub='+urllib.quote(sub)+'&blk='+str(block)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'

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
        print(str(len(aerials)))
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
    return ret


def get_results_from_bcpao_results_string(bcpao_results_string):
#     print(bcpao_results_string)
    ret = []
    soup = BeautifulSoup(bcpao_results_string, 'html.parser')
    table = soup.find('table', border='1')
    if table:
        trs = table.find_all(   'tr')

        for index, item in enumerate(trs):
            tds = item.find_all('td')
            if len(tds) > 0:
                acct = tds[2].a.string
                name = str(tds[3].contents[0])
                addr = str(tds[4].contents[0])
                pid = str(tds[5].contents[0])
                if len(acct) > 0:
                    acct = acct.replace('<br/>', '')
                if len(name) > 0:
                    name = name.replace('<br/>', '')
                if len(addr) > 0:
                    addr = addr.replace('<br/>', '')
                if len(pid) > 0:
                    pid = pid.replace('<br/>', '')
                my_ret_item = {}
                my_ret_item['acct'] = acct
                my_ret_item['name'] = name
                my_ret_item['addr'] = addr
                my_ret_item['pid'] = pid
                ret.append(my_ret_item)

    return ret


def get_bcpao_results_string(data):
    url = 'https://www.bcpao.us/asp/find_property.asp'
    headers = { # 'Cookie': 'CFID='+cfid+'; CFTOKEN='+cftoken,
        'Cookie':'ASPSESSIONIDQABRBBSS=ELGLAMBAELLCGOLCONGKOFHE',
        'Content-Type':'application/x-www-form-urlencoded'}
    print 'url: ' + url
    print 'data: ' + data
    req = requests.post(url, headers=headers, data=data)
    bcpao_results_string = req.text.encode('utf-8')
    return bcpao_results_string

def get_accts_by_legal_by_sub__sub_pg_lot(legal):
    sub, lot, block, pb, pg, s, t, r, subid = legal
    sub = sub.replace(u'\xc2', u'').encode('utf-8')
    print('get_accts_by_legal_by_sub__sub_pg_lot(sub="'+sub+'", lot='+str(lot)+', block='+str(block)+', pb='+str(pb)+', pg='+str(pg)+', s='+str(s)+', t='+str(t)+', r='+str(r)+', subid='+str(subid)+')')




    ret=[]
    data=None
    print('manual: https://www.bcpao.us/asp/real_search.asp')
    print('pull down: "Subdivision Name, Lot & Block"')
    if sub and pg and lot:
        print('sub: ' + sub)
        print('pg: ' + pg)
        print('lot: ' + lot)
        data='SearchBy=Sub&sub='+urllib.quote(sub)+'&pg='+str(pg)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'

        bcpao_results_string = get_bcpao_results_string(data)
        ret = get_results_from_bcpao_results_string(bcpao_results_string)
    return ret

def get_accts_by_legal_by_plat__pb_pg_lot_block(legal):
    sub, lot, block, pb, pg, s, t, r, subid = legal
    sub = sub.replace(u'\xc2', u'').encode('utf-8')
    print('get_accts_by_legal_by_plat__pb_pg_lot_block(sub="'+sub+'", lot='+str(lot)+', block='+str(block)+', pb='+str(pb)+', pg='+str(pg)+', s='+str(s)+', t='+str(t)+', r='+str(r)+', subid='+str(subid)+')')

    ret=[]
    data=None
    print('manual: https://www.bcpao.us/asp/real_search.asp')
    print('pull down: "Plat Book/Page, Lot & Block"')
    if pb and pg and lot:
        print('pb: ' + pb)
        print('pg: ' + pg)

        print('lot: ' + lot)
        block_str = ''
        if block:
            print('block: ' + block)
            block_str = str(block)

        data='SearchBy=Plat&blk='+block_str+'&page='+str(pg)+'&book='+str(pb)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'

        bcpao_results_string = get_bcpao_results_string(data)
        ret = get_results_from_bcpao_results_string(bcpao_results_string)
    return ret

def get_accts_by_legal_by_pid__t_r_s_subid_block_lot(legal):
    sub, lot, block, pb, pg, s, t, r, subid = legal
    sub = sub.replace(u'\xc2', u'').encode('utf-8')
    print('get_accts_by_legal_by_pid__t_r_s_subid_block_lot(sub="'+sub+'", lot='+str(lot)+', block='+str(block)+', pb='+str(pb)+', pg='+str(pg)+', s='+str(s)+', t='+str(t)+', r='+str(r)+', subid='+str(subid)+')')

    ret=[]
    data=None
    print('manual: https://www.bcpao.us/asp/real_search.asp')
    print('pull down: "Parcel Id"')
    if t and r and s:
#         print('pb: ' + pb)
#         print('pg: ' + pg)

#         print('lot: ' + lot)

        print('t: ' + t)
        print('r: ' + r)
        print('s: ' + s)

        subid_str = ''
        if subid:
            print('subid: ' + subid)
            subid_str = str(subid)

        blk_str = convertBlock(block)
        if not blk_str:
            blk_str = ''

        lot_str = convertLot(lot)


#         print('subid: ' + subid)
        print('block: ' + blk_str)
        print('lot: ' + lot_str)
        data='SearchBy=PID&twp='+str(t)+'&rng='+str(r)+'&sec='+str(s)+'&subn='+subid_str+'&blk='+str(blk_str)+'&lot='+str(lot_str)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'

        bcpao_results_string = get_bcpao_results_string(data)
        ret = get_results_from_bcpao_results_string(bcpao_results_string)
    return ret

def get_acct_by_legal_by_sub__sub_pg_lot(legal):
    sub, lot, block, pb, pg, s, t, r, subid = legal
    sub = sub.replace(u'\xc2', u'').encode('utf-8')
    print('get_acct_by_legal_by_sub(sub="'+sub+'", lot='+str(lot)+', block='+str(block)+', pb='+str(pb)+', pg='+str(pg)+', s='+str(s)+', t='+str(t)+', r='+str(r)+', subid='+str(subid)+')')
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
        if pg is not None:
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
    return ret

def get_acct_by_legal(legal):
    use_local_logging_config = False
    if use_local_logging_config:
        logging.basicConfig(format='%(asctime)s %(module)-15s %(levelname)s %(message)s', level=logging.DEBUG)
    #     logging.getLogger().setLevel(logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.info('START')
    sub, lot, block, pb, pg, s, t, r, subid = legal
    sub = sub.replace(u'\xc2', u'').encode('utf-8')
    logging.info('get_acct_by_legal(sub="'+sub+'", lot='+str(lot)+', block='+str(block)+', pb='+str(pb)+', pg='+str(pg)+', s='+str(s)+', t='+str(t)+', r='+str(r)+', subid='+str(subid)+')')
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
#         elif t and r and s and subid and lot:
#             data='SearchBy=Sub&sub='+urllib.quote(sub)+'&blk=&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'

        elif pg is not None:
            data='SearchBy=Sub&sub='+urllib.quote(sub)+'&pg='+str(pg)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
        # r = requests.post(url, data, stream=True)
        # time.sleep(1)
        req = requests.post(url, headers=headers, data=data, verify=False)
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
        blk_str = convertBlock(block)
        if not blk_str:
            blk_str = ''
        lot_str = convertLot(lot)
        data='SearchBy=PID&twp='+str(t)+'&rng='+str(r)+'&sec='+str(s)+'&subn='+str(subid)+'&blk='+str(blk_str)+'&lot='+str(lot_str)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
        req = requests.post(url, headers=headers, data=data)
        # the_url="https://www.bcpao.us/asp/find_property.asp?"+'SearchBy=Sub&sub='+urllib.quote(sub)+'&blk='+str(block)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
        print(data)
        soup = BeautifulSoup(req.text.encode('utf-8'), 'html.parser')
#         print(soup.prettify())
#         print_headers(the_url, 'html.parser')
        rers_cell = soup.find(text="Real Estate Records Search")
        #print_small_texts(list(rers_cell.parent.parent.parent.parent.parent.descendants), max=50)
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
    the_url="http://www.bcpao.us/asp/Show_parcel.asp?"+'acct='+acct+'&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Address'

    print(the_url)
    f = urlopen(the_url)
    html = f.read().replace(u'\xa0', u'').encode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    try:
        # time.sleep(1)

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
        # time.sleep(1)
        # with closing(urlopen(the_url)) as f:
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
        # soup = BeautifulSoup(html, 'lxml')
    # soup = BeautifulSoup(urlopen(the_url))
    #     print('test test test adrian ' + data)
    #     print(soup.prettify())
        # print('one two three')
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
            ret['latest market value total']=str(list(vs_cell.parent.parent.parent.parent.descendants)[38])
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
            # print_small_texts(list(bai_cell.parent.parent.parent.parent.descendants))
            ret['total base area']=str(list(bai_cell.parent.parent.parent.parent.descendants)[93])
    except:
        raise

    # print(ret)

    try:
        if 'latest market value total' not in ret:
            # with closing(urlopen(the_url)) as f:
            soup = BeautifulSoup(html, "html.parser")
            mvt = soup.find(text="Market Value Total:")
            # for index,item in enumerate(list(mvt.parent.parent.descendants)):
                # print('list(gpc.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
            if mvt:
                ret['latest market value total']=str(list(mvt.parent.parent.descendants)[13])

        if 'latest market value total' not in ret:
            # with closing(urlopen(the_url)) as f:
            #     html = f.read().replace(u'\xa0', u'').encode('utf-8')
            filtered=[]
            for l in html.split('\n'):
                if 'Homestead' not in l and 'tdHeader_Row_1_Col_1' not in l:
                    filtered.append(l.replace(u'\xa0', u'').encode('utf-8'))
                # else:
                    # print('filtering: '+l)
            soup = BeautifulSoup(''.join(filtered), "lxml")
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
        # f = urlopen(the_url)
        # html = f.read()
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
        # time.sleep(1)
        soup = BeautifulSoup(html, 'html.parser')
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
        # time.sleep(1)
        soup = BeautifulSoup(html, 'html.parser')
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
            ret['frame code']=list(bi_cell.parent.parent.parent.parent.parent.descendants)[65].parent.parent.get_text().encode('utf-8')
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

def fill_bcpao_from_legal(mr):
    legal = mr.item['legal']
    if 'subd' in legal:
        acc = get_acct_by_legal((legal['subd'], legal['lt'], legal['blk'], legal['pb'], legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid']))
        # logging.debug('a: ' + (str(acc) if acc else 'None'))
        mr.item['bcpao_acc'] = acc
        mr.item['bcpao_item'] = get_bcpaco_item(acc)
    #mr.item['bcpao_radius'] = bcpao_radius.get_average_from_radius(mr.item['bcpao_acc'])
    # logging.debug('asdfasd 1.5 ' + pprint.pformat(mr.item))
    legals = mr.item['legals']
    # logging.debug('legals: ' + pprint.pformat(legals))
    # logging.debug('** * * ****   4563456')
    mr.item['bcpao_accs'] = []
    for i, l in enumerate(legals):
        # logging.debug(pprint.pformat(l))
        acc = None
        if 't' in l:
            acc = get_acct_by_legal((l['subd'], l['lt'], l['blk'], l['pb'], l['pg'], l['s'], l['t'], l['r'], l['subid']))
            mr.item['bcpao_accs'].append(acc)
            if 'bcpao_acc' not in mr.item:
                mr.item['bcpao_acc'] = acc
                mr.item['bcpao_item'] = get_bcpaco_item(acc)
                # logging.debug('choosing a secondary legal description because it gave a bcpao_acc')
        # logging.debug(str(i) + ': ' + ('None' if not acc else str(acc)))

    # logging.debug('asdfasd 222 ' + pprint.pformat(mr.item))

def get_legal_tuple(legal):
    return (legal['subd'], legal['lt'], legal['blk'], legal['pb'], legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])

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