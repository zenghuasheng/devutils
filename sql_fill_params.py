import re

# 原始SQL日志和参数
sql_log = '''
[SQL] 2024/07/23 07:22:24 SELECT COUNT(1) AS count FROM task WHERE team_uuid in (?) AND owner=? AND (summary, issue_type_uuid, sub_issue_type_uuid) NOT IN ((?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?),(?,?,?)); 
'''
parameters_log = '''
[1:"NDdzL73c" 2:"WSPhsP9D" 3:"未开始制作的订单支持自动取消" 4:"XPdwHqMg" 5:"" 6:""XPdwHqMg" 8:"" 9:"已开始制作的订单禁止用户取消" 10:"XPdwHqMg" 11:"" 12:"营销后台增加优惠券模块，支持商家自主发放优惠券" 13:"XPdwHqMg" 14:"" 15:"支持商家自主编辑、修改优惠券规则" 16:"XPdwHqMg" 17:"E2PS5gCA" 18:"支持商家自主删除优惠券:"E2PS5gCA" 24:"支持商家查看已发放优惠券" 25:"XPdwHqMg" 26:"E2PS5gCA" 27:"优惠券手动发放功能" 28:"XPdwHqMg" 29:"E2PS5gCA" 30:"支持设置优惠券自动发放和优惠券发放成功提醒功能" 31:"XPdwHqMg" 32:"E2PS5gCA" 33:"自动取消开关设置" 34:"Lepe37:"LepetTX1" 38:"" 39:"手动取消订单入口" 40:"LepetTX1" 41:"" 42:"取消订单分类增加自动取消" 43:"LepetTX1" 44:"" 45:"自动取消设置接口" 46:"LepetTX1" 47:"" 48:"取消订单增加新分类" 49:"LepetTX1" 50:"" 51:"通知客户端接口" 52:"LepetTX1" 订单二次确认弹窗" 58:"LepetTX1" 59:"" 60:"测试" 61:"LepetTX1" 62:"" 63:"测试用例编写" 64:"LepetTX1" 65:"" 66:"商家主动取消按钮点击没有反应" 67:"RVqL6d16" 68:"" 69:"取消订单后，未按时退款到对应账号" 70:"RVqL6d16" 71:"" 72:"取消订单后态未同步到购买方账号" 76:"RVqL6d16" 77:"" 78:"取消订单后，界面显示空白" 79:"RVqL6d16" 80:"" 81:"制作中的商家订单不应该显示取消按钮" 82:"RVqL6d16" 83:"" 84:"商家主动取消按钮点击没有生效、订单未取消" 85:"RVqL6d16" 86:""]
'''

# 提取参数
parameters = re.findall(r'\d+:"(.*?)"', parameters_log)

# 将参数填充到SQL语句中
sql_filled = sql_log
for param in parameters:
    sql_filled = sql_filled.replace('?', f"'{param}'", 1)

print(sql_filled)
