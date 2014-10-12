import xl3

class ColumnHandler(object):
    def __init__(self,col_header_display):
        self.col_header_display=col_header_display
    def get_col_header_display(self):
        return self.col_header_display
    def handle_add(self, headers):
        pass
    def handle_add_to_row(self, row, r):
        pass
class ClassicMapColumnHandler(ColumnHandler):
    def __init__(self,col_header_display):
        super(ClassicMapColumnHandler, self).__init__(col_header_display)
    def handle_add(self, headers):
            headers.append(xl3.Cell.from_link(self.get_col_header_display(), 'https://www.bcpao.us/scripts/esrimap.dll?name=Brevard1&cmd=map&id=20140608'))
    def handle_add_to_row(self, row, r):
        i=r.get_item()
        map_link_cell=None
        try:
            map_link_cell = xl3.Cell.from_link('map', i['bcpao_radius']['map_url'])
        except:
            pass
        row.append(map_link_cell)
class Avg250ColumnHandler(ColumnHandler):
    def __init__(self,col_header_display):
        super(Avg250ColumnHandler, self).__init__(col_header_display)
    def handle_add(self, headers):
            headers.append(xl3.Cell.from_display('avg 250'))
    def handle_add_to_row(self, row, r):
        i=r.get_item()
        avg_x = xl3.Cell.from_display('')
        try:
            if 'bcpao_radius' in i and 'entries' in i['bcpao_radius'] and len(i['bcpao_radius']['entries'])>0:
                avg_x = xl3.Cell.from_display(str(i['bcpao_radius']['entries'][0]['average']))
        except:
            raise
        row.append(avg_x)
class Avg500ColumnHandler(ColumnHandler):
    def __init__(self,col_header_display):
        super(Avg500ColumnHandler, self).__init__(col_header_display)
    def handle_add(self, headers):
            headers.append(xl3.Cell.from_display('avg 500'))
    def handle_add_to_row(self, row, r):
        i=r.get_item()
        avg_x = xl3.Cell.from_display('')
        try:
            if 'bcpao_radius' in i and 'entries' in i['bcpao_radius'] and len(i['bcpao_radius']['entries'])>1:
                avg_x = xl3.Cell.from_display(str(i['bcpao_radius']['entries'][1]['average']))
        except:
            raise
        row.append(avg_x)
class Avg750ColumnHandler(ColumnHandler):
    def __init__(self,col_header_display):
        super(Avg750ColumnHandler, self).__init__(col_header_display)
    def handle_add(self, headers):
            headers.append(xl3.Cell.from_display('avg 750'))
    def handle_add_to_row(self, row, r):
        i=r.get_item()
        avg_x = xl3.Cell.from_display('')
        try:
            if 'bcpao_radius' in i and 'entries' in i['bcpao_radius'] and len(i['bcpao_radius']['entries'])>2:
                avg_x = xl3.Cell.from_display(str(i['bcpao_radius']['entries'][2]['average']))
        except:
            raise
        row.append(avg_x)
class Avg1000ColumnHandler(ColumnHandler):
    def __init__(self,col_header_display):
        super(Avg1000ColumnHandler, self).__init__(col_header_display)
    def handle_add(self, headers):
            headers.append(xl3.Cell.from_display('avg 1000'))
    def handle_add_to_row(self, row, r):
        i=r.get_item()
        avg_x = xl3.Cell.from_display('')
        try:
            if 'bcpao_radius' in i and 'entries' in i['bcpao_radius'] and len(i['bcpao_radius']['entries'])>3:
                avg_x = xl3.Cell.from_display(str(i['bcpao_radius']['entries'][3]['average']))
        except:
            raise
        row.append(avg_x)