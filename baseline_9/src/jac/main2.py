
import sys
# import myutils
# from collections import namedtuple


# import re
#import cfm
import argparse
import datetime
#import pprint
# # import urllib.request as req
# import bcpao

#import bclerk
# import bcpao_radius

from xlwt import Workbook

import logging



#import jac.jac_core
import jac_core



def main2():

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

    the_jac = jac_core.Jac()
    the_jac.do_run(args)

    print('END')


def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, periodic,
                  (scheduler, interval, action, actionargs))
    action(*actionargs)

if __name__ == '__main__':
    sys.exit(main2())