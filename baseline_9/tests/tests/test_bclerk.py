'''
Created on Nov 10, 2014

@author: Adrian
'''
import unittest
import jac.bclerk
import jac.myutils
from bs4 import BeautifulSoup
import logging
import pprint
import re


class Test(unittest.TestCase):




    def test0(self):
        #@unittest.skip("this test was written against an implementation that used JUDGMENT REAL PROPERTY. using jrp you get lot 5 but using lis pendens you get lot 8.")
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('jac starting')
        case_number = '05-2009-CA-009068-XXXX-XX'
        items = jac.bclerk.get_records_grid_for_case_number(case_number)
        pprint.pprint(items)
        self.assertEquals(items, [{u'Book': u'5917',
  u'CFN': u'2009043291',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'LIS PENDENS',
  u'First Direct Name': u'CITIBANK NA TR',
  u'First Indirect Name': u'ALLEY,MARTHA B',
  u'First Legal': u'LT 5 BLK 159 PB 22 PG 46 PORT ST JOHN UNIT 5 S 21 T 23 R 35 SUBID JN',
  u'Page': u'5651',
  u'RecordDate': u'3/9/2009',
  u'Status': u'',
  u'[row]': u'1'},
 {u'Book': u'6010',
  u'CFN': u'2009153570',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'NOTICE',
  u'First Direct Name': u'CITIBANK NA TR',
  u'First Indirect Name': u'ALLEY,MARTHA B',
  u'First Legal': u'',
  u'Page': u'2419',
  u'RecordDate': u'8/18/2009',
  u'Status': u'',
  u'[row]': u'2'},
 {u'Book': u'6234',
  u'CFN': u'2010170255',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'JUDGMENT REAL PROPERTY',
  u'First Direct Name': u'CITIBANK NA TR',
  u'First Indirect Name': u'ALLEY,MARTHA B',
  u'First Legal': u'LT 8 BLK 159 PB 22 PG 46 PORT ST JOHN UNIT 5 S 21 T 23 R 35 SUBID JN',
  u'Page': u'2212',
  u'RecordDate': u'9/2/2010',
  u'Status': u'',
  u'[row]': u'3'},
 {u'Book': u'6846',
  u'CFN': u'2013077836',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'ORDER',
  u'First Direct Name': u'CITIBANK NA TR',
  u'First Indirect Name': u'ALLEY,MARTHA B',
  u'First Legal': u'',
  u'Page': u'55',
  u'RecordDate': u'4/5/2013',
  u'Status': u'',
  u'[row]': u'4'},
 {u'Book': u'7017',
  u'CFN': u'2013256767',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'LIS PENDENS',
  u'First Direct Name': u'WILMINGTON TRUST NATIONAL ASSN TR',
  u'First Indirect Name': u'ALLEY,MARTHA B',
  u'First Legal': u'LT 5 BLK 159 PB 22 PG 46 PORT ST JOHN UNIT 5 S 21 T 23 R 35 SUBID JN',
  u'Page': u'39',
  u'RecordDate': u'11/21/2013',
  u'Status': u'',
  u'[row]': u'5'},
 {u'Book': u'7216',
  u'CFN': u'2014192199',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'JUDGMENT REAL PROPERTY',
  u'First Direct Name': u'WILMINGTON TRUST NATIONAL ASSN TR',
  u'First Indirect Name': u'ALLEY,MARTHA E TR',
  u'First Legal': u'LT 5 BLK 159 PB 22 PG 46 PORT ST JOHN UNIT 5 S 21 T 23 R 35 SUBID JN',
  u'Page': u'2034',
  u'RecordDate': u'9/26/2014',
  u'Status': u'',
  u'[row]': u'6'},
 {u'Book': u'7266',
  u'CFN': u'2014244049',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$100.00',
  u'DocTypeKey': u'CERTIFICATE OF TITLE',
  u'First Direct Name': u'ALLEY,MARTHA E TR',
  u'First Indirect Name': u'WILMINGTON TRUST NATIONAL ASSN TR',
  u'First Legal': u'LT 5 BLK 159 PB 22 PG 46 PORT ST JOHN UNIT 5 S 21 T 23 R 35 SUBID JN',
  u'Page': u'1136',
  u'RecordDate': u'12/16/2014',
  u'Status': u'',
  u'[row]': u'7'}])

