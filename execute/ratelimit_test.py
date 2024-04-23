import subprocess


def test_ratelimit():
    command = '''curl 'https://p1109-k3s-2.k3s-dev.myones.net/project/api/ones-project/team/F1mbN32a/test' \
-H 'Host: p1109-k3s-2.k3s-dev.myones.net' \
-H 'Connection: keep-alive' \
-H 'sec-ch-ua: "Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"' \
-H 'Accept: application/json, text/plain, */*' \
-H 'Accept-Language: zh' \
-H 'sec-ch-ua-mobile: ?0' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' \
-H 'sec-ch-ua-platform: "macOS"' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Sec-Fetch-Mode: cors' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Referer: https://p1109-k3s-2.k3s-dev.myones.net/project/' \
--cookie 'ajs_anonymous_id=be7324c7-fe87-40ca-8458-a97ce66d951f; ajs_user_id=WEDzSrNy; ones-uid=8eXaoEG3; ones-lt=b1KNuJD3RRDZqT7P6g8Ttw7HAzkF4yGVd1KbCXUJpcr48N9CeM4TkCSeZBjjhWik; timezone=Asia/Shanghai; language=zh; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22DmnHzYAA%22%2C%22first_id%22%3A%2218e798cd87114a4-0b324976c3ab708-1d525637-2073600-18e798cd872139b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiJEbW5IellBQSIsIiRpZGVudGl0eV9jb29raWVfaWQiOiIxOGU3OThjZDg3MTE0YTQtMGIzMjQ5NzZjM2FiNzA4LTFkNTI1NjM3LTIwNzM2MDAtMThlNzk4Y2Q4NzIxMzliIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22DmnHzYAA%22%7D%2C%22%24device_id%22%3A%2218e798cd87114a4-0b324976c3ab708-1d525637-2073600-18e798cd872139b%22%7D; ct=c38cf885aa3fc9a9e2a9c8636aa6724052190ec77f4d2d04985fc071f719f8d3'
'''
    for i in range(101):
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        if output.returncode != 0:
            print(output.stderr)
            break


if __name__ == '__main__':
    test_ratelimit()
