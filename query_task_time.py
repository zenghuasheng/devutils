import requests
import json
import time


def query_tasks(parent_uuids):
    url = 'https://plugin.k3s-dev.myones.net/project/api/project/team/DSsFH9nr/items/graphql?t=nextlevel'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg2ZTljZGY1LTIxZjItNDBmNi02YTVjLTJlYzExZTQxZTY5YiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsib25lcy52MSJdLCJjbGllbnRfaW5mbyI6eyJjbGllbnRfaXAiOiIyMTguMTcuMjE1LjE4In0sImV4cCI6MTcyMjk0MDgxOSwiaWF0IjoxNzIyOTM2OTE5LCJpc3MiOiJodHRwOi8vcGx1Z2luLmszcy1kZXYubXlvbmVzLm5ldC8iLCJqdGkiOiJlOTllYjM3OS0yZTAwLTRiMTItNTc4ZC1kYTQ5Y2MwYTE2NzIiLCJsb2dpbl90aW1lIjoxNzIyODMwODkzOTYxLCJuYmYiOjE3MjI5MzY5MTksIm9yZ191c2VyX3V1aWQiOiJYdVA3Zzg5OSIsIm9yZ191dWlkIjoiRnZGVDkyY2IiLCJyZWdpb25fdXVpZCI6ImRlZmF1bHQiLCJzY29wZXMiOlsib3BlbmlkIiwib2ZmbGluZV9hY2Nlc3MiLCJvbmVzOm9yZzpkZWZhdWx0OkZ2RlQ5MmNiOlh1UDdnODk5Il0sInNpZCI6IjY1NmM3ZGQxLWVjMTQtNDE3Yy02ZDQ4LTE3ZGI3YzdkOWI2ZSIsInN1YiI6IjZkZmNQTHpDOmRlZmF1bHQ6RnZGVDkyY2I6WHVQN2c4OTkifQ.gl7GIje16OLgJiLGTqdzYf6ecChXLLCGUXpxMFkS-cRdX0wyIyzCDxh-zeKJFLafoZNTFT2wIUjCZx1S4Sf-a_HwChQcdcnnu7RmGz_lly0hdcbVbwQtwcmE1r-SLvY7G-ukrKID53IeSUedzTIa1P7RpypHyoyPHLIeah1pl1Sxgq6Q58svMBXGOpLB5piTsPhTa2qxIwabOVOUe99UOYxCCmSy_8V34VCM2ibaIpGYYG7BHCgNPx6hq4I6_p_Z0VhTty5USlnyOZvCBXGa7ACxf4Ua2RjGNkCOtS43IqvVom-QlCRRACGg7WnYeZR6Oh_wCsIAbWxL8lWT28fcZQ',
        'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190baaa1d1d6a8-00c9a3b6ad31ef9-19525637-2073600-190baaa1d1e28fb%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwYmFhYTFkMWQ2YTgtMDBjOWEzYjZhZDMxZWY5LTE5NTI1NjM3LTIwNzM2MDAtMTkwYmFhYTFkMWUyOGZiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190baaa1d1d6a8-00c9a3b6ad31ef9-19525637-2073600-190baaa1d1e28fb%22%7D; ones-tz=Asia%2FShanghai; ones-region-uuid=default; ones-org-uuid=FvFT92cb; timezone=Asia/Shanghai; ones-ids-sid=f8def544-0c1d-4cd6-54d8-dfb300631e4d; ones-lang=zh; ct=6617887edab0da28f77b69cdbbadb8bd9cbf916663fa2f00d130e5fed2893298; ones-lt=eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg2ZTljZGY1LTIxZjItNDBmNi02YTVjLTJlYzExZTQxZTY5YiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsib25lcy52MSJdLCJjbGllbnRfaW5mbyI6eyJjbGllbnRfaXAiOiIyMTguMTcuMjE1LjE4In0sImV4cCI6MTcyMjk0MDgxOSwiaWF0IjoxNzIyOTM2OTE5LCJpc3MiOiJodHRwOi8vcGx1Z2luLmszcy1kZXYubXlvbmVzLm5ldC8iLCJqdGkiOiJlOTllYjM3OS0yZTAwLTRiMTItNTc4ZC1kYTQ5Y2MwYTE2NzIiLCJsb2dpbl90aW1lIjoxNzIyODMwODkzOTYxLCJuYmYiOjE3MjI5MzY5MTksIm9yZ191c2VyX3V1aWQiOiJYdVA3Zzg5OSIsIm9yZ191dWlkIjoiRnZGVDkyY2IiLCJyZWdpb25fdXVpZCI6ImRlZmF1bHQiLCJzY29wZXMiOlsib3BlbmlkIiwib2ZmbGluZV9hY2Nlc3MiLCJvbmVzOm9yZzpkZWZhdWx0OkZ2RlQ5MmNiOlh1UDdnODk5Il0sInNpZCI6IjY1NmM3ZGQxLWVjMTQtNDE3Yy02ZDQ4LTE3ZGI3YzdkOWI2ZSIsInN1YiI6IjZkZmNQTHpDOmRlZmF1bHQ6RnZGVDkyY2I6WHVQN2c4OTkifQ.gl7GIje16OLgJiLGTqdzYf6ecChXLLCGUXpxMFkS-cRdX0wyIyzCDxh-zeKJFLafoZNTFT2wIUjCZx1S4Sf-a_HwChQcdcnnu7RmGz_lly0hdcbVbwQtwcmE1r-SLvY7G-ukrKID53IeSUedzTIa1P7RpypHyoyPHLIeah1pl1Sxgq6Q58svMBXGOpLB5piTsPhTa2qxIwabOVOUe99UOYxCCmSy_8V34VCM2ibaIpGYYG7BHCgNPx6hq4I6_p_Z0VhTty5USlnyOZvCBXGa7ACxf4Ua2RjGNkCOtS43IqvVom-QlCRRACGg7WnYeZR6Oh_wCsIAbWxL8lWT28fcZQ',
    }
    query = """
    {
      tasks (
        filterGroup: $filterGroup
      ) {
        uuid
        path
        issueType {
          uuid
        }
      }
    }
    """

    variables = {
        "filterGroup": [
            {
                "parent_in": parent_uuids
            }
        ]
    }

    data = {
        "query": query,
        "variables": variables
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()


def recursive_query(parent_uuids):
    total_time = 0
    while parent_uuids:
        start_time = time.time()
        result = query_tasks(parent_uuids)
        elapsed_time = time.time() - start_time
        total_time += elapsed_time
        print(f"Query time: {elapsed_time:.2f} seconds")

        tasks = result['data']['tasks']
        if not tasks:
            break

        parent_uuids = [task['uuid'] for task in tasks]

    return total_time


if __name__ == "__main__":
    # initial_parents = ["XuP7g899PuWePJq9", "XuP7g899gJoueY8k"]
    # total_query_time = recursive_query(initial_parents)
    # print(f"Total query time: {total_query_time:.2f} seconds")
    # 这个过程进行 10 次，然后取平均值
    total_query_time = 0
    for i in range(10):
        initial_parents = ["XuP7g899PuWePJq9", "XuP7g899gJoueY8k"]
        total_query_time += recursive_query(initial_parents)
    print(f"Average query time: {total_query_time / 10:.2f} seconds")

