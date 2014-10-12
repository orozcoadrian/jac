'''
Created on Jul 27, 2014

@author: Adrian
'''
from jac.record.MyRecordSet import MyRecordSet
from jac.filters import Filter

class FilterCountId(Filter):
    def __init__(self, args=None):
        self.count_id = args.count_id
    def get_name(self):
        return "FilterCountId"
    def get_count_id(self):
        return self.count_id
    def get_count_id_ints(self):
        ret=[]
        for i_str in self.get_count_id():
            ret.append(int(i_str))
        return ret
    def apply(self, recordset):
        items2=recordset.get_records()
        if self.get_count_id() is not None:
            mrs=MyRecordSet()
            recs=[]
            for i in items2:
                if i.get_item()['count'] in self.get_count_id_ints():
                    recs.append(i)
            mrs.set_records(recs)
            return mrs
        else:
            return recordset