import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from sqlalchemy import create_engine
import jieba.posseg as pseg

# 连接到 MySQL 数据库
# 请根据实际情况修改下面的数据库连接信息
db_connection_info = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': '',
    'database': 'blog'
}

engine = create_engine(f"mysql+mysqlconnector://{db_connection_info['user']}:{db_connection_info['password']}@{db_connection_info['host']}:{db_connection_info['port']}/{db_connection_info['database']}")

# 从数据库中读取数据
# query = "SELECT from_user, send_msg, res_msg FROM message where from_user = 'oxlcXw9YCql2m3RH0A3xVLw8oFo0'"
query = "SELECT from_user, send_msg FROM message where from_user = 'oxlcXw_nzSJleeUcTu3286eioG7A'"
df = pd.read_sql(query, engine)

# 合并 send_msg 和 res_msg 字段
# df['combined_msg'] = df['send_msg'].astype(str) + ' ' + df['res_msg'].astype(str)
df['combined_msg'] = df['send_msg'].astype(str)

# 分词
def cut_words(text):
    words = pseg.cut(text)
    # words = [word.word for word in words if word.flag.startswith('n') or word.flag.startswith('v')]
    words = [word.word for word in words if word.flag.startswith('n')]
    filtered_words = [word for word in words if len(word) > 1]
    return " ".join(filtered_words)

df['cut_msg'] = df['combined_msg'].apply(cut_words)

# 合并每个用户的消息
grouped_df = df.groupby('from_user')['cut_msg'].agg(lambda x: ' '.join(x)).reset_index()

# 生成词云
text = ' '.join(grouped_df['cut_msg'])
font_path = '/Library/Fonts/Arial Unicode.ttf'  # 替换为你的中文字体文件路径
wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(text)

# 保存词云图到文件
wordcloud.to_file('wordcloud_lxx.png')