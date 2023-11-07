import re


def find_package_function_calls(go_code, package_name):
    function_calls = []
    constant_references = []

    pattern = r'{}\.\w+\(?'.format(package_name)
    matches = re.findall(pattern, go_code)

    for match in matches:
        if re.search(r'\($', match):
            # 去掉最后一个字符
            match = match[:-1]
            function_calls.append(match)
        else:
            constant_references.append(match)

    # 去重
    function_calls = list(set(function_calls))
    constant_references = list(set(constant_references))
    return function_calls, constant_references


if __name__ == '__main__':
    go_code = """
    if !utils.IsLenValidUTF8(o.Value, utilsModel.FieldOptionValueMaxLen) {
        f.UUID = utils.UUID()
    }
    var x = utils.Constant
    """

    package_name = 'utils'
    function_calls, constant_references = find_package_function_calls(go_code, package_name)

    print("Function Calls:")
    print(function_calls)

    print("Constant References:")
    print(constant_references)
