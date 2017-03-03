#! -*- coding: utf-8 -*-
baidu_gaojing_fatal = {"service_id": "9999",
                 "token": "d5cbe9b479b248e9c6a8",
                 }
baidu_gaojing_info = {"service_id": "8888",
                       "token": "37d027e07fff552",
                       }

task = (
    {'action': 'send_mail',
     'mail_smtp': 'smtp.google.com',
     'mail_login_user': 'ss_gaoj@gmail.com',
     'mail_login_password': 'EI_F',
     'mail_success_recipients': 'zuwe@bbb.net', # recipients should be in a string separated by comma
     'mail_success_cc_recipients': 'zuwe@bbb.net',
     'mail_success_bcc_recipients': '', # same as above
     'mail_fail_recipients': 'uo@edfdf.net',
     'mail_success_sub': u'每日投资人数统计',
     'mail_fail_sub': u'FAIL IN Daily  investor number report',
     'mail_success_cont': u'每日投资人数统计',
     'mail_fail_cont': u'FAIL IN Daily investor number report',
     'attached_file': u'投资人数统计.xlsx',
     'host':'10.13.2.125', 'port': 3306, 'user': 'root', 'passwd': 'test', 'db': 'ddddd',
     'sql':
         """
            select
            date(t3.dt_date) as '还款日期',
            truncate(sum(t3.nb_principal),2) as '还款本金',
            truncate(sum(t3.nb_interest),2) as '利息',
            truncate(sum(t3.nb_principal+t3.nb_interest+nb_fee),2) as '还款本息',
            count(*) as '笔数'
            from fiz_repay_plan t3
            left join fiz_loan t4 on t3.fk_loan_id =t4.pk_id
            where t3.dc_status ='00'
            and date(t3.dt_date) >= '2017-01-19' and date(t3.dt_date) <= '2017-02-18'
            and t4.dc_category_code not in ('9','11','12','14','15','5')
            group by 1
            order by 1
         """
     },
    {'action': 'upload_ftp',
     'ftp_host': '10.13.4.56',
     'ftp_user': 'ftpupload',
     'ftp_password': 'ftppassword',
     'attached_file': u'test_ftp_upload.xlsx',
     'remote_path': u'投资人明细-理财计划',
     'host':'10.13.2.125', 'port': 3306, 'user': 'root', 'passwd': 'test', 'db': 'database',
     'sql':
         """
            select
            date(t3.dt_date) as '还款日期',
            truncate(sum(t3.nb_principal),2) as '还款本金',
            truncate(sum(t3.nb_interest),2) as '利息',
            truncate(sum(t3.nb_principal+t3.nb_interest+nb_fee),2) as '还款本息',
            count(*) as '笔数'
            from fiz_repay_plan t3
            left join fiz_loan t4 on t3.fk_loan_id =t4.pk_id
            where t3.dc_status ='00'
            and date(t3.dt_date) >= '2017-01-19' and date(t3.dt_date) <= '2017-02-18'
            and t4.dc_category_code not in ('9','11','12','14','15','5')
            group by 1
            order by 1
         """
     },
)
