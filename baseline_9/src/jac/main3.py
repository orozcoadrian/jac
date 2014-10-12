import sys
import argparse
import datetime
from xlwt import Workbook
import logging
import jac_core
import time
import jac.filters.FilterMax
import jac.filters.FilterCountId
import jac.filters.FilterCancelled
import jac.sales.sales
import mydate
from datetime import date
import record.MyRecordSet
import pprint
from fetch import Cfm, Legal, Bcpao
import os
import zipfile
import shutil


def get_non_cancelled_nums(args, mrs):
    mrs = record.MyRecordSet.MyRecordSet()
    jac.sales.sales.add_foreclosures(mrs)
    mrs=jac.filters.FilterCancelled.FilterCancelled(args).apply(mrs)
    date_counts = pprint.pformat(jac.myutils.get_dates_count_map(mrs.get_records())).replace('\n', '<br>').replace('datetime.datetime(', '').replace(', 0, 0', '').replace(', ', '/').replace(')', '')
    return date_counts

def main3():
    print('START')
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

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('jac starting')
    #logging.debug('jac starting2')
    #print('asdf')
    start = time.time()
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    logging.info('args: '+str(args))

    fnum=jac.filters.FilterMax.FilterMax(args)
    mrs=record.MyRecordSet.MyRecordSet()
    jac.sales.sales.add_foreclosures(mrs,fnum.get_limit())
    date_counts = pprint.pformat(jac.myutils.get_dates_count_map(mrs.get_records())).replace('\n', '<br>').replace('datetime.datetime(','').replace(', 0, 0','').replace(', ','/').replace(')','')

    parent_out_dir = 'outputs'
    out_dir = parent_out_dir+'/'+timestamp
    if args.out_tag:
        out_dir+='_'+args.out_tag
    os.makedirs(out_dir)
    print(os.path.abspath(out_dir))

    the_tag = timestamp
    if args.out_tag:
        the_tag += '_' + args.out_tag
    filename = the_tag + '.xls'
    out_file = out_dir + '/' + filename
    book = Workbook()


    #date_string_to_add = '02/18/2015'

    #dataset = get_mainsheet_dataset(args, fnum, mrs, out_dir, date_string_to_add)

    dates_to_add = mydate.get_next_dates(date.today())
    date_strings_to_add = [x.strftime("%m/%d/%Y") for x in dates_to_add]

    datasets = []
    datasets.extend([get_mainsheet_dataset(args, fnum, mrs, out_dir, date_str) for date_str in date_strings_to_add])
    #datasets.append(get_mainsheet_dataset(args, fnum, mrs, out_dir, '02/18/2015'))
    #datasets.append(get_mainsheet_dataset(args, fnum, mrs, out_dir, '02/19/2015'))

    for dataset in datasets:
        jac.xl3.add_data_set_sheet(dataset, book)
    book.save(out_file)
    print(out_file)

    if args.open:
        os.system('start "" "C:/Program Files/Microsoft Office/Office12/Excel.exe" /e '+out_file)

    #date_strings_to_add2 = [x.strftime("%A %b %d") for x in dates_to_add]
    #date_strings_to_add2.extend(args.dates)
    short_date_strings_to_add = [x.strftime("%m.%d") for x in dates_to_add]
    abc = '-'.join([short_date_strings_to_add[0], short_date_strings_to_add[1]])
    print(abc)
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

def get_mainsheet_dataset(args, fnum, mrs, out_dir, date_string_to_add):
    filters = []
    filters.append(jac.filters.FilterCountId.FilterCountId(args))
    filters.append(jac.filters.FilterCancelled.FilterCancelled(args))
    filterByDatesObj = jac.filters.FilterByDates(args)
    date_strings_to_add = [date_string_to_add] #[x.strftime("%m/%d/%Y") for x in dates_to_add]
    filterByDatesObj.set_dates(date_strings_to_add)
    filters.append(filterByDatesObj)
    filters.append(fnum)
    print(date_string_to_add)
    for f in filters:
        logging.info(f.get_name() + ' before:' + str(len(mrs.get_records())))
        mrs = f.apply(mrs)
        logging.info('after: ' + str(len(mrs.get_records())))

    logging.info('after filters: ' + str(len(mrs.get_records())))
    sheet_name = date_string_to_add.replace('/', '_')[:5]
    out_dir_htm = out_dir +'/'+sheet_name+ '/html_files'
    os.makedirs(out_dir_htm)
    fetchers = []
    fetchers.append(Cfm(out_dir_htm))
    fetchers.append(Legal())
    fetchers.append(Bcpao())
    for r in mrs.get_records():
        print 'count_id: ' + str(r.item['count'])
        for f in fetchers:
            logging.info(f.get_name())
            f.fetch(r)


    sheetBuilder = jac.xl_builder.MainSheetBuilder(sheet_name)
    sheetBuilder.set_args(args)
    dataset = sheetBuilder.add_sheet(mrs.get_records())
    return dataset


if __name__ == '__main__':
    sys.exit(main3())




