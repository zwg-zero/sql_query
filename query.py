# -*- coding: utf8 -*-
# use python2.7 on linux amd64

import configure  # configure.py is setting file of this program, format refer to configure_fake.py
import os
import time
import json
import requests
import arrow
import MySQLdb  # install mysqlclient please
from xlwt import Workbook
import datetime
import logging
import ftplib
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header

# setup logging
current_path = os.path.abspath(os.path.dirname(__file__))
log_file = os.path.join(current_path, "messages.log")
logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    filemode='w',
                    format='%(asctime)s file:%(filename)s fun:%(funcName)s line:%(lineno)d %(levelname)s: %(message)s',
                    )


# query db and retrieve result
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


# write sql query result to excel file
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


def send_mail(server, user, password,
              recipients,
              cc_recipients='',  # string separated by comma
              bcc_recipients='',  # same as above
              subject='TEST',
              content='TEST',
              attach_file=None,
              ):
    msg = MIMEMultipart()
    msg["subject"] = Header(subject, 'utf-8')
    msg["From"] = user
    msg["To"] = recipients
    if cc_recipients:
        msg["Cc"] = cc_recipients
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    if attach_file:
        file_base_name = os.path.basename(attach_file)
        attach_part = MIMEBase('application', 'octet-stream')
        attach_part.set_payload(open(attach_file, 'rb').read())
        encoders.encode_base64(attach_part)
        attach_part.add_header('Content-Disposition', 'attachment',
                               filename=(Header(file_base_name, 'utf-8').encode()))
        msg.attach(attach_part)

    receive_list = [item for item in recipients.split(', ')
                    ] + [item for item in cc_recipients.split(', ') if cc_recipients
                         ] + [item for item in bcc_recipients.split(', ') if bcc_recipients
                              ]
    # try two times of sending mail
    try:
        s = smtplib.SMTP_SSL(server, timeout=30)
        s.login(user, password)
        s.sendmail(user, receive_list, msg.as_string())
        s.close()
        return True
    except Exception as e:
        print(str(e) + "/nTry again after 3s.")
        time.sleep(3)
        try:
            s = smtplib.SMTP_SSL(server, timeout=30)
            s.login(user, password)
            s.sendmail(user, receive_list, msg.as_string())
            s.close()
            return True
        except Exception as e:
            print(str(e))
            logging.error(str(e))
            return False


# send message to baidu gaojing http://tonggao.baidu.com if send mail fail
def send_gaojing(service_id, token, message):
    data = {"service_id": service_id,
            "description": message,
            "event_type": "trigger"
            }
    resp = requests.post("http://gaojing.baidu.com/event/create",
                         data=json.dumps(data),
                         headers={
                             "servicekey": token,
                         },
                         timeout=3, verify=False
                         )
    result = json.loads(resp.content)
    print("The baidu Gaojing return message is: %s" % result["message"])
    logging.info("The baidu Gaojing return message is: %s" % result["message"])


def send_ftp(host, user, password, local_file, remote_path):
    remote_file_name = os.path.basename(local_file)
    try:
        ftp = ftplib.FTP(host, user, password, timeout=3)
        ftp.cwd(remote_path.encode("gb2312"))
        # print(ftp.pwd().decode('gb2312'))
        file_handler = open(local_file, 'rb')
        ftp.storbinary("STOR %s" % remote_file_name.encode('gb2312'), file_handler)
        file_handler.close()
        ftp.close()
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False
    return True


if __name__ == '__main__':
    for item in configure.task:
        content = ''
        # try to execute db query, totally twice tried
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
                # try to send alert mail if db query fail
                # if send_mail fail, send baidu gaojing
                # if sending baidu gaojing fail do nothing
                if send_mail(item['mail_smtp'], item['mail_login_user'], item['mail_login_password'],
                             item['mail_fail_recipients'],
                             subject=item['mail_fail_sub'],
                             content=item['mail_fail_cont'],
                             attach_file=log_file):
                    exit()
                else:
                    send_gaojing(configure.baidu_gaojing_info['service_id'], configure.baidu_gaojing_info['token'],
                                 item['mail_fail_cont'])
                    exit()
        # the above all successful, write query result into excel file under current path
        file_to_write = os.path.join(current_path, item['attached_file']) + '_' + arrow.now().format('YYYYMMDD') + \
                        '.xlsx'
        write_xls(file_to_write, content)
        print("file: %s write" % file_to_write)
        # read action from configure file, send_mail or upload file
        if item['action'] == 'send_mail':
            if not send_mail(item['mail_smtp'], item['mail_login_user'], item['mail_login_password'],
                             item['mail_success_recipients'],
                             cc_recipients=item['mail_success_cc_recipients'],
                             bcc_recipients=item['mail_success_bcc_recipients'],
                             subject=item['mail_success_sub'],
                             content=item['mail_success_cont'],
                             attach_file=file_to_write):
                send_gaojing(configure.baidu_gaojing_info['service_id'], configure.baidu_gaojing_info['token'],
                             item['mail_fail_cont'])
                exit()
            else:
                logging.info("successful in send file %s using mail" % file_to_write)
                print("successful in send file %s using mail" % file_to_write)
        elif item['action'] == 'upload_ftp':
            if not send_ftp(item['ftp_host'], item['ftp_user'], item['ftp_password'], file_to_write,
                            item['remote_path']):
                send_gaojing(configure.baidu_gaojing_info['service_id'], configure.baidu_gaojing_info['token'],
                             item['mail_fail_cont'])
                exit()
            else:
                logging.info("successful in upload file %s to ftp" % file_to_write)
                print("successful in upload file %s to ftp" % file_to_write)
