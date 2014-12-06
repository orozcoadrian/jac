'''
Created on Jul 27, 2014

@author: Adrian
'''
import unittest
from jac.cfm import cfm
import pprint
import logging

class Test(unittest.TestCase):


    def test1(self):
#         out_dir='hi'
        year='1950'
        court_type='hj'
        seq_number='56'
        cfid='99'
        cftoken='66'
        self.assertEqual('https://vweb1.brevardclerk.us/facts/d_caseno.cfm', cfm.get_url())
        expected_headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'CFID=99; CFTOKEN=66'}
        self.assertEqual(expected_headers, cfm.get_headers(cfid, cftoken))
        expected_data='CaseNumber1=05&CaseNumber2=1950&CaseNumber3=hj&CaseNumber4=56&CaseNumber5=&CaseNumber6=&submit=Submit'
        self.assertEqual(expected_data, cfm.get_data(year, court_type, seq_number))
#         cfm.cfm.case_info(out_dir, year, court_type, seq_number, cfid, cftoken)

    def test2(self):
#         cfm.case_info_grid(year='2013', court_type='CA', seq_number='033024')
#         print('='*80)
        ret = cfm.reg_actions_grid(year='2013', court_type='CA', seq_number='033024')
        print('='*80)
        for i in ret['items']:
            if 'OR MTG' in i['Description']:
                pprint.pprint(i)
                
    def test3(self):
        cn = cfm.get_case_number_fields('05-2007-CA-025830-XXXX-XX')
        pprint.pprint(cn)
        
    def test4(self):
        ret = cfm.reg_actions_grid_by_cn('05-2007-CA-025830-XXXX-XX')
        print('='*80)
        for i in ret['items']:
#             pprint.pprint(i)
            if 'Description' in i and 'OR MTG' in i['Description']:
                print(i['Img'])
                
    def test5(self):
        url = cfm.get_orig_mortgage_url_by_cn('05-2007-CA-025830-XXXX-XX')
        print(url)
        
    def test5b(self):
        url = cfm.get_orig_mortgage_url_by_cn('05-2009-CA-028248')
        print(url)
        self.assertEqual('http://vweb3.brevardclerk.us/PublicAccess/ImageView.aspx?DKT_ID=23642134&PROJ_ID=BCC&All=Y&UseRedacted=Y', url)
    def test5c(self):
        # works with soup = BeautifulSoup(r_text.encode('utf-8'), 'html5lib')
        self.assert_orig_mortgage_by_cn('05-2009-CA-046394','http://vweb3.brevardclerk.us/PublicAccess/ImageView.aspx?DKT_ID=20413258&PROJ_ID=BCC&All=Y&UseRedacted=Y')
    def test5cc(self):
        # works with soup = BeautifulSoup(r_text.encode('utf-8'), 'html5lib')
        self.assert_orig_mortgage_by_cn('05-2013-CA-027927-XXXX-XX','http://vweb3.brevardclerk.us/PublicAccess/ImageView.aspx?DKT_ID=22425977&PROJ_ID=BCC&All=Y&UseRedacted=Y')
#         pass
    def test5d(self):
        self.assert_orig_mortgage_by_cn('05-2009-CA-012115-XXXX-XX','http://vweb3.brevardclerk.us/PublicAccess/ImageView.aspx?DKT_ID=19297279&PROJ_ID=BCC&All=Y&UseRedacted=Y')
        #
    def test5e(self):
        self.assert_orig_mortgage_by_cn('05-2012-CA-051727','http://vweb3.brevardclerk.us/PublicAccess/ImageView.aspx?DKT_ID=23228067&PROJ_ID=BCC&All=Y&UseRedacted=Y')
        
        
    def assert_orig_mortgage_by_cn(self, cn, expected_url):
        self.assertEqual(expected_url, cfm.get_orig_mortgage_url_by_cn(cn))
        #
        
    def test6(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('test6 starting')
        self.assertEquals('http://vweb3.brevardclerk.us/PublicAccess/ImageView.aspx?DKT_ID=10910667&PROJ_ID=BCC&All=Y&UseRedacted=Y',
                          cfm.get_orig_mortgage_url_by_cn('05-2007-CA-025830-XXXX-XX'))
    def test7(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('test7 starting')
        self.assertEquals('http://vweb3.brevardclerk.us/PublicAccess/ImageView.aspx?DKT_ID=10910667&PROJ_ID=BCC&All=Y&UseRedacted=Y',
                          cfm.get_orig_mortgage_url_by_yts('2007', 'CA', '025830'))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()