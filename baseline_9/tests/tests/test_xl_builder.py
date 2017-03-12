'''
Created on Aug 23, 2014

@author: Adrian
'''
import unittest
import jac.xl_builder
import jac.record
from jac.record import MyRecord


class Test(unittest.TestCase):


    def test_one(self):
        instance = jac.xl_builder.MainSheetBuilder()
        self.assertEqual('MainSheetBuilder',instance.get_name())
        instance.set_args(None)
        self.assertEqual('http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=1%2F1%2F1981&ed=5%2F31%2F2014&n=the_url&bt=OR&d=2%2F5%2F2015&pt=-1&cn=&dt=ALL%20DOCUMENT%20TYPES&st=fullname&ss=ALL%20DOCUMENT%20TYPES',instance.get_bclerk_name_url("the_url"))
        self.assertEqual(None,instance.get_items_to_use(None))
        headers=instance.get_headers()
        self.assertEqual(21, len(headers))
        self.assertEqual('cn-',instance.get_display_case_number('cn-XXXX-XX'))

    def test_add_to_row(self):
        instance = jac.xl_builder.MainSheetBuilder()
        test_row=[]
        test_item={}
        test_item['case_number']='cn'
        test_item['case_title']='ct'
        test_item['foreclosure_sale_date']='fsd'
        test_item['count']='c'
        test_item['comment']=''
        test_item['taxes_value']=''
        r=jac.record.MyRecord.MyRecord(test_item)
        instance.add_to_row(test_row, r, 0)
        #print(test_row)



    def test_MainSheetBuilder(self):
        instance = jac.xl_builder.MainSheetBuilder()
        self.assertEqual('MainSheetBuilder',instance.get_name())
        headers=instance.get_headers()
        self.assertEqual(21, len(headers), str(headers))

        header_strings = [cell.get_display() for cell in headers]
        self.assertEqual(['high', 'win', 'case_number', 'case_title', 'fc._sale_date', 'case_info', 'reg_actions', 'count', 'address', 'zip', 'liens-name', 'bcpao', 'f_code', 'owed_link', 'owed', 'assessed', 'base_area', 'year built', 'owed - ass', 'orig_mtg', 'taxes'], header_strings)

    def test_MainSheetBuilder_with_rows(self):
        instance = jac.xl_builder.MainSheetBuilder()
        records = [MyRecord.MyRecord({
                                      'case_number':'cn0'
                                      ,'case_title':'ct0'
                                      ,'foreclosure_sale_date':'2'
                                      ,'count':'2'
                                      ,'comment':''
                                      ,'taxes_value':''
                                      })]
        data_set = instance.add_sheet(records)
        self.assertTrue(data_set is not None)
        print(data_set.get_items())
        #for row in data_set.get_items():
        header_row = data_set.get_items()[0]
        self.assertEqual('high', header_row[0].get_display())
        self.assertEqual('win', header_row[1].get_display())
        self.assertEqual('case_number', header_row[2].get_display())
        first_data_row = data_set.get_items()[1]
        self.assertEqual('', first_data_row[0].get_display())
        self.assertEqual('', first_data_row[1].get_display())
        self.assertEqual('cn0', first_data_row[2].get_display())

    def test_MainSheetBuilder_owed_minus_ass(self):
        instance = jac.xl_builder.MainSheetBuilder()
        records = [MyRecord.MyRecord({
            'case_number': 'cn0'
            , 'case_title': 'ct0'
            , 'foreclosure_sale_date': '2'
            , 'count': '2'
            , 'comment': ''
            , 'taxes_value': ''
        })]
        data_set = instance.add_sheet(records)
        self.assertTrue(data_set is not None)
        print(data_set.get_items())
        # for row in data_set.get_items():
        header_row = data_set.get_items()[0]
        self.assertEqual('high', header_row[0].get_display())
        first_data_row = data_set.get_items()[1]
        self.assertEqual('', first_data_row[0].get_display())
        self.assertEqual('IF(AND(NOT(ISBLANK(P2)),NOT(ISBLANK(Q2))),P2-Q2,"")', first_data_row[17].get_formula())
        for x,y in enumerate(first_data_row):
            print(x, y.get_formula())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()