import urllib

import requests
import time

import jac
from jac.xl_builder import MainSheetBuilder


class Maps(object):
    def __init__(self):
        print('here')

    def get_json_for_address(self, address):
        # print(address)
        # address=urllib.quote(address)
        # print(address)
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote(address)
        print(url)
        r = requests.get(url)
        return r.content

    def get_case_number_url(self, cn):
        adate = time.strftime("%m/%d/%Y")  # '5/31/2014'
        # thedate=urllib2.quote(adate) why is this not escaping the fwd slash to %2F ?
        thedate = adate.replace('/', '%2F')
        print(thedate)
        # print(urllib.quote('/~connolly/'))
        # print (time.strftime("%m/%d/%Y"))
        return self.get_case_number_url2(thedate, cn)

    def get_case_number_url2(self, date_str, cn):
        return 'http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=1%2F1%2F1981&ed=' + date_str + '&n=&bt=OR&d=' + date_str + '&pt=-1&cn=' + cn + '&dt=ALL%20DOCUMENT%20TYPES&st=casenumber&ss=ALL%20DOCUMENT%20TYPES'

    def do_map_output(self, mrs, out_dir, sheet_name):
        map_file = out_dir + '/' + sheet_name + '/' + 'map.htm'
        ads = []
        for r in mrs.get_records():
            if 'bcpao_item' in r.get_item():
                if 'address' in r.get_item()['bcpao_item']:
                    my_d = {}
                    my_d['title'] = r.get_item()['bcpao_item']['address']
                    my_d['title'] = '"' + my_d['title'] + '"'
                    my_d['adr_geo'] = r.get_item()['bcpao_item']['address-geo'].replace('\n', ' ')
                    mystr = r.get_item()['bcpao_acc']
                    url = jac.bcpao.get_bcpao_query_url_by_acct(mystr)
                    bcpao_line = 'bcpao: ' + "<a href='" + url + "' target='_blank' '>" + mystr + "</a>"
                    case_title_line = '"case_title: ' + r.get_item()['case_number'] + '"'
                    subtitle_lines = []
                    subtitle_lines.append('count #: ' + str(r.get_item()['count']))
                    subtitle_lines.append(bcpao_line)
                    subtitle_lines.append('case_title: ' + str(r.get_item()['case_title']))
                    # my_d['subtitle'] += 'bclerk: '+xl_builder.get_case_number_url(r.get_item()['case_title'])
                    subtitle_lines.append(
                        'bclerk: ' + "<a href='" + str(self.get_case_number_url(r.get_item()['case_number'])).replace(' ',
                                                                                                                 '%20') + "' target='_blank' '>" + str(
                            r.get_item()['case_number']) + "</a>")
                    print('out_dir: ' + out_dir)
                    print('sheet_name: ' + sheet_name)
                    sheet_builder = MainSheetBuilder('')
                    print('link: ' + sheet_builder.get_case_info_link(r.get_item()))
                    case_info_relative_path = str(sheet_builder.get_case_info_link(r.get_item()))
                    case_info_relative_path = case_info_relative_path[
                                              1:]  # chopping off the leading fwd slash makes the browser treat it as a relative path, which makes the link it work
                    subtitle_lines.append(
                        'case_info: ' + "<a href='" + case_info_relative_path + "' target='_blank' '>" + 'link' + "</a>")
                    reg_actions_relative_path = str(sheet_builder.get_reg_actions_link(r.get_item()))
                    reg_actions_relative_path = reg_actions_relative_path[
                                                1:]  # chopping off the leading fwd slash makes the browser treat it as a relative path, which makes the link it work
                    subtitle_lines.append(
                        'reg_actions: ' + "<a href='" + reg_actions_relative_path + "' target='_blank' '>" + 'link' + "</a>")
                    subtitle_lines.append('assessed: ' + str(sheet_builder.get_assessed_str(r.get_item())))
                    subtitle_lines.append('base_area: ' + str(sheet_builder.get_base_area(r.get_item())))
                    subtitle_lines.append('year: ' + str(sheet_builder.get_year_built_str(r.get_item())))
                    # my_d['subtitle'] += case_title_line
                    my_d['subtitle'] = '<BR>'.join(subtitle_lines)
                    my_d['subtitle'] = '"' + my_d['subtitle'] + '"'
                    ads.append(my_d)
        if len(ads) > 0:
            with open(map_file, 'wb') as handle:
                html1 = '''
                <html>
    <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no"/>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
    <title>Google Maps JavaScript API v3 Example: Geocoding Simple</title>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript">
      var geocoder;
      var map;
      var address ="1117 egret lake way";
      var address2 ="1122 cheyenne dr indian harbour beach fl";
      function initialize() {
        geocoder = new google.maps.Geocoder();
        var latlng = new google.maps.LatLng(-34.397, 150.644);
        var myOptions = {
          zoom: 10,
          center: latlng,
        mapTypeControl: true,
        mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
        navigationControl: true,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var results_adr =

        '''
                html2 = '''

          function getAdder(the_result) {
    		  return (function() {
    			var marker = new google.maps.Marker({
    					position: the_result.adr_geo.results[0].geometry.location,
    					map: map,
    					title:the_result.adr_geo.results[0].formatted_address
    				});

    				var infowindow = new google.maps.InfoWindow(
    					{ content: '<b>'+the_result.title+'</b><br>'+the_result.subtitle+'</a>',
    					  size: new google.maps.Size(150,50)
    					});

    				google.maps.event.addListener(marker, 'click', function()
    				{
    				infowindow.open(map,marker);
    				});
    		  })()
          }


        map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
        //if (geocoder) {
          map.setCenter(results_adr[0].adr_geo.results[0].geometry.location);

    		for (i = 0; i < results_adr.length; i++) {
    			//geocoder.geocode( { 'address': cars[i]}, genGeocodeCallback(cars[i]));
    			//console.log(results_adr[i].results[0].formatted_address)
    			getAdder(results_adr[i]);
    		}
        //}
      }
    </script>
    </head>
    <body style="margin:50px; padding:0px;" onload="initialize()">
    placeholder for other info<br>
    <a href="http://www.google.com" target="_blank">link to google.com</a><br>
    <a href="http://www.google.com" target="_blank">link to foreclosures list</a><br>
    <a href="http://www.google.com" target="_blank">link to bcpao</a><br>
     <div id="map_canvas" style="width:100%; height:75%">
    </script>

    </body>
    </html>
    '''

                handle.write(html1)
                handle.write(str(ads).replace("'", ""))
                # print(str(ads))
                handle.write(html2)