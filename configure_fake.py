#! -*- coding: utf-8 -*-
baidu_gaojing_fatal = {"service_id": "0000",
                 "token": "8240ffe79b479b248e9c6a8",
                 }
baidu_gaojing_info = {"service_id": "1111",
                       "token": "307d439a02c79335897fff552",
                       }

task = (
    {'execute_time': '1st every month 7:40',  # this is just for classify"
     'action': 'send_mail',
     'mail_smtp': 'smtp.mailserver.net',
     'mail_login_user': 'mailloginname@mailserver.net',
     'mail_login_password': 'password@youremail',
     'mail_success_recipients': 'mailrecipient1@mailserver.net, mailrecipient2@mailserver.net', # recipients should be in a string separated by comma
     'mail_success_cc_recipients': 'ccrecipient1@mailserver.net, ccrecipient2@mailserver.net',
     'mail_success_bcc_recipients': '', # same as above
     'mail_fail_recipients': 'failrecipient1@mailserver.net, failrecipient2@mailserver.net',
     'mail_success_sub': u'单标投资明细-月',
     'mail_fail_sub': u'FAIL IN 单标投资明细-月',
     'mail_success_cont': u'Dear xxxx，\n\n    关于2.0单标（按月）的结果已经发到邮箱，请您注意查收，谢谢。',
     'mail_fail_cont': u'FAIL IN 单标投资明细-月',
     'database': [
         {
             'local_path': u'/reports/单标投资明细-月',
             'attached_file': u'loan_detail_month.xlsx',
             'sheet_name': u'单标投资明细-月',
             'host':'172.16.0.1', 'port': 3306, 'user': 'databaseuser', 'passwd': 'databasepassword', 'db': 'youdatabase',
             'sql':
                 """
                 select
                  '2.0' as '平台',
                   t6.pk_id as '投资id',
                   t7.vc_name as '单标名称',
                   t7.nb_period as '锁定期',
                   case t7.dc_period_type
                   when  '00' then '按天算'
                   when  '01' then '按月算'
                   end as '计息方式（按月/按天)',
                   concat(left(t7.nb_rate*100,4),'%') as '年化收益率',
                   (t6.nb_amount) as '投资金额(元)',
                   t3.vc_name as '投资人姓名',
                     t3.vc_cellphone as '投资人手机号',
                     t4.vc_value  as '投资人身份证号',
                   t2.vc_name as '邀请人姓名',
                  t2.vc_cellphone as '邀请人手机号',
                     t5.vc_value as '邀请人身份证号',
                   '单标' as '计划类型',
                 """
             },
             # other items in database put here.
         ],
    },
    {'execute_time': '1st every month 7:40',  # this is just for classify"
     'action': 'send_mail',
     'mail_smtp': 'smtp.server.net',
     'mail_login_user': 'mailloginuser@mailserver.net',
     'mail_login_password': 'passordofmaillogin',
     'mail_success_recipients': 'recipient1@mailserver.net, recipient2@mailserver.net', # recipients should be in a string separated by comma
     'mail_success_cc_recipients': 'ccmailrecipient1@mailserver.net',
     'mail_success_bcc_recipients': '', # same as above
     'mail_fail_recipients': 'failrecipient1@mailserver.net, failrecipient2@mailserver.net',
     'mail_success_sub': u'后台投资明细-月',
     'mail_fail_sub': u'FAIL IN 后台投资明细-月',
     'mail_success_cont': u'Dear xxxx，\n\n    关于2.0投资明细（按月）的结果已经发到邮箱，请您注意查收，谢谢。',
     'mail_fail_cont': u'FAIL IN 后台投资明细-月',
     'database': [
         {
             'local_path': u'/reports/后台投资明细-月',
             'attached_file': u'investment_details_month.xlsx',
             'sheet_name': u'后台投资明细-月',
             'host':'172.16.0.1', 'port': 3306, 'user': 'username', 'passwd': 'password', 'db': 'xxxx',
             'sql':
                 """
                 select
                 '2.0' as '平台',
                 t4.pk_id as '投资id',
                 t5.vc_name as '计划名称',
                 t5.nb_period as '锁定期',
                 case t5.dc_period_type
                 when '00' then '按天'
                 when '01' then '按月'
                 end as '计息方式',
                       concat(left(t5.nb_rate*100,4),'%') as '年化收益率',
                      (t4.nb_amount) as '投资金额',
                               t3.vc_name as '投资人姓名',
                        t3.vc_cellphone as '投资人手机号',
                        t6.vc_value as '投资人身份证号',
                        t2.vc_name as '邀请人姓名',
                        t2.vc_cellphone as '邀请人手机号',
                        t7.vc_value  as '邀请人身份证号',
                         t8.vc_name as '计划类型',
                        t4.dt_datetime_start as '起息时间',
                 order by 10
                 """
         },
     ],
     },
     {'action': 'upload_ftp',
      'ftp_host': '10.13.2.52',
      'ftp_user': 'xxxxx',
      'ftp_password': 'xxxxx',
      'fail_cont': u'FAIL IN  战企月初ftp',
      'mail_smtp': 'smtp.mailserver.net',
      'mail_login_user': 'userlogin@mailserver.net',
      'mail_login_password': 'password',
      'mail_fail_recipients': 'mailrecipient1@mailserver, failrecipient2@mailserver.net',
      'mail_fail_sub': u'FAIL IN 战企月初ftp',
      'mail_fail_cont': u'FAIL IN 战企月初ftp',
      'database': [
          {
             'local_path': u'/reports/交明细-单标',
             'attached_file': u'Deal_Loan.xlsx',
             'remote_path': u'成交明细-单标',
             'sheet_name': u'成交明细-单标',
             'host':'172.16.1.9', 'port': 3306, 'user': 'ername', 'passwd': 'password', 'db': 'database',
             'sql':
                 """
                 select
                u.pk_id as '用户id',u.vc_name as '投资人姓名',up.vc_value as '身份证号',u.vc_account as '投资人用户名',t.money as '成交金额',date(t.dtime) as '成交日期'
                from
                (SELECT i.nb_amount as 'money',date(i.dt_datetime) as 'dtime' ,i.pk_id
                from fiz_invest i ,fiz_loan l
                where i.fk_loan_id = l.pk_id
                and l.dc_type in ('00','01')
                and  i.dc_status in ('10','90','99')
                and  i.dt_datetime >= '2015-05-11 00:00:00' and  i.dt_datetime <= now()
                )as t
                inner join fiz_invest i
                on i.pk_id=t.pk_id
                left join fiz_user u
                on i.fk_user_id = u.pk_id
                left join
                (select * from fiz_user_prop
                where vc_code = 'code-identity-number'
                ) up
                on u.pk_id = up.fk_user_id
                 """
          },
          # other items of database come here
     ],
     },
)
