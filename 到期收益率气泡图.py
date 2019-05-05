import pymysql
import pandas as pd
import time
import matplotlib.pyplot as plt

def get_mysql_data(sql_order):
    """
    提取mysql中的数据并返回dataframe格式的数据
    参数仅为sql语句
    :param sql_order:
    :return:
    """
    # 创建数据库连接（方法一）
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='111111', db='test', charset='utf8')
    cursor = conn.cursor()  # 初始化游标（创建游标）
    cursor.execute(sql_order)  # 执行sql语句
    data = cursor.fetchall()  # 获取查询结果
    # colname = cursor.description # 获取字段名
    # columns = []
    # for i in range(len(colname)):
    #     columns.append(colname[i][0])
    result = pd.DataFrame(list(data))
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return result

# 选定债券Wind代码
windcode = '101554067.IB'
code = '\''+windcode+'\''

# 从mysql提取债券日行情数据
sql_order = """select * from 天津城投债日行情 where Wind代码="""+code
data = get_mysql_data(sql_order)
data.columns = ['Wind代码', '交易日期', '成交量(手)', '收盘价(元)', '到期收益率', '久期', '修正久期', '凸性']
# 从mysql提取债券发行日
sql_order = """SELECT * FROM 天津城投债基本资料 WHERE Wind代码="""+code
info = get_mysql_data(sql_order)
info.columns = ['Wind代码', '债券简称', '发行人', '发行票面利率', '付息频率', '债券期限(年)', '发行日', '到期日']

# 从mysql提取债券发行日至今的中国债券市场交易日数据
today = time.strftime("%Y%m%d")
sql_order = """SELECT TRADE_DAYS FROM 中国债券市场交易日 WHERE TRADE_DAYS BETWEEN'"""\
            +info.loc[0, '发行日']+"""' AND '"""+today+"""'AND S_INFO_EXCHMARKET='NIB' ORDER BY TRADE_DAYS"""
date = get_mysql_data(sql_order)
date.columns = ['交易日期']

# 数据汇总
df = pd.merge(date, data.loc[:, ['交易日期', '到期收益率', '成交量(手)']], how='left', on='交易日期')

#绘制所选债券到期收益率图像
plt.rcParams['font.sans-serif'] = ['Times New Roman']  #指定默认字体

#设置画板
fig = plt.figure(1)
ax = plt.subplot(111)
# ax = plt.subplot(111, facecolor='k')
ax.scatter(df.loc[:, '交易日期'], df.loc[:, '到期收益率'], df.loc[:, '成交量(手)']/100, c='#FF9999', alpha=0.7)
# 设置y轴坐标范围
plt.ylim(ymin=0)
#间隔显示x轴坐标
nrow = df.iloc[:, 0].size
num = nrow//5
xticks = list(range(0, nrow, num))
plt.xticks(xticks)
#网格线
plt.grid(c='lightgrey')
#边框颜色
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_color('lightgrey')
ax.spines['left'].set_color('lightgrey')
ax.spines['right'].set_visible(False)

#输出图像
#plt.savefig('H:/1.预测模型/python/line chart.png')
plt.show()
