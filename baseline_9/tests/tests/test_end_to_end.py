'''
Created on Dec 28, 2014

@author: Adrian
'''
import unittest
import jac.bclerk
import jac.bcpao
import pprint
from bs4 import BeautifulSoup
import logging

class Test(unittest.TestCase):

# todo:
# 1. unresolved business-logic (need to separate tests on solution abstractions (what's the lis pendens on this case) from solution abstractions (how will we choose from which record to get the legal description):
#     1. which doc types to use in clerk search? (lis pendens, judgment real property, both?)
#     2. how to search on bcpao? (by pid, by pb)

    def get_address_from_cn(self, cn_str):
        legal = jac.bclerk.get_legal_by_case(cn_str)
        print 'legal=' + str(legal)
        if 'subd' in legal:
            acct = str(jac.bcpao.get_acct_by_legal((legal['subd'], legal['lt'], legal['blk'], legal['pb'], legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid'])))
            print 'acct=' + str(acct)
            i = jac.bcpao.get_bcpaco_item(acct)
            pprint.pprint(i)
            if 'address' in i:
                the_address = str(i['address'])
                return the_address

    def testName(self):
#         cn = cfm.get_case_number_fields('05-2007-CA-025830-XXXX-XX')
#         pprint.pprint(cn)

        cn_str = "05-2007-CA-025830-XXXX-XX"
        the_address = self.get_address_from_cn(cn_str)
        print('addr='+the_address)

    def test2(self):
        cns = [
                '05-2010-CA-027173-',
                '05-2010-CA-032465-',
                '05-2010-CA-033421-',
                '05-2011-CA-041873-',
                '05-2012-CA-024202-',
                '05-2013-CA-033483-',
                '05-2013-CA-035247-',
                '05-2014-CA-010186-',
                '05-2014-CC-017432-',
                ]
        for cn in cns:
            print(self.get_address_from_cn(cn))



    def test2b(self):
        cns = [
                '05-2010-CA-057638-',
                '05-2012-CA-062968-',
                '05-2013-CA-031331-',
                '05-2013-CA-032569-',
                '05-2013-CA-036686-',
                '05-2013-CA-037340-',
                '05-2013-CA-039253-',
                '05-2013-CA-042042-',
                '05-2013-CA-042417-',
                '05-2013-CA-042443-',
                '05-2014-CA-010194-',
                '05-2014-CA-010788-',
                '05-2014-CA-011789-',
                '05-2014-CA-012602-',
                '05-2014-CA-017377-',
                '05-2014-CA-018252-',
                '05-2014-CA-023885-',
                ]
        for cn in cns:
            print(self.get_address_from_cn(cn))



    def test2c(self):
        cns = [
                '05-2009-CA-040883-',
                '05-2010-CA-050280-',
                '05-2011-CA-057164-',
                '05-2011-CA-057609-',
                '05-2012-CA-025685-',
                '05-2012-CA-053178-',
                '05-2012-CA-062378-',
                '05-2013-CA-027878-',
                '05-2013-CA-028461-',
                '05-2013-CA-038908-',
                '05-2013-CA-072125-',
                '05-2013-CC-035392-',
                '05-2014-CA-014662-',
                '05-2014-CA-018312-',
                '05-2014-CA-027470-',
                '05-2014-CA-032923-',

                ]
        for cn in cns:
            print(self.get_address_from_cn(cn))

    def test2d(self):
        cns = [
#                 '05-2011-CA-046980-',
#                 '05-2012-CA-063660-',
#                 '05-2013-CA-026643-',
#                 '05-2013-CA-027486-',
#                 '05-2013-CA-036632-',
#                 '05-2013-CA-038004-',
#                 '05-2013-CA-038998-',
#                 '05-2014-CA-016313-',
#                 '05-2014-CA-021695-',
#                 '05-2014-CA-031789-',
#                 '05-2014-CA-032530-',
#                 '05-2013-CA-028336-', # couldnt get address
#                 '05-2014-CA-029681-', # couldnt get address
#                 '05-2007-CA-021550-', # couldnt get address
#                 '05-2010-CA-013094-', # couldnt get address
#                 '05-2010-CA-038139-', # couldnt get address
#                 '05-2010-CA-057240-', # couldnt get address
#                 '05-2012-CA-021278-', # couldnt get address
#                 '05-2012-CA-047886-', # couldnt get address
#                 '05-2012-CA-072439-', # wrong address
#                 '05-2010-CA-012672-', # couldnt get address. condo. need to change block from 2C to 2.C
#                 '05-2012-CA-038224-', # got error
#                 '05-2010-CA-056748-', # no addr

                # regarding 012414:
                # if i use block 1067, i get nothing, but if i do block 106.7 then i get the correct address (per orig mtg link)
                # bcpao site address: 7010 N HIGHWAY 1 FF-104, COCOA 32927
                # https://www.bcpao.us/asp/Show_parcel.asp?acct=2315844&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=PID
                # orig mtg:
                # 7010 US HIGHWAY #1 NORTH UNIT 104 COCOA, FL 32927
                # LT 12 BLK 1067 PB 2 PG 2 U FF-104 DELESPINE ON INDIAN RIVER SUNRISE VILLAGE CONDO PH III ORB 3024/25 S 18 T 23 R 36 SUBID BH
#                 '05-2011-CA-012414-', # no addr

                # in this other one, the block is 2134 and i get an address. if i use 213.4, then it doesn't work.
                #                       T  R  S  SUBID  BLK  LOT
                #         Parcel ID:    28-36-26-KN-02134.0-0028.00
                # https://www.bcpao.us/asp/Show_parcel.asp?acct=2807459&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=PID

                # so the question is: how to know when to add a period in the block?


                # regarding 030815:
                '05-2013-CA-030815-', # no addr


#                 '05-2012-CA-062429-', # no addr
#                 '05-2013-CA-027486-', # no addr
#                 '05-2013-CA-027540-', # no addr
#                 '05-2013-CA-028409-', # no addr
#
#                 '05-2013-CA-032701-', # no addr
#                 '05-2014-CA-019046-', # no addr
#                 '05-2014-CA-020042-', # no addr
#                 '05-2014-CA-026837-', # no addr
                ]
        for cn in cns:
            print(self.get_address_from_cn(cn))


    def test3(self):
        cn_str = "05-2010-CA-032465-"
#         print(jac.bclerk.get_bclerk_results_text(cn_str))
        ret = jac.bclerk.get_legal_by_case(cn_str)
#         print(repr(ret))
        self.assertEquals('LT 14 PB 1 PG 33 PLAT OF HORTI S 88.81FT OF N 139.10FT; '
                         +'LT 14 PB 1 PG 33 PLAT OF HORTI S 88.81 FT OF N 139.10 FT', ret['legal_description'])
        the_address = self.get_address_from_cn(cn_str)
#         print('addr='+str(the_address))

    def test4(self):
        cn_str = "05-2010-CA-032465-"
#         print(jac.bclerk.get_bclerk_results_text(cn_str))
        ret_items = jac.bclerk.get_records_grid_for_case_number(cn_str)
        self.assertEquals(4, len(ret_items))

        self.assertEquals('LT 14 PB 1 PG 33 PLAT OF HORTI S 88.81FT OF N 139.10FT', ret_items[0]['First Legal'])
        self.assertEquals('', ret_items[1]['First Legal'])
        self.assertEquals('', ret_items[2]['First Legal'])
        self.assertEquals('LT 14 PB 1 PG 33 PLAT OF HORTI S 88.81 FT OF N 139.10 FT', ret_items[3]['First Legal'])
#         the_address = self.get_address_from_cn(cn_str)
#         print('addr='+str(the_address))

    def test_condo_1(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
        logging.getLogger().setLevel(logging.DEBUG)
        # 05-2009-CA-014066-
        print(self.get_address_from_cn('05-2009-CA-014066-'))
        
    def test5(self):
        cases = []
        cases.append('05-2008-CA-018262-')
        cases.append('05-2008-CA-065237-')
        cases.append('05-2009-CA-014066-')
        cases.append('05-2012-CA-061930-')
        cases.append('05-2012-CA-062814-')
        cases.append('05-2012-CA-066773-')
        cases.append('05-2013-CA-027773-')
        cases.append('05-2013-CA-028461-')
        cases.append('05-2013-CA-035656-')
        cases.append('05-2013-CA-037340-')
        cases.append('05-2013-CA-038768-')
        cases.append('05-2013-CA-042443-')
        cases.append('05-2014-CA-013087-')
        cases.append('05-2014-CA-017270-')
        cases.append('05-2014-CA-023885-')
        cases.append('05-2014-CA-026839-')
        cases.append('05-2014-CA-026879-')
        cases.append('05-2014-CA-028045-')
        cases.append('05-2014-CA-028736-')
        for c in cases:
            legals=jac.bclerk.get_legals_by_case(c)
            for l in legals:
                pprint.pprint(l)
                run_new_bcpao(l['legal_desc'])

def run_new_bcpao(legal_desc_str):
    legal = jac.bclerk.get_legal_from_str(legal_desc_str)
    if 'condo' in legal and legal['condo']:
        print('skipping condo: ' + legal_desc_str)
    elif 'subd' not in legal:
        print('skipping non-subd: ' + legal_desc_str)
    else:
        print '>legal ' + legal_desc_str
        print('>sub_pg_lot '+str(len(jac.bcpao.get_accts_by_legal_by_sub__sub_pg_lot(jac.bcpao.get_legal_tuple(legal)))))
        print('>subname_lot_block '+str(len(jac.bcpao.get_accts_by_legal_by_sub__subname_lot_block(jac.bcpao.get_legal_tuple(legal)))))
        print('>plat_lot_block '+str(len(jac.bcpao.get_accts_by_legal_by_plat__pb_pg_lot_block(jac.bcpao.get_legal_tuple(legal)))))
        
        pid_accs = jac.bcpao.get_accts_by_legal_by_pid__t_r_s_subid_block_lot(jac.bcpao.get_legal_tuple(legal))
        print('>pid '+str(len(pid_accs)))
        if len(pid_accs) == 1:
            print('>the_pid: ' + str(pid_accs[0]))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()