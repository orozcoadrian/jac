import jac.sales.sales
import sys
# import myutils
# from collections import namedtuple
import time
import os
# import re
#import cfm
import argparse
import datetime
#import pprint
# # import urllib.request as req
# import bcpao
import jac.xl3
#import bclerk
# import bcpao_radius
import jac.record.MyRecordSet
import jac.filters.FilterMax
import jac.filters.FilterCountId
import jac.filters.FilterCancelled
from xlwt import Workbook
import jac.xl_builder
import logging
from fetch import Cfm, Legal, Bcpao
import jac.myutils
import getpass



def main():
    #mypass=getpass.getpass()
    #logger = logging.getLogger('main')
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('jac starting')
    #logging.debug('jac starting2')
    #print('asdf')
    #return
    start = time.time()
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", default='3000', type=int, help="max number or items to process.")
    parser.add_argument("--open", action='store_true', help="open the main file at the end.")
    parser.add_argument("--out_tag", help="a tag to use to give the output a meaningful name.")
    parser.add_argument("--dates", nargs='+', help="dates to filter by.")
    parser.add_argument("--zip_code", nargs='+', help="zip codes to filter by.")
    parser.add_argument("--cfid", help="the cfid to use.")
    parser.add_argument("--cftoken", help="the cftoken to use.")
    parser.add_argument("--count_id", nargs='+', help="the count_id to use.")
    args = parser.parse_args()
    logging.info('args: '+str(args))

    fnum=jac.filters.FilterMax.FilterMax(args)
    mrs=jac.record.MyRecordSet.MyRecordSet()
    jac.sales.sales.add_foreclosures(mrs,fnum.get_limit())
    filters=[]
    filters.append(jac.filters.FilterCountId.FilterCountId(args))
    filters.append(jac.filters.FilterCancelled.FilterCancelled(args))
    filters.append(jac.filters.FilterByDates(args))
    filters.append(fnum)
    for f in filters:
        logging.info(f.get_name() + ' before:' + str(len(mrs.get_records())))
        mrs=f.apply(mrs)
        logging.info('after: ' + str(len(mrs.get_records())))

    logging.info('after filters: '  + str(len(mrs.get_records())))

    out_dir = 'outputs/'+timestamp
    if args.out_tag:
        out_dir+='_'+args.out_tag
    os.makedirs(out_dir)
    out_dir_htm=out_dir+'/html_files'
    os.makedirs(out_dir_htm)
    fetchers=[]
    fetchers.append(Cfm(out_dir_htm))
    fetchers.append(Legal())
    fetchers.append(Bcpao())
    for r in mrs.get_records():
        print('count_id: ' + str(r.item['count']))
        for f in fetchers:
            logging.info(f.get_name())
            f.fetch(r)

    the_tag=timestamp
    if args.out_tag:
        the_tag+='_'+args.out_tag
    out_file=out_dir+'/'+the_tag+'.xls'
    book = Workbook()
    sbs=[]
    sbs.append(jac.xl_builder.MainSheetBuilder())
    sbs.append(jac.xl_builder.ZipsSheetBuilder())
    sbs.append(jac.xl_builder.LuxurySheetBuilder())
    sbs.append(jac.xl_builder.CheapSheetBuilder())
    sbs.append(jac.xl_builder.RadiusSheetBuilder())
    dss=[]
    for sb in sbs:
        #sb.args = args
        sb.set_args(args)
        print(sb.get_name())
        dss.append(sb.add_sheet(mrs.get_records()))

    for ds in dss:
        jac.xl3.add_data_set_sheet(ds, book)
    book.save(out_file)
    print(out_file)

    if args.open:
        os.system('start "" "C:/Program Files/Microsoft Office/Office12/Excel.exe" /e '+out_file)


    # print 'It took ', time.time()-start, ' seconds.'
    # print 'It took %.2f seconds' % (time.time()-start)
    print 'duration %s' % datetime.timedelta(seconds=time.time()-start)

    #jac.myutils.my_send_mail(out_file,mypass)


if __name__ == '__main__':
    sys.exit(main())