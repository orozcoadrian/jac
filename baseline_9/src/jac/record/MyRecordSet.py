'''
Created on Jul 27, 2014

@author: Adrian
'''
import MyRecord

class MyRecordSet(object):
    '''
    a set of records
    '''
    def __init__(self):
        pass
    def set_items(self, items):
        self.records = []
        for i in items:
            mr = MyRecord.MyRecord(i)
            self.records.append(mr)
            # mr.
        # self.items=items
    def get_size(self):
        return len(self.records)
    def get_records(self):
        return self.records
    def set_records(self, recs):
        self.records = recs
    def pprint(self):
        # pprint.pprint(self.records)
        for record in self.records:
            record.pprint()
