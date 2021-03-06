# http://askubuntu.com/questions/116020/python-https-requests-urllib2-to-some-sites-fail-on-ubuntu-12-04-without-proxy
import ssl
import traceback

ssl.PROTOCOL_SSLv23 = ssl.PROTOCOL_TLSv1

# http://stackoverflow.com/questions/30904815/having-ssl-problems-with-requests-get-in-python     and     http://docs.python-requests.org/en/latest/user/advanced/
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

import requests




import sys
import argparse
import datetime
from xlwt import Workbook
import logging
import time
import jac.filters.FilterMax
import jac.filters.FilterCountId
import jac.filters.FilterCancelled
import jac.sales.sales
import mydate
from datetime import date
import record.MyRecordSet
import pprint
from fetch import Cfm, Legal, Bcpao, Bcpao_db, Taxes
import os
import zipfile
import shutil
from jac import myutils
from jac.maps import Maps

def get_non_cancelled_nums(args, mrs):
    mrs = record.MyRecordSet.MyRecordSet()
    jac.sales.sales.add_foreclosures(mrs)
    mrs=jac.filters.FilterCancelled.FilterCancelled(args).apply(mrs)
    date_counts = pprint.pformat(jac.myutils.get_dates_count_map(mrs.get_records())).replace('\n', '<br>').replace('datetime.datetime(', '').replace(', 0, 0', '').replace(', ', '/').replace(')', '')
    return date_counts

def main3():
    logging.basicConfig(format='%(asctime)s %(module)-15s %(levelname)s %(message)s', level=logging.DEBUG)
#     logging.getLogger().setLevel(logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('START')
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", default='3000', type=int, help="max number or items to process.")
    parser.add_argument("--open", action='store_true', help="open the main file at the end.")
    parser.add_argument("--out_tag", help="a tag to use to give the output a meaningful name.")
    parser.add_argument("--dates", nargs='+', help="dates to filter by.")
    parser.add_argument("--zip_code", nargs='+', help="zip codes to filter by.")
    parser.add_argument("--cfid", help="the cfid to use.")
    parser.add_argument("--cftoken", help="the cftoken to use.")
    parser.add_argument("--count_id", nargs='+', help="the count_id to use.")
    parser.add_argument("--wednesday", action='store_true', help="next thursday will be added.")
    parser.add_argument("--thursday", action='store_true', help="next thursday will be added.")
    parser.add_argument("--zip", action='store_true', help="do zip.")
    parser.add_argument("--email", action='store_true', help="do email.")
    parser.add_argument("--passw", help="email password.")
    args = parser.parse_args()


    logging.debug('jac starting')
    #logging.debug('jac starting2')
    #print('asdf')
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    logging.info('args: '+str(args))

    fnum=jac.filters.FilterMax.FilterMax(args)
    mrs=record.MyRecordSet.MyRecordSet()
    jac.sales.sales.add_foreclosures(mrs,fnum.get_limit())
    date_counts = pprint.pformat(myutils.get_dates_count_map(mrs.get_records())).replace('\n', '<br>').replace('datetime.datetime(','').replace(', 0, 0','').replace(', ','/').replace(')','')

    dates = mydate.get_next_dates(date.today())
    logging.info(dates)
    dates_to_add = dates#[0:2]
    if args.dates:
        dates_to_add = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in args.dates]
    date_strings_to_add = [x.strftime("%Y-%m-%d") for x in dates_to_add]

    #date_strings_to_add2 = [x.strftime("%A %b %d") for x in dates_to_add]
    #date_strings_to_add2.extend(args.dates)
    
    short_date_strings_to_add = [x.strftime("%m.%d") for x in dates_to_add]
    logging.info('short_date_strings_to_add: ' + str(short_date_strings_to_add))
    abc = '-'.join(short_date_strings_to_add[0:1])

    parent_out_dir = 'outputs'
    out_dir = parent_out_dir+'/'+timestamp
    if args.out_tag:
        out_dir+='_'+args.out_tag
    os.makedirs(out_dir)
    logging.info(os.path.abspath(out_dir))

    the_tag = abc#timestamp
    if args.out_tag:
        the_tag += '_' + args.out_tag
    filename = the_tag + '.xls'
    out_file = out_dir + '/' + filename
    book = Workbook()


    #date_string_to_add = '02/18/2015'

    #dataset = get_mainsheet_dataset(args, fnum, mrs, out_dir, date_string_to_add)



    datasets = []
    logging.info('date_strings_to_add: ' + str(date_strings_to_add))
    logging.info('abc: ' + abc)
