import os
import sys
from time import strftime
#import pprint
from xlwt import Workbook,easyxf,Formula
#from collections import namedtuple
#import myutils

link_style = easyxf('font: underline single, color blue')

def get_formula_hyperlink(url, text):
    return Formula('HYPERLINK("'+url+'";"'+text+'")')
def get_formula(formula):
    return Formula(formula)

class Cell():
    def __init__(self, display, link, formula, width):
        self.display=display
        self.link=link
        self.width=width
        self.formula=formula

    @classmethod
    def from_display(cls, display, width=None):
        return cls(display, link=None, formula=None, width=width)
    @classmethod
    def from_link(cls, display, link, width=None):
        return cls(display, link, formula=None, width=width)
    @classmethod
    def from_formula(cls, formula, width=None):
        return cls(display=None, link=None, formula=formula, width=width)

    def get_display(self):
        return self.display
    def get_link(self):
        return self.link
    def set_link(self, link):
        self.link=link
    def get_formula(self):
        return self.formula
    def __str__(self):
        return 'Cell(%s)'%self.display
    def __repr__(self):
        return self.__str__()
    def set_col_width(self,width):
        self.width=width
    def get_col_width(self):
        return self.width

class DataSet():
    def __init__(self, name, items):
        self.name=name
        self.items=items
    def get_name(self):
        return self.name+'('+str(len(self.get_items())-1)+')'
    def get_items(self):
        return self.items
    def get_row(self, row):
        return self.items[row]

def add_data_set_sheet(ds, book):
    # print('sdf:'+str(len(ds.get_items())))
    # row_datas=[]
    # for row in ds.get_items():

    sheet = book.add_sheet(ds.get_name())
    for iX, itemX in enumerate(ds.get_items()):
        row = sheet.row(iX)
        # print('row='+str(iX))
        for iY, itemY in enumerate(itemX):
            # print(' iY='+str(iY)+' itemY='+str(itemY))
            try:
                # print('a')
                # pprint.pprint(itemY)
                if itemY is None:
                    row.write(iY, '')
                elif itemY.get_link() is not None:
                    row.write(iY, get_formula_hyperlink(itemY.get_link(), itemY.get_display()), link_style)
                elif itemY.get_formula() is not None:
                    row.write(iY, get_formula(itemY.get_formula()))
                else:
                    row.write(iY, itemY.get_display())

            except:
                raise
                # row.write(iY, itemY)
            if itemY is not None and itemY.get_col_width() is not None:
                sheet.col(iY).width = itemY.get_col_width()

def main():
    timestamp = strftime("%Y-%m-%d_%H-%M-%S")
    out_dir = 'outputs/'+timestamp+'_xl'
    os.makedirs(out_dir)
    out_file=out_dir+'/'+timestamp+'_test.xls'


    data_sets=[]
    data_sets.append(DataSet('dss1', [[Cell.from_link('one','http://www.google.com'),Cell.from_display('two')],[Cell.from_display('one2'),Cell.from_display('two2')]]))
    data_sets.append(DataSet('dss2', [[Cell.from_display('oneb'),Cell.from_display('twob')]]))

    book = Workbook()
    for ds in data_sets:
        # my_print_dataset(ds)

        add_data_set_sheet(ds, book)


    # sheet.write(1,0,Formula('HYPERLINK("http://www.google.com";"Python")'),style)


    # if len(row_data) > 0:
    book.save(out_file)


    os.system("start "+out_file)

if __name__ == '__main__':
    sys.exit(main())