#http://rowinggolfer.blogspot.com/2009/08/pylint-recursively.html


'''
this module runs pylint on all python scripts found in a directory tree
'''

import os
import re
import sys
import pprint

total = 0.0
count = 0

data = []

def check(module):
    '''
    apply pylint to the file specified if it is a *.py file
    '''
    global total, count

    if module[-3:] == ".py":

        print "CHECKING ", module
        this_item = {'module': module}
        pout = os.popen('pylint %s'% module, 'r')
        for line in pout:
            if  re.match("E....:.", line):
                print line
            if "|code" in line:
                print line
                this_item['loc_code_line']=line
                splits = this_item['loc_code_line'].split('|')
                pprint.pprint(splits)
                this_item['loc_code']=splits[2]
                this_item['loc_code_pct']=splits[3]
            if "|comment" in line:
                print line
                this_item['loc_comment_line']=line
                splits = this_item['loc_comment_line'].split('|')
                pprint.pprint(splits)
                this_item['loc_comment']=splits[2]
                this_item['loc_comment_pct']=splits[3]
            if "Your code has been rated at" in line:
                print line
                score = re.findall("\d.\d\d", line)[0]
                total += float(score)
                count += 1
        data.append(this_item)
    
if __name__ == "__main__":
    try:
        print sys.argv   
        BASE_DIRECTORY = sys.argv[1]
    except IndexError:
        print "no directory specified, defaulting to current working directory"
        BASE_DIRECTORY = os.getcwd()

    print "looking for *.py scripts in subdirectories of ", BASE_DIRECTORY 
    for root, dirs, files in os.walk(BASE_DIRECTORY):
        for name in files:
            filepath = os.path.join(root, name)
            check(filepath)
            
    print "==" * 50
    print "%d modules found"% count
    print "AVERAGE SCORE = %.02f"% (total / count)
    pprint.pprint(data)
    # for d in data:
        # print(d['module'] + ' ' +d['loc_code_line'])
    print('module' + ' ' +'loc_code'+ ' ' +'loc_code_pct'+ ' ' +'loc_comment'+ ' ' +'loc_comment_pct')
    for d in data:
        print(d['module'] + ' ' +d['loc_code']+ ' ' +d['loc_code_pct']+ ' ' +d['loc_comment']+ ' ' +d['loc_comment_pct'])
