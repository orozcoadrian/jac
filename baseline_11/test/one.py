import json
import pprint
import re
import unittest
import urllib

import itertools
import requests

def get_legal_dict_from_str(the_str):
    legal_desc = the_str.replace(u'\xc2',u'')
    print('get_legal_from_str('+legal_desc+')')
    ret={}

    m = re.search('(LT (?P<lt>[0-9a-zA-Z]+) )?(BLK (?P<blk>[0-9a-zA-Z]+) )?(PB (?P<pb>\d+) PG (?P<pg>\d+))?(?P<subd>.*) S (?P<s>\d+) T (?P<t>\d+G?) R (?P<r>\d+)( SUBID (?P<subid>[0-9a-zA-Z]+))?', the_str)
    if m:
        # pprint.pprint(m)
        # pprint.pprint(m.groups())
        # print(m.group('blk'))
        # return m.groupdict()
        # ret = dict(itertools.chain(ret.items(), m.groupdict().items()))
        ret = m.groupdict()

        # print(m.group(1)+','+m.group(2)+','+m.group(3))
        # ret['lt']=m.group(1)
        # ret['blk']=m.group(2)
        # ret['subd']=m.group(3)
        # ret['subid']=m.group(4)
    # elif 'condo'.upper() in the_str.upper():
        # ret['condo']=True
#     print('ret='+str(ret))
#     ret['legal_desc']=legal_desc
    return ret

def get_legal_tuple_from_legal_dict(l):
    return (l['subd'], l['lt'], l['blk'], l['pb'], l['pg'], l['s'], l['t'], l['r'], l['subid'])

def get_acct_by_legal_tuple(legal):
    print('get_acct_by_legal_tuple('+str(legal)+')')
    sub, lot, block, pb, pg, s, t, r, subid = legal
    print('get_acct_by_legal_tuple(sub="' + sub + '", lot=' + str(lot) + ', block=' + str(block) + ', pb=' + str(
        pb) + ', pg=' + str(pg) + ', s=' + str(s) + ', t=' + str(t) + ', r=' + str(r) + ', subid=' + str(subid) + ')')

    # (Township - Range - Section - Subdivision - block - lot)
    # url = 'https://www.bcpao.us/api/search?parcel='+t+'-'+r+'-'+s+'-'+subid+'-'+block+'-'+lot+''
    url2 = 'https://bcpao.us/api/v1/search?'
    if lot is not None:
        url2 += 'lot=' + str(lot)
    if block is not None:
        url2 += '&blk=' + str(block)
    if pb is not None:
        url2 += '&platbook=' + str(pb)
    if pg is not None:
        url2 += '&platpage=' + str(pg)
    url2 += '&subname=' + urllib.quote(sub)
    url2 += '&activeonly=true&size=10&page=1'
    headers = ''  # get_headers(cfid, cftoken)
    data = ''  # get_data(year, court_type, seq_number)
    #     r = requests.post(url, data, headers=headers, stream=True)
    print('url2='+url2)
    r = requests.get(url2)
    # print(r.text)
    return r.text

def get_parcelData_by_acct(acct):
    print('get_parcelData_by_acct('+str(acct)+')')
    # (Township - Range - Section - Subdivision - block - lot)
    # url = 'https://www.bcpao.us/api/search/parcelData?account='+str(acct)+''
    url = 'https://bcpao.us/api/v1/account/' + str(acct) + ''
    headers = ''  # get_headers(cfid, cftoken)
    data = ''  # get_data(year, court_type, seq_number)
    #     r = requests.post(url, data, headers=headers, stream=True)
    print('url='+url)
    r = requests.get(url)
    # print(r.text)
    return r.text

class MyTestCase(unittest.TestCase):
    def test_first(self):
        # https://www.bcpao.us/api/search/parcelData?account=2605634
        # https://www.bcpao.us/PropertySearch/#/parcel/2605634
        # url = 'https://www.bcpao.us/api/search/parcelData?account=2605634'
        url = 'https://www.bcpao.us/api/v1/search?parcel=26-36-36-50-*-415'
        # url = 'https://www.bcpao.us/api/search/parcelData?parcel=26-36-36-50-*-415'
        headers = ''  # get_headers(cfid, cftoken)
        data = ''  # get_data(year, court_type, seq_number)
        #     r = requests.post(url, data, headers=headers, stream=True)
        r = requests.get(url)
        print(r.text)
        # self.assertEqual(True, False)

    def test_legal(self):
        #                       T  R  S  SUBID  BLK  LOT
        #         Parcel ID:    28-36-26-KN-02134.0-0028.00
        #                       sub,                    lot,  block,  pb,   pg     Sec   Twn  Rng
        i = get_acct_by_legal_tuple(('PORT MALABAR UNIT 42', '28', '2134', '21', '105', '26', '28', '36', '00'))
        pprint.pprint(i)
        parsed_json = json.loads(i)
        self.assertEqual(parsed_json[0]['account'], '2807459')

    def test_one(self):
        # 05-2010-CA-012850
        # LT 46 BLK 6 PB 20 PG 115 IXORA PARK PLAT NO 4 S 20 T 27 R 37 SUBID 55
        # T  R  S  SUBID  BLK  LOT
        # 27-37-20-55-6-46
        # 1783 S Dodge Cir Melbourne FL 32935
        # 2723697
        legal_str = 'LT 46 BLK 6 PB 20 PG 115 IXORA PARK PLAT NO 4 S 20 T 27 R 37 SUBID 55'
        legal_dict = get_legal_dict_from_str(legal_str)
        print(legal_dict)
        legal_tuple = get_legal_tuple_from_legal_dict(legal_dict)
        i = get_acct_by_legal_tuple(legal_tuple)
        print(i)
        parsed_json = json.loads(i)
        addr = parsed_json[0]['siteAddress']
        print(addr)
        self.assertEqual('1783 S DODGE CIR MELBOURNE FL 32935', addr)
        self.assertEqual('2723697', parsed_json[0]['account'])
        pd = get_parcelData_by_acct(parsed_json[0]['account'])
        print(pd)
        parsed_json2 = json.loads(pd)
        print(parsed_json2['valueSummary'][0]['marketVal'])
        self.assertEqual(110060.0, parsed_json2['valueSummary'][0]['marketVal'])




if __name__ == '__main__':
    unittest.main()
