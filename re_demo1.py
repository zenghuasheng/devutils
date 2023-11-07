import re

text = 'containerModel "github.com/bangwork/bang-api/app/models/container"'
# text = '"github.com/bangwork/bang-api/app/models"'

pattern = r'(([a-zA-Z0-9]+\s+)?"[^"]+")'
match = re.search(pattern, text)

if match:
    matched_string = match.group(1)
    print(matched_string)
