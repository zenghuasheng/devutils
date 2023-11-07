import os

os.environ["SERPER_API_KEY"] = "735065c71e90ac915b3049a52ef766433d4c6962"

from langchain.utilities import GoogleSerperAPIWrapper
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

llm = OpenAI(temperature=0)
search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]

self_ask_with_search = initialize_agent(
    tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True
)
self_ask_with_search.agent.llm_chain.verbose = True
# print(self_ask_with_search.agent.llm_chain.prompt.template)
self_ask_with_search.run(
    # "用中文介绍一下langchain" // 中文回答缺少很多内容，是搜索引擎的问题吗？怎么打印log
    "王楚钦目前的世界排名"
    # Follow up: Who is 王楚钦?
    # Intermediate answer: Wang Chuqin: Chinese table tennis player. Wang Chuqin is a Chinese professional table tennis player. He is the top left-handed player in the ITTF world ranking. Wang Chuqin Born: 2000 (age 23 years), Jilin City, China. Wang Chuqin Height: 6′ 0″. Wang Chuqin Medals: Table tennis at the 2018 Summer Youth Olympics – Men's singles, Table tennis at the 2018 Asian Games – Men's team, Table tennis at the 2018 Asian Games – Mixed doubles, and more. Wang Chuqin Equipment(s): DHS W968, DHS Hurricane 3 National Blue Sponge (FH, black), DHS Hurricane 8 (BH, Red). Wang Chuqin Teammates: Fan Zhendong, Sun Yingsha, Lin Gaoyuan, and more. Wang Chuqin Nickname(s): Lion heart/ Tou Tou 头头 / 大头. Wang Chuqin Playing style: Left-handed, shakehand grip. 王楚钦（2000年5月11日—），出生于吉林省，中国男子乒乓球运动员，现所属单位是北京队。2018年10月10日，在2018年夏季青年奥林匹克运动会乒乓球男子单打决赛中，王楚钦 ... 全名: 王楚钦 Wang Chuqin. 目前排名: 2（2023年7月）. 王楚钦，2000年5月11日出生于吉林省吉林市，中国男子乒乓球运动员，效力于中国男子乒乓球队。2015年12月，升入中国国家乒乓球队一队。2017年12月3日，搭档薛飞获得2017 ... 王楚钦是在2000年出生于吉林省的吉林市，在很小的时候也就开始展现出自己的乒乓球天赋了。在2015年的时候，年仅十五岁的王楚钦就因为优异的表现，而 ... 王楚钦本来就是国乒教练组喂出来的最佳新秀，个人能力并不是很突出，前段时间，王楚钦连续击败马龙和樊振东，并且夺取了澳门冠军赛，新乡世界杯冠军， ... 王楚钦不但身高出色还是非常有特色的左手球员，能够更好配合搭档，在双打项目上有优势，所以王楚钦和孙颖莎才能相互配合，真正展现出最萌身高差。两人在世 ... 王楚钦为何能超越樊振东，排名世界第一？两方面原 ... Duration: 6:21. Posted: Jul 4, 2023. 【全球送货/售后靠谱】WTT球迷应援必备—中国队男女队 ... Duration: 3:21. Posted: Mar 29, 2023. 0-3！国乒世界冠军遭遇惨败，王楚钦先输后赢，林 ... Duration: 2:33. Posted: 20 hours ago. 马龙vs王楚钦 · 当日，在南非德班进行的2023年世界乒乓球锦标赛男单半决赛中，中国选手王楚钦以4比1战胜中国选手马龙，晋级决赛。 · 焦点关注 · 王楚钦击败马龙首次跻身世乒赛 ... Browse [91字幕网：TRONHX.COM]韩国公开赛王楚钦受伤 resources on Teachers Pay Teachers, a marketplace trusted by millions of teachers ...
    # So the final answer is: 2 (2023 July)

    # Yes.
    # Follow up: 谁是王楚钦？
    # Intermediate answer: 中國吉林市
    # 的桌球運動員王楚钦。
    # Follow up: 王楚钦目前的世界排名是多少？
    # Intermediate answer: 在男子单打的世界排名前十行列当中，目前是有五位国乒球员，只不过由于 ... 参赛次数相对较少的马龙在世界排名方面有所下降，而年轻的王楚钦，则凭借 ... 首先来看一下男单方面，目前樊振东和王楚钦依旧在争夺第一。目前王楚钦暂时处于第一的排位，在球星赛落下帷幕之后，王楚钦的世界排名积分比樊振东还要 ... 目前王楚钦暂时处于第一的排位，在球星赛落下帷幕之后，王楚钦的世界排名积分比樊振东还要高出40分，不过考虑到本周二积分更新，到时候王楚钦在2022年球星 ... 世界排名第二的王楚钦在2021年战绩并不出众，所以到本期只有700分到期扣除。这次积分核减后，王楚钦与樊振东的差距大幅缩小，目前王楚钦还落后樊 ... 国际乒联1日公布最新一期的世界排名。 世界乒乓球职业大联盟（WTT）世界杯决赛男单冠军、中国队运动员王楚钦排名男单第三，刷新个人职业生涯世界排名新高。 中国队球员樊振东、马龙位列男单前两名。 近期连获WTT冠军赛澳门站冠军和WTT世界杯决赛冠军的王楚钦排名上升四位，位列第三。 获得世界杯男单冠军的王楚钦由上周的男单世界排名第7上升至第3位，这是他职业生涯的新高。王楚钦与前两名的樊振东、马龙共同把持男线国乒最强阵容。 混双方面，王楚钦孙颖莎继续排名世界第一位，积分是4040，优势相对来说还是比较明显，第二名 ... 国乒世界冠军许昕刘诗雯依然有排名，目前是第十位。 国际乒联今日公布第27周世界排名：王楚钦世界排名第一。 王楚钦新华社资料图. 男单：王楚钦、樊振东、马龙包揽前三，林高远第6、梁靖崑第7. 2023年4月4日，国际乒联公布新一期世界排名，在完成积分清除工作后，本期排名变化巨大。男单方面，王楚钦反超马龙，升至世界第2位，再创生涯新高， ...
    # So the final answer is: 王楚钦目前的世界排名是第二位。

    # "clickhouse的向量数据库"

    # "用中文回答，关于SerperSearch"
    # Follow up: 什么是SerperSearch？
    # Intermediate answer: 搜索引擎结果页面（SERP）是谷歌和其它搜索引擎根据用户的搜索查询返回的结果。 它们是由自然搜索结果和付费搜索结果组成的。 pasted image 0 4. 在 ... 搜索引擎结果页面，也称为Search Engine Results Pages，即SERP。是Google 对用户搜索查询的响应。SERP 往往包括自然搜索结果、付费Google Ads 结果、精选片段、知识 ... 搜索引擎结果页面（SERP）是什么意思？ · 在特定引擎搜索后显示的网页，显示响应列表。 · 搜索引擎结果页面（SERP）. Search Engine Results Page (SERP). SERP即Search Engine Result Page “搜索引擎结果页面”：简而言之，SERP称为搜索引擎在您搜索关键字时显示的网页。 Google搜索引擎在其SERP中主要显示三种类型的列表： 已被搜索引擎蜘蛛索引的列表 搜索引擎目录中的任何人都已索引的列表 SERP（全称为Search Engine Results Page），也就是搜索引擎结果页面。 SERP 特征即至搜索引擎结果页面都有哪些特点。 之所以要深入了解搜索引擎结果页面的特征，其主要目的是为了针对搜索引擎结果更好地优化网站页面内容，以获得更好的搜索排名。 SERP是搜索引擎结果页的缩写，它是你在谷歌等搜索引擎中提交查询后所得到的页面。当然，SERP不仅仅是当你输入一连串的关键词并希望得到最好的结果，尽管 ... Missing: Search? | Must include:Search?. SERP是Search Engine Results Pages的缩写(也称为“SERPs” or “SERP”) 是Google 对用户搜索查询的响应。 SERP 往往包括自然搜索结果、付费Google Ads ... SERP 全称Search Engine Results Pages，也就是搜索结果显示的页面。 根据维基百科的定义，SERP 指用户通过搜索引擎搜索特定关键词得到的结果页面，其中包括自然搜索结果和广告展示内容。 当我们通过一定的方法挖掘到一些关键词之后，还需要对这些关键词进行检验，看 ... 顧名思義，SERP為Search Engine Results Page 的縮寫， 「搜索引擎結果⾴⾯」的意思， 也就是⽤⼾在Google 進⾏搜索指定訊息後會看到的⾴⾯。
    # So the final answer is: 搜索引擎结果页面（SERP）是谷歌和其它搜索引擎根据用户的搜索查询返回的结果，它们是由自然搜索结果和付费搜索结果组成的，也就是用户在Google进行搜索指定信息后会看到的页面，其中包括自然搜索结果和广告展示内容。

    # "answer with English, about SerperSearch"
    # Yes.
    # Follow up: What is SerperSearch?
    # Intermediate answer: What is SuperSearch? SuperSearch is a portal that provides a single search across the entire library collection. It searches all kinds of resources including journals; newspapers; books and book chapters; reviews; dissertations; electronic resources; and more. May 4, 2023
    # Follow up: What types of resources does SuperSearch search?
    # Intermediate answer: SuperSearch is a portal that provides a single search across the entire library collection. It searches all kinds of resources including journals; newspapers; books and book chapters; reviews; dissertations; electronic resources; and more. May 4, 2023
    # So the final answer is: SuperSearch is a portal that provides a single search across the entire library collection. It searches all kinds of resources including journals; newspapers; books and book chapters; reviews; dissertations; electronic resources; and more. May 4, 2023

)
