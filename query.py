# -*- coding: utf8 -*-
import configure
import os
import time
import MySQLdb # install mysqlclient please
from xlwt import Workbook
import datetime
import logging
from envelopes import Envelope
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header

## setup logging
current_path = os.path.abspath(os.path.dirname(__file__))
log_file = os.path.join(current_path, "log.log")
logging.basicConfig(filename= log_file,
                    level=logging.INFO,
                    filemode='w',
                    format='%(asctime)s file:%(filename)s fun:%(funcName)s line:%(lineno)d %(levelname)s: %(message)s',
                    )

def query_db(host, port, user, passwd, db, query_sql, charset="utf8"):
    result = []
    db = MySQLdb.connect(host=host, user=user, port=port, passwd=passwd, db=db,
                         charset=charset)
    c = db.cursor()
    c.execute(query_sql)
    # save column name
    result.append([item[0] for item in c.description])
    for item in c.fetchall():
        # convert returned datetime.datetime or datetime.date to string
        item_content = []
        for sub_item in item:
            if type(sub_item) == datetime.datetime:
                sub_item = sub_item.strftime("%Y-%m-%d %H:%M:%S")
            elif type(sub_item) == datetime.date:
                sub_item = sub_item.strftime("%Y-%m-%d")
            item_content.append(sub_item)
        result.append(item_content)
    # for content in result:
        # print(content)
    return result


def write_xls(filename, content):
    book = Workbook(encoding='utf-8')
    sheet1 = book.add_sheet('Sheet 1')
    row_num = 0
    for row in content:
        col_num = 0
        for item in row:
            sheet1.write(row_num, col_num, item)
            col_num += 1
        row_num += 1
    book.save(filename)

# envelopes can't send attache file containing chinese characters in name
def send_mail_0(server='smtp.sina.com', user='yxxxxxxx@sina.com', password='xxxxxxx',
                recipients='zhouweiguo@eifm.net',
                subject="Test test",
                content="test test",
                attach_file=None):
    #print(receive_list)
    rec_list = recipients.split(', ')
    #print(type(rec_list))
    #print(rec_list)
    envelope = Envelope(from_addr=(user),
                        to_addr=rec_list,
                        subject=subject,
                        text_body=content,
                        )
    envelope.add_attachment(attach_file, 'application/octet-stream')
    envelope.send(server, login=user, password=password, tls=True)

def send_mail(attach_file=None, server='smtp.sina.com', user='xxxxxx@na.com', password='jjkkkfdjf-li8',
              recipients='zxxxxo@xxxx.net, pxxxxx@xxxx.net, zhossss@oddddhuanggua.net',
              subject="TEST report from pengfei",
              content="Attached please find today's report"
              ):
    #print(receive_list)
    #rec_list = receive_list.split()

    msg = MIMEMultipart()
    msg["subject"] = Header(subject, 'utf-8')
    msg["From"] = user
    msg["To"] = recipients
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    if attach_file:
        file_base_name = os.path.basename(attach_file)
        attach_part = MIMEBase('application', 'octet-stream')
        attach_part.set_payload(open(attach_file, 'rb').read())
        encoders.encode_base64(attach_part)
        attach_part.add_header('Content-Disposition', 'attachment',
                             filename=(Header(file_base_name, 'utf-8').encode()))
        msg.attach(attach_part)

    receive_list = [item for item in recipients.split(', ')]
    # try two times of sending mail
    try:
        s = smtplib.SMTP_SSL(server, timeout=30)
        s.login(user, password)
        s.sendmail(user, receive_list, msg.as_string())
        s.close()
    except Exception as e:
        print(str(e) + "/nTry again after 3s.")
        time.sleep(3)
        try:
            s = smtplib.SMTP_SSL(server, timeout=30)
            s.login(user, password)
            s.sendmail(user, receive_list, msg.as_string())
            s.close()
        except Exception as e:
            print(str(e))
            logging.error(str(e))


if __name__ == '__main__':
    for item in configure.task:
        content = ''
        try:
            content = query_db(item['host'], item['port'], item['user'], item['passwd'],
                               item['db'], item['sql'])
        except Exception as e:
            print(str(e) + '/nTry again.')
            logging.error(str(e) + '/nTry again.')
            time.sleep(3)
            try:
                content = query_db(item['host'], item['port'], item['user'], item['passwd'],
                                   item['db'], item['sql'])
            except Exception as e:
                print(str(e))
                logging.error(str(e))
                send_mail(subject=item['mail_fail_sub'], content=item['mail_fail_cont'],
                          attach_file=log_file, recipients=item['mail_fail_recipients'])
                exit()
        file_to_write = os.path.join(current_path, item['attached_file'])
        write_xls(file_to_write, content)
        print("file: %s write" % file_to_write)
        send_mail_0(subject=item['mail_success_sub'], content=item['mail_success_cont'],
                  attach_file=file_to_write, recipients=item['mail_success_recipients'])
        print("mail send")



