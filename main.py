import requests
import sys
import unittest

class Test1(unittest.TestCase):
    def test_one(self):
        the_html= """<title>Foreclosure Sale List</title> 
                 <body><center><h3><font color=red>Foreclosure Auctions are held at 11:00 AM at the Brevard County Government Center North, Brevard Room, 518 S. Palm Avenue, Titusville, Florida.</font></h3></center></body> 
                <!doctype html public "-//w3c//dtd html 4.0 transitional//en">
                <html>
                <head>
                <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
                <meta name="Author" content="Brevard County Clerk of Circuit Courts">
                <style type="text/css">
                BODY {
                     font-family: MS Sans Serif;
                     font-size: 8pt ;
                     text-align: Left;
                     background-color: #FFFFFF;
                     color: #0;
                 }
                TH {
                     font-family: MS Sans Serif;
                     font-size: 10pt ;
                     text-align: Center;
                     background-color: #8282FF;
                     color: #FFFFFF;
                 }
                .oddrows {
                     font-family: MS Sans Serif;
                     font-size: 8pt ;
                     text-align: Left;
                     background-color: #FFFFFF;
                     color: #0;
                 }
                .evenrows {
                     font-family: MS Sans Serif;
                     font-size: 8pt ;
                     text-align: Left;
                     background-color: #FFFFBF;
                     color: #0;
                 }

                </style>
                <title></title>
                </head>
                <body>
                <p><b><font size=+2></font></b></p>
                <table border=2 cellpadding=2 cellspacing=1>
                <tr>
                <th>case_number</th>
                <th>case_title</th>
                <th>comment</th>
                <th>foreclosure_sale_date</th>
                </tr>
                <tr>
                <td class=oddrows>05-2008-CA-019393-XXXX-XX</td>
                <td class=oddrows>US BANK VS ALICIA RODRIGUEZ</td>
                <td class=oddrows>&nbsp;</td>
                <td class=oddrows>06/11/2014</td>
                </tr>
                <tr>
                <td class=oddrows>05-2012-CA-062010-XXXX-XX</td>
                <td class=oddrows>BANK NEW YORK VS ROBERT CASTRO</td>
                <td class=oddrows>&nbsp;</td>
                <td class=oddrows>11/05/2014</td>
                </tr>
                </table>
                </body>
                </html>"""
        soup = BeautifulSoup(the_html)
        print(soup.prettify())
        # assert_equals()

def main():
    print("hello")
    r = requests.get('http://vweb2.brevardclerk.us/Foreclosures/foreclosure_sales.html')
    lines = r.text.split('\n')
    print(lines)

if __name__ == '__main__':
    sys.exit(main())