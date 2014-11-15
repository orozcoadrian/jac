import smtplib
import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import datetime

def pprinttable(rows): # http://stackoverflow.com/questions/5909873/python-pretty-printing-ascii-tables
    pass
#   if len(rows) > 0:
#     headers = rows[0]._fields
#     lens = []
#     for i in range(len(rows[0])):
#       lens.append(len(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x)))))
#     formats = []
#     hformats = []
#     for i in range(len(rows[0])):
#       if isinstance(rows[0][i], int):
#         formats.append("%%%dd" % lens[i])
#       else:
#         formats.append("%%-%ds" % lens[i])
#       hformats.append("%%-%ds" % lens[i])
#     pattern = " | ".join(formats)
#     hpattern = " | ".join(hformats)
#     separator = "-+-".join(['-' * n for n in lens])
#     print(hpattern % tuple(headers))
#     print(separator)
#     for line in rows:
#       print(pattern % tuple(line))

def do_emails(file_path, password):
    # Credentials (if needed)
        username = 'orozcoadrian'
        #username = 'spacecoastmarketing'
        #password = getpass.getpass()

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)

        #for i,e in enumerate(emails):
        fromaddr = 'orozcoadrian@gmail.com'
        #fromaddr = 'spacecoastmarketing@gmail.com'
        toaddr  = 'orozcoadrian@gmail.com'
        #toaddrs  = fromaddr#'spacecoastmarketing@gmail.com'
        #toaddr  = 'kumarvinaya@gmail.com'
        cc = []#['spacecoastmarketing@gmail.com']
        bcc = []
        message_text = 'Test5'
        message_subject = 'Subject5'

        # message = 'Subject: %s\r\n' % subject
        # message += "CC: %s\r\n" % ",".join(cc)
        # message += '\n\n'
        # message += '%s' % msg
        message = "From: %s\r\n" % fromaddr
        message += "To: %s\r\n" % toaddr
        message += "CC: %s\r\n" % ",".join(cc)
        # + "BCC: %s\r\n" % ",".join(bcc)
        message += "Subject: %s\r\n" % message_subject
        message += "\r\n"
        message += message_text
        toaddrs = [toaddr] + cc + bcc

        server.sendmail(fromaddr, toaddrs, message)
        # if i == 0:
            # break
        server.quit()

def my_send_mail(file_paths, password, subject, body):
    fromaddr = 'orozcoadrian@gmail.com'
    toaddr  = ['orozcoadrian@gmail.com']
    toaddr.append('spacecoastmarketing@gmail.com')
    message_text = body#'Test6'+' '+file_path
    #message_text+='\n'+file_path
    message_subject = subject#'Subject6'
    files=[]
    username = 'orozcoadrian'
    send_mail(username, password, fromaddr, toaddr, message_subject, message_text, file_paths, 'smtp.gmail.com:587')

def send_mail(username,password,send_from, send_to, subject, text, files=[], server="localhost"):
    assert isinstance(send_to, list)
    assert isinstance(files, list)

    msg = MIMEMultipart('alternative')
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text, 'html') )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

def get_dates_count_map(items2):
    dates_count_map = {}
    for i in items2:
        item = i.get_item()
        date = datetime.datetime.strptime(item['foreclosure_sale_date'], "%m/%d/%Y")
        if date not in dates_count_map:
            dates_count_map[date] = 1
        else:
            dates_count_map[date] += 1
    # with open(out_dir+'/'+'date_counts.txt', 'w') as handle:
    # for map_key in sorted(dates_count_map.keys()):
        # # handle.write(str(map_key) + ': ' + str(dates_count_map[map_key]) + '\n')
        # print(str(map_key) + ': ' + str(dates_count_map[map_key]))
    return dates_count_map

def print_small_texts(the_list,max2=20):
    for index, item in enumerate(the_list):
        # print('the_list['+str(index)+']: ' + item.encode('utf-8'))
        if len(item.encode('utf-8').strip()) > 0 and len(item.encode('utf-8')) < max2:
            print('the_list['+str(index)+']: ' + item.encode('utf-8'))