import time

import requests

proxies = {
    'http': 'http://localhost:9090',
    'https': 'http://localhost:9090',
}

# curl 'https://memory.k3s-dev.myones.net/project/api/project/team/WA7zYRTi/notices/info?type=1' \
# -H 'Host: memory.k3s-dev.myones.net' \
# -H 'Connection: keep-alive' \
# -H 'sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"' \
# -H 'Accept: application/json, text/plain, */*' \
# -H 'Accept-Language: zh' \
# -H 'sec-ch-ua-mobile: ?0' \
# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36' \
# -H 'sec-ch-ua-platform: "macOS"' \
# -H 'Sec-Fetch-Site: same-origin' \
# -H 'Sec-Fetch-Mode: cors' \
# -H 'Sec-Fetch-Dest: empty' \
# -H 'Referer: https://memory.k3s-dev.myones.net/project/' \
# --cookie 'sensorsdata2015jssdkcross=; language=zh; ones-uid=MpC3gsRq; ones-lt=NwIJh6AqUzEYpep45mica6R91q3mphOD9joVIPviAVBQYDD7UKmLo9vHGUrvAaot; timezone=Asia/Shanghai; ct=cbf1addf8c6ba86f84eb131949d16d3f9f5a8f8433218436a5167d181954401e' \
# --proxy http://localhost:9090

cookies = {
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMTUzZWJmMGVlYi0wNjVkNDUwYTBiMThjYWMtMWE1MjU2MzctMjA3MzYwMC0xOTAxNTNlYmYwZjIzYTcifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%7D',
    'language': 'zh',
    'ones-uid': 'MpC3gsRq',
    'ones-lt': 'NwIJh6AqUzEYpep45mica6R91q3mphOD9joVIPviAVBQYDD7UKmLo9vHGUrvAaot',
    'timezone': 'Asia/Shanghai',
    'ct': 'cbf1addf8c6ba86f84eb131949d16d3f9f5a8f8433218436a5167d181954401e',
}

headers = {
    'Host': 'memory.k3s-dev.myones.net',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'X-CSRF-TOKEN': '4813f0c74e8983ef600e3be05175e3dc77cc210a1b58d228a3ea5c09e731a013',
    'Accept-Language': 'zh',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua-platform': '"macOS"',
    'Origin': 'https://memory.k3s-dev.myones.net',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://memory.k3s-dev.myones.net/project/',
    'Content-Type': 'application/json;charset=UTF-8',
    # 'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMTUzZWJmMGVlYi0wNjVkNDUwYTBiMThjYWMtMWE1MjU2MzctMjA3MzYwMC0xOTAxNTNlYmYwZjIzYTcifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190153ebf0eeb-065d450a0b18cac-1a525637-2073600-190153ebf0f23a7%22%7D; language=zh; ones-uid=E2VDNNai; ones-lt=0eVh2h7q5hPrMH3s7yALcGGOvXWkmfT8ScXhfNaX7YaNcRoNDwhVrYQxaP6A8SmJ; timezone=Asia/Shanghai; ct=4813f0c74e8983ef600e3be05175e3dc77cc210a1b58d228a3ea5c09e731a013',
}

params = {
    't': 'group-task-data',
}

