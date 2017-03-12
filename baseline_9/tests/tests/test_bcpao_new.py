import json
import pprint
import unittest

import requests

import jac.bcpao
import jac.bclerk


class MyTestCase(unittest.TestCase):
    def test_condo_new_bcpao(self):
        # BLK 123 U 135 NW 1/4 OF NW 1/4 & NE 1/4 OF PINEDA OCEAN CLUB CONDO PH I ORB 2211/2194 S 23 T 26 R 37 SUBID 00
        # https://bcpao.us/api/v1/condos?draw=5&columns%5B0%5D%5Bdata%5D=condoNumber&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=commonPropertyID&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=condoName&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=location&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=totalBuildings&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=totalUnits&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=50&search%5Bvalue%5D=pineda&search%5Bregex%5D=false&_=1484619285354
        url = 'https://bcpao.us/api/v1/condos?'
        # url += 'draw=5'

        # url += '&columns%5B0%5D%5Bdata%5D=condoNumber'
        # url += '&columns%5B0%5D%5Bname%5D='
        # url += '&columns%5B0%5D%5Bsearchable%5D=true'
        # url += '&columns%5B0%5D%5Borderable%5D=true'
        url += 'columns%5B0%5D%5Bsearch%5D%5Bvalue%5D='
        # url += '&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false'

        # url += '&columns%5B1%5D%5Bdata%5D=commonPropertyID'
        # url += '&columns%5B1%5D%5Bname%5D='
        # url += '&columns%5B1%5D%5Bsearchable%5D=true'
        # url += '&columns%5B1%5D%5Borderable%5D=true'
        url += '&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D='
        # url += '&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false'

        # url += '&columns%5B2%5D%5Bdata%5D=condoName'
        # url += '&columns%5B2%5D%5Bname%5D='
        # url += '&columns%5B2%5D%5Bsearchable%5D=true'
        # url += '&columns%5B2%5D%5Borderable%5D=true'
        url += '&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D='
        # url += '&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false'

        # url += '&columns%5B3%5D%5Bdata%5D=location'
        # url += '&columns%5B3%5D%5Bname%5D='
        # url += '&columns%5B3%5D%5Bsearchable%5D=true'
        # url += '&columns%5B3%5D%5Borderable%5D=true'
        url += '&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D='
        # url += '&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false'

        # url += '&columns%5B4%5D%5Bdata%5D=totalBuildings'
        # url += '&columns%5B4%5D%5Bname%5D='
        # url += '&columns%5B4%5D%5Bsearchable%5D=true'
        # url += '&columns%5B4%5D%5Borderable%5D=true'
        url += '&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D='
        # url += '&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false'

        # url += '&columns%5B5%5D%5Bdata%5D=totalUnits'
        # url += '&columns%5B5%5D%5Bname%5D='
        # url += '&columns%5B5%5D%5Bsearchable%5D=true'
        # url += '&columns%5B5%5D%5Borderable%5D=true'
        url += '&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D='
        # url += '&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false'

        # url += '&order%5B0%5D%5Bcolumn%5D=0'
        url += '&order%5B0%5D%5Bdir%5D=asc'
        url += '&start=0'
        url += '&length=50'
        url += '&search%5Bvalue%5D=pineda'
        # url += '&search%5Bregex%5D=false'
        # url += '&_=1484619285354'
        headers = ''  # get_headers(cfid, cftoken)
        data = ''  # get_data(year, court_type, seq_number)
        #     r = requests.post(url, data, headers=headers, stream=True)
        # print('url='+url)
        r = requests.get(url)
        # print(r.text)
        parsed_json = json.loads(r.text)
        pprint.pprint('hi')
        self.assertEqual(5, len(parsed_json['data']))
        self.assertEqual('PINEDA OCEAN CLUB CONDO PH I', parsed_json['data'][0]['condoName'].strip())
        self.assertEqual(2621090, parsed_json['data'][0]['commonPropertyID'])
        self.assertEqual('101-135 HWY A1A, SATELLITE BCH, 32937', parsed_json['data'][0]['location'])

    # def test_condo_legal_new_bcpao(self):
    #     legal_str = 'BLK 123 U 135 NW 1/4 OF NW 1/4 & NE 1/4 OF PINEDA OCEAN CLUB CONDO PH I ORB 2211/2194 S 23 T 26 R 37 SUBID 00'
    #     legal = jac.bclerk.get_legal_from_str(legal_str)
    #     self.assertEqual({'subid': '00',
    #                       'legal_desc': u'BLK 123 U 135 NW 1/4 OF NW 1/4 & NE 1/4 OF PINEDA OCEAN CLUB CONDO PH I ORB 2211/2194 S 23 T 26 R 37 SUBID 00',
    #                       'lt': None,
    #                       'pb': None,
    #                       's': '23',
    #                       'r': '37',
    #                       'pg': None,
    #                       'blk': '123',
    #                       'subd': 'NW 1/4 OF NW 1/4 & NE 1/4 OF PINEDA OCEAN CLUB CONDO PH I',
    #                       't': '26',
    #                       'u': '135',
    #                       'orb': '2211/2194'},
    #                      legal)
        # 2621090	PINEDA OCEAN CLUB CONDO PH I	101-135 HWY A1A, SATELLITE BCH, 32937


if __name__ == '__main__':
    unittest.main()
