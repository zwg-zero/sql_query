#! -*- coding: utf-8 -*-

task = (
    {'host':'10.13.2.125', 'port': 3306, 'user': 'root', 'passwd': 'tasdfasf', 'db': 'sdfaf',
     'mail_success_recipients': 'zhdfasf@eisfmfdasf.net',
     'mail_fail_recipients': 'zhdfsf@ohsdfsfua.net',
     'mail_success_sub': u'每日投资人数统计',
     'mail_fail_sub': u'FAIL IN Daily jubao investor number report',
     'mail_success_cont': u'每资人数统计',
     'mail_fail_cont': u'FAIL IN Daily investor number report',
     'attached_file': u'投资人数统计.xls',
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
    {'host':'10.13.2.125', 'port': 3306, 'user': 'root', 'passwd': 'sdgd3', 'db': 'jfddgao',
     'mail_success_recipients': 'zeigudddo@esdfs.net',
     'mail_fail_recipients': 'zho@oha.net',
     'mail_success_sub': u'每日投资总额统计',
     'mail_fail_sub': u'FAIL IN Daily  investor number report',
     'mail_success_cont': u'每日投资总额统计',
     'mail_fail_cont': u'FAIL IN Daily  investor number report',
     'attached_file': u'每投资总额统计.xls',
     'sql':
         """
            select
            (t2.vc_value) as 'a1',
            t1.vc_name as '姓名',
            t1.vc_account as '用户名',
            t1.pk_id as '用户id',
            date(t1.dt_create_time) as 'a2'
            from fiz_user t1
            left join fiz_user_prop t2 on t1.pk_id =t2.fk_user_id
            where t2.vc_code = 'code-identity-number'
            and date(t1.dt_create_time) >= '2015-05-11' and date(t1.dt_create_time) <= now()
            and t1.dc_type in('00', '07')
         """
     },
)
