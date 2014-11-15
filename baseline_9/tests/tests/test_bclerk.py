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



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()