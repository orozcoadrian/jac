from jac.record.MyRecordSet import MyRecordSet

class FilterMax():
    def __init__(self, args=None):
        self.limit=None
        if args.max:
            self.limit = args.max
        # print('aaaasdfsdfsdfsdf:'+str(self.limit))
    def get_name(self):
        return 'FilterMax'
    def get_limit(self):
        return self.limit
    def apply(self, recordset):
        items2=recordset.get_records()
        limit=recordset.get_size()
        if self.limit is not None:
            limit = self.limit
        mrs=MyRecordSet()
        mrs.set_records(items2[:limit])
        return mrs