#     return
    datasets.extend([get_mainsheet_dataset(args, fnum, mrs, out_dir, date_str) for date_str in date_strings_to_add])
    #datasets.append(get_mainsheet_dataset(args, fnum, mrs, out_dir, '02/18/2015'))
    #datasets.append(get_mainsheet_dataset(args, fnum, mrs, out_dir, '02/19/2015'))

    for dataset in datasets:
        jac.xl3.add_data_set_sheet(dataset, book)
    book.save(out_file)
    print(out_file)

    if args.open:
        os.system('start "" "C:/Program Files/Microsoft Office/Office12/Excel.exe" /e '+out_file)



    
    body = 'this result is for: ' + abc
    body += '<br>total records: ' + str(len(mrs.get_records()))

    date_counts = get_non_cancelled_nums(args, mrs)


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
        zip_filename=abc+'.zip'
        zip_filepath=parent_out_dir+'/'+zip_filename
        zipf = zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED)
        zipdir(out_dir, zipf)
        zipf.close()
        final_zip_path=out_dir+'/'+zip_filename
        shutil.move(zip_filepath, final_zip_path)

        file_paths.append(final_zip_path)

    subject = '[jac biweekly report]' + ' for: ' + abc
    print('subject: ' + subject)
    print('body: ' + body)

    if args.email and args.passw:
        # ; next week: ' + str(len(datasets[0].get_items())+len(datasets[1].get_items())) + ' records'
        jac.myutils.my_send_mail(file_paths,args.passw, subject, body)

    print 'duration %s' % datetime.timedelta(seconds=time.time()-start)
    print('END')
    return 0

def get_mainsheet_dataset(args, fnum, mrs, out_dir, date_string_to_add):
    logging.info('**get_mainsheet_dataset: ' + date_string_to_add)
    filters = []
    filters.append(jac.filters.FilterCountId.FilterCountId(args))
#     filters.append(jac.filters.FilterCancelled.FilterCancelled(args))
    filterByDatesObj = jac.filters.FilterByDates(args)
    date_strings_to_add = [date_string_to_add] #[x.strftime("%m/%d/%Y") for x in dates_to_add]
    filterByDatesObj.set_dates(date_strings_to_add)
    filters.append(filterByDatesObj)
    filters.append(fnum)
    logging.info(date_string_to_add)
    for f in filters:
        logging.info(f.get_name() + ' before:' + str(len(mrs.get_records())))
        mrs = f.apply(mrs)
        logging.info('after: ' + str(len(mrs.get_records())))

    logging.info('after filters: ' + str(len(mrs.get_records())))
    sheet_name = date_string_to_add[5:]
    out_dir_htm = out_dir +'/'+sheet_name+ '/html_files'
    os.makedirs(out_dir_htm)



    fetchers = []
    fetchers.append(Cfm(out_dir_htm))
    fetchers.append(Legal())
    fetchers.append(Bcpao(out_dir_htm))
#     fetchers.append(Bcpao_db())
    fetchers.append(Taxes())
    for r in mrs.get_records():
        logging.info('count_id: ' + str(r.item['count']))
        for f in fetchers:
            logging.info(f.get_name())
            done = False
            retries_count = 0
            while not done and retries_count < 10:
                try:
                    f.fetch(r)
                    done = True
                except Exception as e:
                    logging.error(' got an error when fetching: ' + str(e))
                    traceback.print_exc(file=sys.stdout)
                    logging.error(' retrying...')
                    retries_count += 1
                    logging.error(' retries_count: ' + str(retries_count))
                    time.sleep(1)

    # Maps().do_map_output(mrs, out_dir, sheet_name)

    logging.info('fetch complete')
    logging.info('num records: '+str(len(mrs.get_records())))
#     pprint.pprint(mrs.get_records())
    sheetBuilder = jac.xl_builder.MainSheetBuilder(sheet_name)
    sheetBuilder.set_args(args)
    dataset = sheetBuilder.add_sheet(mrs.get_records())
    return dataset





if __name__ == '__main__':
    sys.exit(main3())




