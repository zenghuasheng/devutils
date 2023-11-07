import sys

import json as base_json
import json5 as json
from jsoncomment import JsonComment

if len(sys.argv) != 2:
    print("need json file path")
    sys.exit(1)
file_path = sys.argv[1].strip()
with open(file_path, 'r') as file:
    parser = JsonComment(json)
    res = parser.loads(file.read())
    print(base_json.dumps(res, indent=4, ensure_ascii=False))
