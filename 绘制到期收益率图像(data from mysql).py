import pymysql
import pandas as pd
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

windcode = '101554067.IB'
code = '\''+windcode+'\''
sql_order = """select * from test.天津城投债日行情 where Wind代码="""+code+""""""
data = get_mysql_data(sql_order)
data.columns = ['Wind代码', '交易日期', '成交量(手)', '收盘价(元)', '到期收益率', '久期', '修正久期', '凸性']

#绘制所选债券到期收益率图像
#设置画板
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot(data.loc[:, '交易日期'], data.loc[:, '到期收益率'], lw=1.8, c='skyblue', label=windcode, marker='o')
#图例置于图像上方居中
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width, box.height])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=3, frameon=False, fontsize=10)
#间隔显示x轴坐标
nrow = data.iloc[:, 0].size
num = nrow//5
xticks = list(range(0, nrow, num))
xticks.append(nrow-1)
plt.xticks(xticks)
#网格线
plt.grid(c='gainsboro', axis='y')
#边框颜色
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_color('lightgrey')
ax.spines['left'].set_color('lightgrey')
ax.spines['right'].set_visible(False)

#输出图像
#plt.savefig('H:/1.预测模型/python/line chart.png')
plt.show()