json_data = {
    "query": "{\n  tasks(filter: { uuid_in:$taskUUIDs}) \n    {\n    uuid\n    name\n    subIssueType{\n      uuid\n      name\n    }\n    links{\n      taskLinkTypeUUID\n      taskUUID\n    }\n    relatedTasks{\n      uuid\n      subIssueType{\n        uuid\n      }\n      issueType{\n        uuid\n        name\n      }\n      manhours{\n        hours\n        owner {\n          company\n        }\n      } \n    }\n    subTasks{\n      uuid\n      subIssueType{\n        uuid\n        name\n      }\n      manhours{\n        hours\n        owner {\n            company\n        }\n      }\n    } \n    issueType{\n      uuid\n      name\n    }\n    manhours{\n      hours\n      owner {\n        company\n      }\n    } \n  }\n}",
    "variables": {"taskUUIDs":
                      ['MpC3gsRq171ekKrs',
                       'MpC3gsRq3TDAQAjo', 'MpC3gsRq6CYhyR8q', 'MpC3gsRq6NHyZ9og',
                       'MpC3gsRq6Q8JyLDH', 'MpC3gsRq9H76mgM4', 'MpC3gsRqDCpFijDn', 'MpC3gsRqE6TkQ7Cm',
                       'MpC3gsRqEsnP6Uoh', 'MpC3gsRqFjDSf8KN', 'MpC3gsRqN8cdniqm', 'MpC3gsRqNXdz8Kya',
                       'MpC3gsRqQygD8Svu', 'MpC3gsRqRRJmBRt3', 'MpC3gsRqU4GWG4xU', 'MpC3gsRqWp6WTkgN',
                       'MpC3gsRqX8zNx9J3', 'MpC3gsRqXWWDboMz', 'MpC3gsRqXbyMbWw7', 'MpC3gsRq00630cc3',
                       'MpC3gsRq009d2fe6', 'MpC3gsRq00c21f55', 'MpC3gsRq012c0bce', 'MpC3gsRq018691d8',
                       'MpC3gsRq01d5beb1', 'MpC3gsRq022a9a7d', 'MpC3gsRq022bbcad', 'MpC3gsRq0232448c',
                       'MpC3gsRq0247635b', 'MpC3gsRq024d46c0', 'MpC3gsRq02891e63', 'MpC3gsRq02b43a21',
                       'MpC3gsRq03079875', 'MpC3gsRq036b8988', 'MpC3gsRq03f101cc', 'MpC3gsRq041c6fe7',
                       'MpC3gsRq04ac8ac0', 'MpC3gsRq051128f9', 'MpC3gsRq0546351c', 'MpC3gsRq05807351',
                       'MpC3gsRq062efc0d', 'MpC3gsRq0652ef13', 'MpC3gsRq06548860', 'MpC3gsRq067705db',
                       'MpC3gsRq068465d9', 'MpC3gsRq068f2b9e', 'MpC3gsRq06ccc99e', 'MpC3gsRq06f694e6',
                       'MpC3gsRq07298b95', 'MpC3gsRq07411a0c', 'MpC3gsRq07ae6d5e', 'MpC3gsRq07b8f1a4',
                       'MpC3gsRq07da95a7', 'MpC3gsRq07e393e4', 'MpC3gsRq08266a70', 'MpC3gsRq082f0b2c',
                       'MpC3gsRq08319716', 'MpC3gsRq08608ce5', 'MpC3gsRq088249b3', 'MpC3gsRq0898dcd4',
                       'MpC3gsRq08e1b500', 'MpC3gsRq09536c3a', 'MpC3gsRq09ebfe43', 'MpC3gsRq0a650ebc',
                       'MpC3gsRq0a83dba4', 'MpC3gsRq0aebf285', 'MpC3gsRq0af09b4f', 'MpC3gsRq0b30062c',
                       'MpC3gsRq0ba778be', 'MpC3gsRq0bca72f0', 'MpC3gsRq0c4d98ed', 'MpC3gsRq0c670918',
                       'MpC3gsRq0c8bc590', 'MpC3gsRq0d62d224', 'MpC3gsRq0dae085d', 'MpC3gsRq0df232de',
                       'MpC3gsRq0df4e848', 'MpC3gsRq0e1ca89a', 'MpC3gsRq0f289380', 'MpC3gsRq0f5e0f7f',
                       'MpC3gsRq0f67b77b', 'MpC3gsRq0f6f7e66', 'MpC3gsRq0f8f3253', 'MpC3gsRq0ffeef86',
                       'MpC3gsRq10ddb376', 'MpC3gsRq114a3487', 'MpC3gsRq11ccd65a', 'MpC3gsRq11f65ffe',
                       'MpC3gsRq1259d27f', 'MpC3gsRq12867289', 'MpC3gsRq12942a2c', 'MpC3gsRq12a77908',
                       'MpC3gsRq130e4717', 'MpC3gsRq131776e0', 'MpC3gsRq133a3759', 'MpC3gsRq13ca99e5',
                       'MpC3gsRq145a2854', 'MpC3gsRq15226d24', 'MpC3gsRq15a6716c', 'MpC3gsRq15c05c13',
                       'MpC3gsRq170c2811', 'MpC3gsRq1777faab', 'MpC3gsRq1817fd06', 'MpC3gsRq186b4fcb',
                       'MpC3gsRq18a3a56e', 'MpC3gsRq18c23613', 'MpC3gsRq19231863', 'MpC3gsRq1923b830',
                       'MpC3gsRq19377f5a', 'MpC3gsRq194f63e4', 'MpC3gsRq1950885e', 'MpC3gsRq19624124',
                       'MpC3gsRq1978b129', 'MpC3gsRq19d58043', 'MpC3gsRq19e57c15', 'MpC3gsRq1b748ef7',
                       'MpC3gsRq1b7cb6b6', 'MpC3gsRq1be1a882', 'MpC3gsRq1c060623', 'MpC3gsRq1c7b6b76',
                       'MpC3gsRq1c8081f3', 'MpC3gsRq1c845a7a', 'MpC3gsRq1c9b014f', 'MpC3gsRq1cc98dc2',
                       'MpC3gsRq1d00e1ea', 'MpC3gsRq1d683520', 'MpC3gsRq1dac2326', 'MpC3gsRq1e140eb2',
                       'MpC3gsRq1e3270b2', 'MpC3gsRq1e4d35df', 'MpC3gsRq1e96599e', 'MpC3gsRq1eb6162d',
                       'MpC3gsRq1f2a2de9', 'MpC3gsRq1f3443a8', 'MpC3gsRq1f738aef', 'MpC3gsRq200985bf',
                       'MpC3gsRq201d2337', 'MpC3gsRq2025612f', 'MpC3gsRq20357576', 'MpC3gsRq2042b310',
                       'MpC3gsRq21846e93', 'MpC3gsRq221b2a05', 'MpC3gsRq2234d4cc', 'MpC3gsRq2267ca49',
                       'MpC3gsRq22cb22b7', 'MpC3gsRq22d63cd9', 'MpC3gsRq24b582dc', 'MpC3gsRq24cd64b0',
                       'MpC3gsRq24e58d3a', 'MpC3gsRq252d32ce', 'MpC3gsRq25d223ad', 'MpC3gsRq26925536',
                       'MpC3gsRq26b6b5d3', 'MpC3gsRq273c5838', 'MpC3gsRq27983425', 'MpC3gsRq27d33a54',
                       'MpC3gsRq27d594f5', 'MpC3gsRq27e3f6fb', 'MpC3gsRq2890d36f', 'MpC3gsRq289e04d6',
                       'MpC3gsRq28b1f5e4', 'MpC3gsRq290ec638', 'MpC3gsRq298aae6f', 'MpC3gsRq29b04209',
                       'MpC3gsRq29d8afbb', 'MpC3gsRq29e0a0bd', 'MpC3gsRq29f6e40f', 'MpC3gsRq2a032954',
                       'MpC3gsRq2a2550c9', 'MpC3gsRq2a761c25', 'MpC3gsRq2a85dcb1', 'MpC3gsRq2b5f5cb1',
                       'MpC3gsRq2b7ebede', 'MpC3gsRq2baf8ffd', 'MpC3gsRq2bc552ba', 'MpC3gsRq2bcb33d9',
                       'MpC3gsRq2c96c3c9', 'MpC3gsRq2ca77ea1', 'MpC3gsRq2d04879d', 'MpC3gsRq2d20f504',
                       'MpC3gsRq2d3702d0', 'MpC3gsRq2de43f73', 'MpC3gsRq2de84322', 'MpC3gsRq2e06c92a',
                       'MpC3gsRq2e3ce499', 'MpC3gsRq2e9eac82', 'MpC3gsRq2ebf38bf', 'MpC3gsRq2ec69d75',
                       'MpC3gsRq2f4a3341', 'MpC3gsRq2f9f46cb', 'MpC3gsRq3006e23d', 'MpC3gsRq306c3099',
                       'MpC3gsRq307fa6c6', 'MpC3gsRq309dc9bc', 'MpC3gsRq30e7e80a', 'MpC3gsRq31300864',
                       'MpC3gsRq31726a58', 'MpC3gsRq31d1e6e3', 'MpC3gsRq3229e4c4', 'MpC3gsRq33087471',
                       'MpC3gsRq33b1ce0a', 'MpC3gsRq3416cdff', 'MpC3gsRq34349645', 'MpC3gsRq34f103c1',
                       'MpC3gsRq35487910', 'MpC3gsRq357d7522', 'MpC3gsRq359ebb25', 'MpC3gsRq35b4fc5e',
                       'MpC3gsRq35b9c241', 'MpC3gsRq35d47245', 'MpC3gsRq35ecf4e8', 'MpC3gsRq35f47dbb',
                       'MpC3gsRq3610c175', 'MpC3gsRq363e492d', 'MpC3gsRq37f867b7', 'MpC3gsRq385618e3',
                       'MpC3gsRq3860c8a6', 'MpC3gsRq388e493b', 'MpC3gsRq39bda7f8', 'MpC3gsRq39d00bf5',
                       'MpC3gsRq3a174ccc', 'MpC3gsRq3a21b3c2', 'MpC3gsRq3a823a24', 'MpC3gsRq3a938845',
                       'MpC3gsRq3aaa5d06', 'MpC3gsRq3b2c605c', 'MpC3gsRq3b81bffa', 'MpC3gsRq3bd1d6d9',
                       'MpC3gsRq3c5e1f30', 'MpC3gsRq3ca43d6e', 'MpC3gsRq3cc68423', 'MpC3gsRq3d00d6d6',
                       'MpC3gsRq3d088aa8', 'MpC3gsRq3d6cd8a2', 'MpC3gsRq3da3ba56', 'MpC3gsRq3e2d0731',
                       'MpC3gsRq3e56c28e', 'MpC3gsRq3e91679a', 'MpC3gsRq3ef8d810', 'MpC3gsRq3f0da6ac',
                       'MpC3gsRq3f3b6c04', 'MpC3gsRq3f4b856e', 'MpC3gsRq3fe92c18', 'MpC3gsRq4036689d',
                       'MpC3gsRq40498931', 'MpC3gsRq411ea330', 'MpC3gsRq412a8ca5', 'MpC3gsRq412f296d',
                       'MpC3gsRq41d241ed', 'MpC3gsRq41db3f54', 'MpC3gsRq421173dd', 'MpC3gsRq4218ee86',
                       'MpC3gsRq4248c026', 'MpC3gsRq4279831b', 'MpC3gsRq42983497', 'MpC3gsRq429d325d',
                       'MpC3gsRq42eb3921', 'MpC3gsRq42fc8626', 'MpC3gsRq43089440', 'MpC3gsRq438919e2',
                       'MpC3gsRq4411274f', 'MpC3gsRq44e93111', 'MpC3gsRq44ff825b', 'MpC3gsRq45324ec8',
                       'MpC3gsRq453fef74', 'MpC3gsRq459d6de4', 'MpC3gsRq45d922d6', 'MpC3gsRq464e7978',
                       'MpC3gsRq473ab01a', 'MpC3gsRq4844c09e', 'MpC3gsRq4849051a', 'MpC3gsRq48b5aa9a',
                       'MpC3gsRq491d9ecf', 'MpC3gsRq49338f47', 'MpC3gsRq4956fd3b', 'MpC3gsRq495e2b1a',
                       'MpC3gsRq49651924', 'MpC3gsRq497587a9', 'MpC3gsRq49e7de37', 'MpC3gsRq4DcSs1Ti',
                       'MpC3gsRq4EeUXNcP', 'MpC3gsRq4a9603c7', 'MpC3gsRq4af7f893', 'MpC3gsRq4b2c58ca',
                       'MpC3gsRq4c019bb8', 'MpC3gsRq4c332974', 'MpC3gsRq4cc66fbc', 'MpC3gsRq4ce19901',
                       'MpC3gsRq4d1ba4ed', 'MpC3gsRq4d443a52', 'MpC3gsRq4dcb1380', 'MpC3gsRq4e40c8d4',
                       'MpC3gsRq4f1ea292', 'MpC3gsRq4f5147da', 'MpC3gsRq4khPumH9', 'MpC3gsRq50a2969b',
                       'MpC3gsRq50b1f928', 'MpC3gsRq515a99aa', 'MpC3gsRq515ddfa9', 'MpC3gsRq51906f5e',
                       'MpC3gsRq51fdabbb', 'MpC3gsRq52242a5f', 'MpC3gsRq52361c75', 'MpC3gsRq52584bef',
                       'MpC3gsRq5283ee98', 'MpC3gsRq5298f1f9', 'MpC3gsRq52a4fa85', 'MpC3gsRq52a57935',
                       'MpC3gsRq532ff3c4', 'MpC3gsRq53585b2d', 'MpC3gsRq5376bdad', 'MpC3gsRq53a5293d',
                       'MpC3gsRq53bbf511', 'MpC3gsRq53eff918', 'MpC3gsRq545bd96a', 'MpC3gsRq550bf384',
                       'MpC3gsRq55413f13', 'MpC3gsRq55b256a9', 'MpC3gsRq55d03ccd', 'MpC3gsRq55e8db4a',
                       'MpC3gsRq563498ff', 'MpC3gsRq569d0f32', 'MpC3gsRq56b7ac27', 'MpC3gsRq5710a687',
                       'MpC3gsRq573dd016', 'MpC3gsRq57b0d8ff', 'MpC3gsRq57fc8c80', 'MpC3gsRq5802992a',
                       'MpC3gsRq58332ceb', 'MpC3gsRq59601ba6', 'MpC3gsRq5995c2c0', 'MpC3gsRq59f78a76',
                       'MpC3gsRq5b1c649a', 'MpC3gsRq5b5a9f98', 'MpC3gsRq5ba493ce', 'MpC3gsRq5bebbe70',
                       'MpC3gsRq5c4b490b', 'MpC3gsRq5c65d243', 'MpC3gsRq5c6d6273', 'MpC3gsRq5ce7c6f0',
                       'MpC3gsRq5cea7ce5', 'MpC3gsRq5d0d0017', 'MpC3gsRq5d289270', 'MpC3gsRq5d61a445',
                       'MpC3gsRq5dad0f8e', 'MpC3gsRq5db7276d', 'MpC3gsRq5dbe7a75', 'MpC3gsRq5e2dca3f',
                       'MpC3gsRq5e984f71', 'MpC3gsRq5ed11924', 'MpC3gsRq5ed1a959', 'MpC3gsRq5ed4585e',
                       'MpC3gsRq5f14ef97', 'MpC3gsRq5f162f55', 'MpC3gsRq5f8bbcd3', 'MpC3gsRq5f9bdbae',
                       'MpC3gsRq5fc564c5', 'MpC3gsRq5myfwCdq', 'MpC3gsRq600fde4b', 'MpC3gsRq607d2e4b',
                       'MpC3gsRq60abbc46', 'MpC3gsRq60e9ce7b', 'MpC3gsRq6114fd18', 'MpC3gsRq613d226b',
                       'MpC3gsRq614c16e6', 'MpC3gsRq6260c3d3', 'MpC3gsRq627e3412', 'MpC3gsRq62a9fc3e',
                       'MpC3gsRq62b2a919', 'MpC3gsRq62c2ecda', 'MpC3gsRq62dee2cd', 'MpC3gsRq6317fb80',
                       'MpC3gsRq63480287', 'MpC3gsRq63aff040', 'MpC3gsRq63c70b90', 'MpC3gsRq64395af1',
                       'MpC3gsRq64557dea', 'MpC3gsRq6491530a', 'MpC3gsRq64a50147', 'MpC3gsRq64fc41c2',
                       'MpC3gsRq65a3439a', 'MpC3gsRq65efd724', 'MpC3gsRq66575298', 'MpC3gsRq66781cdf',
                       'MpC3gsRq670426ec', 'MpC3gsRq6758e393', 'MpC3gsRq67bb5b84', 'MpC3gsRq67eecf28',
                       'MpC3gsRq67f0fad6', 'MpC3gsRq680c63a4', 'MpC3gsRq681f0ef0', 'MpC3gsRq685ccebd',
                       'MpC3gsRq68f47d26', 'MpC3gsRq6918d469', 'MpC3gsRq69ac7b3a', 'MpC3gsRq6Ak25kLa',
                       'MpC3gsRq6a60f862', 'MpC3gsRq6a6c471b', 'MpC3gsRq6a79d719', 'MpC3gsRq6a7ac6bf',
                       'MpC3gsRq6aff1e80', 'MpC3gsRq6b6ff59d', 'MpC3gsRq6b9ce65d', 'MpC3gsRq6ba1c9aa',
                       'MpC3gsRq6bc59850', 'MpC3gsRq6bdaabcd', 'MpC3gsRq6c3c34ce', 'MpC3gsRq6c8e92d2',
                       'MpC3gsRq6cb8fd3a', 'MpC3gsRq6cba8c2a', 'MpC3gsRq6cbf9928', 'MpC3gsRq6dad4db6',
                       'MpC3gsRq6e453d96', 'MpC3gsRq6ed92c12', 'MpC3gsRq6f862df3', 'MpC3gsRq6fdb06a3',
                       'MpC3gsRq6fe5029d', 'MpC3gsRq7020db72', 'MpC3gsRq7021d1f2', 'MpC3gsRq70404fc5',
                       'MpC3gsRq70927184', 'MpC3gsRq70d9486d', 'MpC3gsRq70e85b93', 'MpC3gsRq70f774a2',
                       'MpC3gsRq71094753', 'MpC3gsRq72795bb4', 'MpC3gsRq72bb18e5', 'MpC3gsRq734f32dd',
                       'MpC3gsRq7352497e', 'MpC3gsRq735b9105', 'MpC3gsRq73642db9', 'MpC3gsRq7396e191',
                       'MpC3gsRq73bc081e', 'MpC3gsRq73d43844', 'MpC3gsRq73ddc3ec', 'MpC3gsRq73e57482',
                       'MpC3gsRq73fddb71', 'MpC3gsRq741ede3b', 'MpC3gsRq744eeb69', 'MpC3gsRq746ec2b3',
                       'MpC3gsRq746f68f1', 'MpC3gsRq74bb661a', 'MpC3gsRq74f82ba0', 'MpC3gsRq750ecaee',
                       'MpC3gsRq751ea44d', 'MpC3gsRq761eaf5a', 'MpC3gsRq763f9b91', 'MpC3gsRq764a46dc',
                       'MpC3gsRq76563c9d', 'MpC3gsRq76b9c305', 'MpC3gsRq76d53320', 'MpC3gsRq76ef9203',
                       'MpC3gsRq772eb981', 'MpC3gsRq77ae4355', 'MpC3gsRq77fadb64', 'MpC3gsRq7804d5f0',
                       'MpC3gsRq79902512', 'MpC3gsRq7a0574c1', 'MpC3gsRq7a17bcb2', 'MpC3gsRq7a93ef7c',
                       'MpC3gsRq7b36fdf6', 'MpC3gsRq7b712fd1', 'MpC3gsRq7baae941', 'MpC3gsRq7bbbd6ff',
                       'MpC3gsRq7bdf90a3', 'MpC3gsRq7cc394b5', 'MpC3gsRq7d2c4608', 'MpC3gsRq7db25089',
                       'MpC3gsRq7e3e9902', 'MpC3gsRq7e86e1df', 'MpC3gsRq7fe671ee', 'MpC3gsRq8033cad3',
                       'MpC3gsRq80b85fd7', 'MpC3gsRq81a76bc0', 'MpC3gsRq81ee3b78', 'MpC3gsRq81f76b68',
                       'MpC3gsRq82767d53', 'MpC3gsRq82c22e6d', 'MpC3gsRq82d3683e', 'MpC3gsRq82e0ba78',
                       'MpC3gsRq82f94d67', 'MpC3gsRq83889649', 'MpC3gsRq83fc750c', 'MpC3gsRq843b7ce0',
                       'MpC3gsRq8550fa08', 'MpC3gsRq855a8a33', 'MpC3gsRq85923f72', 'MpC3gsRq85e3045a',
                       'MpC3gsRq85e70e7e', 'MpC3gsRq85f098d9', 'MpC3gsRq866d8fd4', 'MpC3gsRq8683bf2c',
                       'MpC3gsRq86dd15c2', 'MpC3gsRq8728c278', 'MpC3gsRq8743749e', 'MpC3gsRq877b6a5d',
                       'MpC3gsRq87cd343d', 'MpC3gsRq880428e1', 'MpC3gsRq8833a1cc', 'MpC3gsRq8912b4fe'
                       ]}}

if __name__ == '__main__':
    i = 0
    while True:
        response = requests.post(
            'https://memory.k3s-dev.myones.net/project/api/project/team/WA7zYRTi/items/graphql',
            params=params,
            cookies=cookies,
            headers=headers,
            json=json_data,
            # proxies=proxies,
        )
        print(response.status_code, i)
        print(response.text)
        i += 1
        if i > 1520:
            break
        # time.sleep(0.1)
