import jac.record.MyRecordSet

class Filter(object):
    def get_name(self):
        return "Filter"

class FilterByDates(Filter):
    def __init__(self, args):
        self.args = args
        self.dates=None
    def set_dates(self, dates):
        self.dates = dates
    def get_name(self):
        return 'FilterByDates'
    def apply(self, mrs):
        new_recs = []
        if self.args.dates:
            if self.dates is None:
                self.dates = []
            self.dates.extend(self.args.dates)
        if self.dates:
            # print(args.dates)
            for rec in mrs.get_records():
                add_it = False
                if rec.get_item()['foreclosure_sale_date'] in self.dates:
                    add_it = True
                # print(add_it)
                if add_it:
                    new_recs.append(rec)
            # for d in args.dates:
                # # print('d:'+d+' date: '+i['foreclosure_sale_date'])
                # if d in i['foreclosure_sale_date']:
                    # add_it = True
            new_mrs=jac.record.MyRecordSet.MyRecordSet()
            new_mrs.set_records(new_recs)
            return new_mrs
        else:
            return mrs