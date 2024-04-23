import argparse
import requests


def send_post_request_with_id(id):
    url = 'https://devopsour.ones.pro/api/environment/start'
    headers = {
        'Host': 'devopsour.ones.pro',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'Origin': 'https://devopsour.ones.pro',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://devopsour.ones.pro/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22R9o8QgKu%22%2C%22first_id%22%3A%22181ae269bf5cf6-02d82d82d82d82e-37796305-1296000-181ae269bf61a2e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiJSOW84UWdLdSIsIiRpZGVudGl0eV9jb29raWVfaWQiOiIxODFhZTI2OWJmNWNmNi0wMmQ4MmQ4MmQ4MmQ4MmUtMzc3OTYzMDUtMTI5NjAwMC0xODFhZTI2OWJmNjFhMmUifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22R9o8QgKu%22%7D%2C%22%24device_id%22%3A%22181ae269bf5cf6-02d82d82d82d82e-37796305-1296000-181ae269bf61a2e%22%7D; our-devops-token=R9o8QgKu%3ABrKFa7nsNIUolpM7wEm7Pn1rdvCHprQlpASbCcTWtKwGU8bigjo1p4Gy79St1WGf',
    }
    data = {'id': id}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f'Successfully started environment with ID {id}')
    else:
        print(f'Error starting environment with ID {id}: {response.text}')


def main():
    parser = argparse.ArgumentParser(description='Send POST requests to start environments')
    parser.add_argument('ids', metavar='ID', type=int, nargs='+',
                        help='One or more environment IDs to start')

    args = parser.parse_args()

    for env_id in args.ids:
        send_post_request_with_id(env_id)


if __name__ == '__main__':
    main()
