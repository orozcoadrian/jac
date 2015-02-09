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



    
    @unittest.skip("this test was written against an implementation that used JUDGMENT REAL PROPERTY. using jrp you get lot 5 but using lis pendens you get lot 8.")
    def test0(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('jac starting')
        case_number = '05-2009-CA-009068-XXXX-XX'
        items = jac.bclerk.get_records_grid_for_case_number(case_number)
        pprint.pprint(items)
        self.assertEquals(items, [{u'Book': u'6234',
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
  u'[row]': u'1'},
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
  u'[row]': u'2'}])
            
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



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()