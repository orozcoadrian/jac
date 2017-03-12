'''
Created on Sep 27, 2014

@author: Adrian
'''
import logging
import record.MyRecordSet
import jac.filters.FilterMax
import jac.filters.FilterCountId
import jac.filters.FilterCancelled
import jac.sales.sales
import getpass
import time
import os
from fetch import Cfm, Legal, Bcpao
from xlwt import Workbook
import datetime
import jac.xl_builder
import jac.myutils
import jac.mydate
import pprint
import copy
import zipfile
import shutil


class Jac(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def do_run(self, args):
        #mypass=getpass.getpass()
        mypass=args.passw
        #logger = logging.getLogger('main')
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('jac starting')
        #logging.debug('jac starting2')
        #print('asdf')
        #return
        start = time.time()
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

        logging.info('args: '+str(args))

        fnum=jac.filters.FilterMax.FilterMax(args)
        mrs=record.MyRecordSet.MyRecordSet()
        jac.sales.sales.add_foreclosures(mrs,fnum.get_limit())
        date_counts = pprint.pformat(jac.myutils.get_dates_count_map(mrs.get_records())).replace('\n', '<br>').replace('datetime.datetime(','').replace(', 0, 0','').replace(', ','/').replace(')','')
        filters=[]
        filters.append(jac.filters.FilterCountId.FilterCountId(args))
        filters.append(jac.filters.FilterCancelled.FilterCancelled(args))
        filterByDatesObj = jac.filters.FilterByDates(args)
        dates_to_add = []
        if args.wednesday:
            dates_to_add.append(jac.mydate.get_next_wed())
        if args.thursday:
            dates_to_add.append(jac.mydate.get_next_thu())
        date_strings_to_add = [x.strftime("%m/%d/%Y") for x in dates_to_add]
        filterByDatesObj.set_dates(date_strings_to_add)
        filters.append(filterByDatesObj)
        filters.append(fnum)
        for f in filters:
            logging.info(f.get_name() + ' before:' + str(len(mrs.get_records())))
            mrs=f.apply(mrs)
            logging.info('after: ' + str(len(mrs.get_records())))

        logging.info('after filters: '  + str(len(mrs.get_records())))

        parent_out_dir = 'outputs'
        out_dir = parent_out_dir+'/'+timestamp
        if args.out_tag:
            out_dir+='_'+args.out_tag
        os.makedirs(out_dir)
        print(os.path.abspath(out_dir))
        out_dir_htm=out_dir+'/html_files'
        os.makedirs(out_dir_htm)
        fetchers=[]
        fetchers.append(Cfm(out_dir_htm))
        fetchers.append(Legal())
        fetchers.append(Bcpao(out_dir_htm))
        for r in mrs.get_records():
            print('count_id: ' + str(r.item['count']))
            for f in fetchers:
                logging.info(f.get_name())
                f.fetch(r)

        the_tag=timestamp
        if args.out_tag:
            the_tag+='_'+args.out_tag
        filename=the_tag+'.xls'
        out_file=out_dir+'/'+filename
        book = Workbook()
        sbs=[]
        sbs.append(jac.xl_builder.MainSheetBuilder())
#         sbs.append(jac.xl_builder.ZipsSheetBuilder())
#         sbs.append(jac.xl_builder.LuxurySheetBuilder())
#         sbs.append(jac.xl_builder.CheapSheetBuilder())
#         sbs.append(jac.xl_builder.RadiusSheetBuilder())
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


        #print(dates_to_add)
        if args.dates:
            dates_to_add.extend([datetime.datetime.strptime(x, "%m/%d/%Y") for x in args.dates])
        date_strings_to_add2 = [x.strftime("%A %b %d") for x in dates_to_add]
        #date_strings_to_add2.extend(args.dates)
        abc = ', '.join(date_strings_to_add2)
        print(abc)
        body = 'this result is for: ' + abc
        body += '<br>total records: ' + str(len(mrs.get_records()))

        body+='<br><br>the following summarizes how many not-cancelled items there are per month in the <a href="http://vweb2.brevardclerk.us/Foreclosures/foreclosure_sales.html">foreclosure sales page</a> as of now: <br>'+date_counts
        body+='<br><br>'+filename

        print(body)
        file_paths = []
        file_paths.append(out_file)
        if args.zip:
            def zipdir(path, azip):
                for root, the_dirs, files in os.walk(path):
                    for f in files:
                        azip.write(os.path.join(root, f))
                        #print(os.path.join(root, file))
            zip_filename=the_tag+'.zip'
            zip_filepath=parent_out_dir+'/'+zip_filename
            zipf = zipfile.ZipFile(zip_filepath, 'w')
            zipdir(out_dir, zipf)
            zipf.close()
            final_zip_path=out_dir+'/'+zip_filename
            shutil.move(zip_filepath, final_zip_path)

            file_paths.append(final_zip_path)

        if args.email:
            jac.myutils.my_send_mail(file_paths,mypass, '[jac daily report]'+' for: ' + abc + '; ' + str(len(mrs.get_records())) + ' records', body)
