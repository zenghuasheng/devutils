import sqlparse

sql_query = """
SELECT * FROM (
    SELECT date, count() as count FROM (
        SELECT uuid, toDate(create_time) AS date FROM default.task
        WHERE ((((project_uuid IN ('KE7pq2hY3M78GqNu'))) AND __deleted = 0 AND project_uuid = 'KE7pq2hY3M78GqNu' AND status = 1 AND team_uuid = '8e9QDNfW') AND create_time >= toDateTime('2023-09-11 00:00:00'))
    ) AS task
    GROUP BY date ORDER BY date ASC WITH FILL FROM toDate(toDateTime('2023-09-11 00:00:00')) TO toDate(now())+1
) AS secondBuilder
SETTINGS use_query_cache = true, query_cache_store_results_of_queries_with_nondeterministic_functions=1, query_cache_compress_entries=0, query_cache_min_query_duration=300
"""

parsed = sqlparse.parse(sql_query)

# 递归函数用于遍历并打印语法树
def traverse(stmt, level=0):
    prefix = "  " * level
    print(f"{prefix}{stmt.get_real_name()}")
    for token in stmt.tokens:
        if isinstance(token, sqlparse.sql.Statement):
            traverse(token, level + 1)

for stmt in parsed:
    traverse(stmt)
