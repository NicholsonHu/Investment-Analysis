# -*- coding: utf-8 -*-
import cx_Oracle
import pandas as pd
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

#从本地文件中读取所选债券代码
f = open('H:/1.预测模型/python/test1.csv', 'r', encoding='utf-8')
code = pd.read_csv(f, dtype='str')
#将读取的债券代码转化为"'011800114.IB','011800549.IB'"格式
codeset = code.values
l = []
for k in codeset:
    for j in k:
        l.append(j)
windcode= '\',\''.join(l)
windcode = '\'' + windcode + '\''

#连接数据库，提取所选债券详细信息
conn = cx_Oracle.connect('wd_user', 'Wande_user1', '10.50.221.100:1521/ORCL')
print('连接成功')
cur = conn.cursor()#游标
printHeader = True#首行
cur.execute("""SELECT CC.S_INFO_WINDCODE, CC.S_INFO_NAME, CC.TRADE_DT, CC.B_ANAL_YTM, CC.B_ANAL_DURATION
               FROM (SELECT AA.*, BB.S_INFO_NAME FROM (SELECT S_INFO_WINDCODE, TRADE_DT, B_ANAL_YTM, B_ANAL_DURATION
              FROM WDDB.CBondValuation WHERE S_INFO_WINDCODE IN ("""+windcode+""") ORDER BY S_INFO_WINDCODE, TRADE_DT) AA
              LEFT JOIN (SELECT S_INFO_WINDCODE, S_INFO_NAME FROM WDDB.CBondDescription) BB ON AA.S_INFO_WINDCODE = 
              BB.S_INFO_WINDCODE) CC INNER JOIN (SELECT TRADE_DAYS  FROM WDDB.CBondCalendar WHERE S_INFO_EXCHMARKET = 'NIB'
              ORDER BY TRADE_DAYS) DD    ON CC.TRADE_DT = DD.TRADE_DAYS ORDER BY S_INFO_WINDCODE, TRADE_DT""")
data = cur.fetchall() #读取所有记录

#将数据输出至csv
name = ['债券代码', '债券简称', '交易日期', '到期收益率', '久期']
test = pd.DataFrame(columns=name, data=data)
test.to_csv("H:/1.预测模型/python/outputtest.csv", index=False, sep=',', encoding='utf_8_sig')

cur.close() #关闭游标
conn.close() #关闭数据链接




