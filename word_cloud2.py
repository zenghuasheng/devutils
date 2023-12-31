import pymysql
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba.posseg as pseg

# 连接到你的MySQL数据库
db = pymysql.connect(
    host='',
    user='',
    password='',
    database='blog',
    charset='utf8mb4'
)

# 获取游标
cursor = db.cursor()

# 读取数据
sql = "SELECT from_user, send_msg FROM message where from_user = 'oxlcXw_nzSJleeUcTu3286eioG7A'"
cursor.execute(sql)
data = cursor.fetchall()

# 关闭数据库连接
cursor.close()
db.close()

# 处理数据并生成词云图
user_messages = {}
# 处理数据并统计词频
user_word_counts = {}

for row in data:
    from_user, send_msg = row
    content = send_msg
    if from_user not in user_messages:
        user_messages[from_user] = content
    else:
        user_messages[from_user] += ' ' + content


# 中文分词
def chinese_word_cut(text):
    words = pseg.cut(text)
    # words = [word.word for word in words if word.flag.startswith('n') or word.flag.startswith('v')]
    words = [word.word for word in words if word.flag.startswith('n')]
    filtered_words = [word for word in words if len(word) > 1]
    return " ".join(filtered_words)


# 保存每个用户前10的词频统计结果为文本文件
for user, word_counts in user_word_counts.items():
    filename = f"{user}_top10_word_counts.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Top 10 Words for User: {user}\n")
        for word, count in word_counts.most_common(10):
            file.write(f"{word}: {count}\n")
    print(f"Top 10 词频统计结果已保存到文件: {filename}")

font_path = '/Library/Fonts/Arial Unicode.ttf'  # 替换为你的中文字体文件路径
# 生成词云图并保存到文件
for user, messages in user_messages.items():
    messages_cut = chinese_word_cut(messages)
    if len(messages_cut) == 0:
        continue

    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(
        messages_cut)
    # 词语也保存一份
    filename = f"wordcloud_{user}.txt"
    with open(filename, 'w') as f:
        f.write(messages_cut)
    # 保存到文件
    filename = f"wordcloud_{user}.png"
    wordcloud.to_file(filename)
    print(f"词云图已保存到文件: {filename}")
