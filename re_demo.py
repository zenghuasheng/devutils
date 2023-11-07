import re

pattern = r'(([a-zA-Z0-9]+\s+)?"[^"]+")'
text = '''
"github.com/bangwork/bang-api/app/models"
containerModel "github.com/bangwork/bang-api/app/models/container"
'''

matches = re.findall(pattern, text)
for match in matches:
    if match[0]:
        print(match[0])