#         print('2')
#         print(results_node)
#         print('3')
#         print(results_node.parent.descendants.find_all('a'))
#         print('4')
#         jac.myutils.print_small_texts(list(soup.descendants))

    def test1(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('jac starting')
        case_number = '05-2009-CA-009068-XXXX-XX'
        items = jac.bclerk.get_records_grid_for_case_number(case_number)
        pprint.pprint(items)
        self.assertEquals(items, [{u'Book': u'5917',
  u'CFN': u'2009043291',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'LIS PENDENS',
  u'First Direct Name': u'CITIBANK NA TR',
  u'First Indirect Name': u'ALLEY,MARTHA B',
  u'First Legal': u'LT 5 BLK 159 PB 22 PG 46 PORT ST JOHN UNIT 5 S 21 T 23 R 35 SUBID JN',
  u'Page': u'5651',
  u'RecordDate': u'3/9/2009',
  u'Status': u'',
  u'[row]': u'1'},
 {u'Book': u'6010',
  u'CFN': u'2009153570',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'NOTICE',
  u'First Direct Name': u'CITIBANK NA TR',
  u'First Indirect Name': u'ALLEY,MARTHA B',
  u'First Legal': u'',
  u'Page': u'2419',
  u'RecordDate': u'8/18/2009',
  u'Status': u'',
  u'[row]': u'2'},
 {u'Book': u'6234',
  u'CFN': u'2010170255',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'JUDGMENT REAL PROPERTY',
  u'First Direct Name': u'CITIBANK NA TR',
  u'First Indirect Name': u'ALLEY,MARTHA B',
  u'First Legal': u'LT 8 BLK 159 PB 22 PG 46 PORT ST JOHN UNIT 5 S 21 T 23 R 35 SUBID JN',
  u'Page': u'2212',
  u'RecordDate': u'9/2/2010',
  u'Status': u'',
  u'[row]': u'3'},
 {u'Book': u'6846',
  u'CFN': u'2013077836',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'ORDER',
  u'First Direct Name': u'CITIBANK NA TR',
  u'First Indirect Name': u'ALLEY,MARTHA B',
  u'First Legal': u'',
  u'Page': u'55',
  u'RecordDate': u'4/5/2013',
  u'Status': u'',
  u'[row]': u'4'},
 {u'Book': u'7017',
  u'CFN': u'2013256767',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'LIS PENDENS',
  u'First Direct Name': u'WILMINGTON TRUST NATIONAL ASSN TR',
  u'First Indirect Name': u'ALLEY,MARTHA B',
  u'First Legal': u'LT 5 BLK 159 PB 22 PG 46 PORT ST JOHN UNIT 5 S 21 T 23 R 35 SUBID JN',
  u'Page': u'39',
  u'RecordDate': u'11/21/2013',
  u'Status': u'',
  u'[row]': u'5'},
 {u'Book': u'7216',
  u'CFN': u'2014192199',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$0.00',
  u'DocTypeKey': u'JUDGMENT REAL PROPERTY',
  u'First Direct Name': u'WILMINGTON TRUST NATIONAL ASSN TR',
  u'First Indirect Name': u'ALLEY,MARTHA E TR',
  u'First Legal': u'LT 5 BLK 159 PB 22 PG 46 PORT ST JOHN UNIT 5 S 21 T 23 R 35 SUBID JN',
  u'Page': u'2034',
  u'RecordDate': u'9/26/2014',
  u'Status': u'',
  u'[row]': u'6'},
 {u'Book': u'7266',
  u'CFN': u'2014244049',
  u'CaseNumber': u'05-2009-CA-009068-XXXX-XX',
  u'Consideration': u'$100.00',
  u'DocTypeKey': u'CERTIFICATE OF TITLE',
  u'First Direct Name': u'ALLEY,MARTHA E TR',
  u'First Indirect Name': u'WILMINGTON TRUST NATIONAL ASSN TR',
  u'First Legal': u'LT 5 BLK 159 PB 22 PG 46 PORT ST JOHN UNIT 5 S 21 T 23 R 35 SUBID JN',
  u'Page': u'1136',
  u'RecordDate': u'12/16/2014',
  u'Status': u'',
  u'[row]': u'7'}])

    def test_bclerk_0(self):
#         legal_str = 'LT 34 PB 25 PG 105 RAVENCREST S 22 T 20G R 34 SUBID 01'
#         legal_str = 'BLK 40K U T174 W 260 FT OF S 530 FT OF N 790 FT THE VILLAGES OF SEAPORT CONDO ORB 2598/136 S 14 T 24 R 37 SUBID 00'
        legal_str = 'LT 14 PB 1 PG 165 FLORIDA INDIAN RIVER LAND CO E 230 FT OF N 1/4 S 23 T 29 R 37'
        legal=jac.bclerk.get_legal_from_str(legal_str)
        print('legal='+str(legal))

    def test_bclerk_1(self):
#         legal_str = 'LT 34 PB 25 PG 105 RAVENCREST S 22 T 20G R 34 SUBID 01'
#         legal_str = 'BLK 40K U T174 W 260 FT OF S 530 FT OF N 790 FT THE VILLAGES OF SEAPORT CONDO ORB 2598/136 S 14 T 24 R 37 SUBID 00'
#         legal_str = 'LT 14 PB 1 PG 165 FLORIDA INDIAN RIVER LAND CO E 230 FT OF N 1/4 S 23 T 29 R 37'
        legal=jac.bclerk.get_legal_by_case("05-2013-CA-037340-XXXX-XX")
        print('legal='+str(legal))

    def test_bclerk_1b(self):
        ret=jac.bclerk.get_legal_by_case('05-2009-CA-034931-')
#         print('rets='+str(rets))
        pprint.pprint(ret)

    def test_bclerk_2(self):
        ret=jac.bclerk.get_legal_by_case('05-2009-CA-014066-')
#         print('rets='+str(rets))
        pprint.pprint(ret)

        rets=jac.bclerk.get_legals_by_case('05-2009-CA-014066-')
#         print('rets='+str(rets))
        pprint.pprint(rets)

    def test_oncoreweb_by_legal(self):
        leg_desc_in = 'LT 7 BLK H PB 54 PG 49 HERITAGE ISLE P.U.D. PHASE 5 S 08 T 26 R 36 SUBID UP'
        l = jac.bclerk.get_legal_from_str(leg_desc_in)
        print(l)
        # leg_desc_url_out = 'http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=01%2F01%2F1981&ed=4%2F19%2F2016&bt=OR&d=4%2F19%2F2016&pt=-1&lf=Lot%2C7%7CBlock%2CH%7CLand_Lot%2C54%7CDistrict%2C49%7CPropSection%2C08%7CBuilding%2C26%7CRange%2C36%7CPhase%2CUP&cn=&dt=&st=legal&ld='
        leg_desc_url_out = 'http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=01%2F01%2F1981&ed=4%2F19%2F2016&bt=OR&d=4%2F19%2F2016&pt=-1&lf=Lot%2C7%7CBlock%2CH%7CLand_Lot%2C54%7CDistrict%2C49%7CPropSection%2C08%7CBuilding%2C26%7CRange%2C36%7CPhase%2CUP&cn=&dt=&st=legal&ld='

        self.assertEqual(leg_desc_url_out, jac.bclerk.oncoreweb_by_legal(leg_desc_in))

    def test_do_oncoreweb_legal(self):
        # self.assertEqual(
        #     'http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=01%2F01%2F1981&ed=4%2F19%2F2016&bt=OR&d=4%2F19%2F2016&pt=-1&lf=Lot%2C1%7CBlock%2C%7CLand_Lot%2C40%7CDistrict%2C33%7CPropSection%2C02%7CBuilding%2C27%7CRange%2C37%7CPhase%2CPY&cn=05-2015-CA-026652-XXXX-XX&dt=ALL%20DOCUMENT%20TYPES&st=legal&ld=Lot%201%20Block%20%20Plat%20BK%2040%20Plat%20Pg%2033%20Section%2002%20Township%2027%20Range%2037%20SUBID%20PY%20'
        #     , jac.bclerk.oncoreweb_by_legal('LT 1 PB 40 PG 33 HARBOUR LIGHTS PHASE II S 02 T 27 R 37 SUBID PY'))

        actual = jac.bclerk.oncoreweb_by_legal('LT 1 PB 40 PG 33 HARBOUR LIGHTS PHASE II S 02 T 27 R 37 SUBID PY')
        print(actual)
        self.assertEqual(
            'http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=01%2F01%2F1981&ed=4%2F19%2F2016&bt=OR&d=4%2F19%2F2016&pt=-1&lf=Lot%2C1%7CLand_Lot%2C40%7CDistrict%2C33%7CPropSection%2C02%7CBuilding%2C27%7CRange%2C37%7CPhase%2CPY&cn=&dt=&st=legal&ld='
            , actual)
        self.assertEqual(
            'http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=01%2F01%2F1981&ed=4%2F19%2F2016&bt=OR&d=4%2F19%2F2016&pt=-1&lf=Lot%2C1%7CLand_Lot%2C40%7CDistrict%2C33%7CPropSection%2C02%7CBuilding%2C27%7CRange%2C37%7CPhase%2CPY&cn=&dt=&st=legal&ld='
            , actual)

    def test_do_oncoreweb_legal2(self):
        # print(jac.bclerk.oncoreweb_by_legal('BLK 261J U 8402 UNSURVEYED LAND LYING W OF GOVT PUERTO DEL RIO CONDO PH 1D ORB 5470/7102 S 15 T 24 R 37 SUBID 00'))
        print(jac.bclerk.oncoreweb_by_legal('BLK 261J U 8402 UNSURVEYED LAND LYING W OF GOVT PUERTO DEL RIO CONDO PH 1D ORB 5470/7102 S 15 T 24 R 37 SUBID 00'))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()