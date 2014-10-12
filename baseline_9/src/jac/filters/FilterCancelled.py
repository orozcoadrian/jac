'''
Created on Jul 27, 2014

@author: Adrian
'''
from jac.record.MyRecordSet import MyRecordSet
from jac.filters import Filter
class FilterCancelled(Filter):
    '''
    classdocs
    '''
    def __init__(self, args):
        self.args = args
    def get_name(self):
        return 'FilterCancelled'

    def apply(self, mrs):
        new_recs = []
        for rec in mrs.get_records():
            add_it = True
            if 'CANCELLED' in rec.get_item()['comment']:
                add_it = False
            # print(add_it)
            if add_it:
                new_recs.append(rec)
        new_mrs=MyRecordSet()
        new_mrs.set_records(new_recs)
        return new_mrs
