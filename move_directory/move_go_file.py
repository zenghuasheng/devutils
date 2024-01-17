import argparse
import os
import re
import subprocess
import sys
import json


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Script to move go file or directory.")
    parser.add_argument("source", help="source path, like app/services/common/get.go "
                                       "or app/services/common/organization")
    parser.add_argument("target", help="target path, like biz-common/get.go or biz-common/organization")
    parser.add_argument("--main-dir", help="directory path of bang-api", required=False,
                        default='/Users/xhs/go/src/github.com/bangwork/bang-api-gomod')
    parser.add_argument("--go-path", help="go path", required=False, default='/Users/xhs/go1.17/go1.20.1/bin/go')
    parser.add_argument("--symbol-bin-path", help="the symbol bin file path to extract go symbols, "
                                                  "the result of compile get_export_symbol.go", required=False,
                        default='/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/tmp/extract_symbol')
    parser.add_argument("--force", help="force move, skip check", required=False, default=False, action='store_true')
    parser.add_argument("--debug", help="debug mode", required=False, default=False, action='store_true')
    parser.add_argument("--no-compile", help="no need to compile", required=False, default=False, action='store_true')
    args = parser.parse_args()

    return args


def move_dir(main_dir, go_path, source, target, no_compile=False):
    os.chdir(main_dir)
    print(f'Moving {source} to {target}')
    target_file = os.path.join(main_dir, target)
    # 判断 source 是否存在
    if not os.path.exists(os.path.join(main_dir, source)):
        print(f'Package "{source}" not exists')
        return

    # 判断 go_path 是否存在
    if not os.path.exists(go_path):
        print(f'go_path "{go_path}" not exists')
        exit(1)

    # 创建父级目录
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    # 移动子目录
    move_command = " ".join(['mv', os.path.join(main_dir, source), os.path.dirname(target_file)])
    print(move_command)
    move_result = subprocess.run(move_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if move_result.returncode != 0:
        print(f'Move failed, Please check the modifications.')
        exit(1)

    # 替换 import
    # find /Users/xhs/go/src/github.com/bangwork/bang-api-gomod/app/services/common/organization -type f -name '*.go' -exec sed -i '' 's|"github\.com/bangwork/bang-api/app/models/user"|"github\.com/bangwork/bang-api/biz-common/user/models/user"|g' {} +
    replace_commands = [
        f"find {main_dir} -type f -name '*.go' -exec sed -i '' 's|\"github\.com/bangwork/bang-api/{source}\"|\"github\.com/bangwork/bang-api/{target}\"|g' {{}} +",
        f"find {main_dir} -type f -name '*.go' -exec sed -i '' 's|\"github\.com/bangwork/bang-api/{source}/|\"github\.com/bangwork/bang-api/{target}/|g' {{}} +",
    ]
    for replace_command in replace_commands:
        print(replace_command)
        subprocess.run(replace_command, shell=True)

    if no_compile:
        # 构建成功，自动提交修改
        git_commit_command = f'git add . && git commit -m "move {source} to {target}"'
        commit_result = subprocess.run(git_commit_command, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        if commit_result.returncode != 0 and "nothing to commit, working tree clean" not in commit_result.stdout.decode(
                "utf-8"):
            print(f'Commit failed, Please check the modifications.')
            exit(1)
    else:
        # 执行构建命令
        build_command = f'{go_path} build  -o /tmp/'
        build_result = subprocess.run(build_command, shell=True, check=False)

        # 检查构建结果
        if build_result.returncode == 0:
            # 构建成功，自动提交修改
            git_commit_command = f'git add . && git commit -m "move {source} to {target}"'
            commit_result = subprocess.run(git_commit_command, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
            if commit_result.returncode != 0 and "nothing to commit, working tree clean" not in commit_result.stdout.decode(
                    "utf-8"):
                print(f'Commit failed, Please check the modifications.')
                exit(1)
        else:
            print(f'Build failed, Please check the modifications.')
            exit(1)


def find_package_symbols(go_code, package_name):
    function_calls = []
    other_symbols = []

    # 前面加一个空格，防止匹配到别的包
    pattern = r'{}\.\w+\(?'.format(package_name)
    matches = re.findall(pattern, go_code)

    for match in matches:
        match = match.strip()
        parts = match.split('.')
        if len(parts) != 2:
            continue
        if parts[0] != package_name:
            continue
        if re.search(r'\($', match):
            # 去掉最后一个字符
            match = match[:-1]
            function_calls.append(match)
        else:
            other_symbols.append(match)

    # 去重
    function_calls = list(set(function_calls))
    other_symbols = list(set(other_symbols))
    return function_calls, other_symbols


def get_file_imported_packages(go_code):
    imported_packages = []
    import_match = re.findall(r'import\s+\((.*?)\)', go_code, re.DOTALL)
    if import_match:
        import_block = import_match[0]
        pattern = r'(([a-zA-Z0-9]+\s+)?"[^"]+")'
        import_lines = re.findall(pattern, import_block)
        for match in import_lines:
            if not match:
                continue
            package = match[0]
            # 'jsonUtils "github.com/bangwork/bang-api/app/utils/json"'
            # 先按空格分割，如果不包含空格，说明没有别名
            packages = package.split(" ")
            if len(packages) == 2:
                alias = packages[0]
                package = packages[1]
            else:
                alias = None
                package = packages[0]
            package = package.strip('"')
            # 包含 bangwork 才是我们需要的包
            if "bangwork" in package:
                # if not alias:
                # alias = package.split("/")[-1].replace('"', '')
                imported_packages.append({
                    "package": package,
                    "alias": alias
                })
    return imported_packages


def search_name(imported_packages, source_package_path):
    if not imported_packages:
        return None
    for imported_package in imported_packages:
        package = imported_package['package']
        alias = imported_package['alias']
        if package == f'github.com/bangwork/bang-api/{source_package_path}':
            # 如果别名为空，使用包名
            if not alias:
                alias = package.split("/")[-1].replace('"', '')
            return alias
    return None


def add_import(content, package_name):
    # 正则表达式匹配 import() 语句
    import_pattern = r'\bimport\s*\(\s*([^)]+)\s*\)\s*'

    # 查找 import() 语句
    import_match = re.search(import_pattern, content)

    if import_match:
        existing_imports = import_match.group(1)

        # 检查 package_name 是否已存在
        if package_name in existing_imports:
            print(f'Package "{package_name}" already exists')
            return

        # 在 import() 语句中添加新的包
        modified_imports = f'{existing_imports}\n\t{package_name}'

        # 检查是否有其他函数或代码紧随在 import() 语句后面
        after_import = content[import_match.end():]
        match_after_import = re.search(r'^\s*\)', after_import)
        if match_after_import:
            modified_content = content[
                               :import_match.start()] + f'import (\n\t{modified_imports}\n)\n\n{after_import[match_after_import.end():]}'
        else:
            modified_content = content[:import_match.start()] + f'import (\n\t{modified_imports}\n)\n{after_import}'
        return modified_content
    else:
        return content


class Symbol:
    name = None
    kind = None
    origin_line = None

    def __init__(self, name, kind, origin_line):
        self.name = name
        self.kind = kind
        self.origin_line = origin_line


def is_go_file(file_name):
    return file_name.endswith('.go')


def include_symbol(symbol_name, go_code):
    # 查找是否含有某个 symbol
    pattern = re.compile(r'\b' + re.escape(symbol_name) + r'\b')
    match_lines = []
    for i, line in enumerate(go_code.split('\n'), start=1):
        if re.search(pattern, line):
            match_lines.append(line)
    if len(match_lines) == 0:
        return False
    # 看是否是别的包的同名 symbol，使用 .symbol_name 来搜索
    this_package_lines = []
    for line in match_lines:
        if re.search(r'\.' + re.escape(symbol_name) + r'\b', line):
            continue
        this_package_lines.append(line)
    if len(this_package_lines) == 0:
        return False
    return True


class MoveGo:
    source = None
    target = None
    main_dir = None
    go_path = None
    symbol_bin_path = None
    source_package_path = None
    target_package_path = None
    package_exported_symbol_names = []
    package_unexported_symbol_names = []
    file_exported_symbol_names = []
    file_unexported_symbol_names = []
    imported_files = []
    debug = False

    def __init__(self, main_dir, go_path, symbol_bin_path, source, target, debug=False):
        self.main_dir = main_dir
        self.go_path = go_path
        self.symbol_bin_path = symbol_bin_path
        self.source = source
        self.target = target
        self.debug = debug

    def extract_go_info(self):
        self.source_package_path = os.path.dirname(self.source)
        print(f'package path: {self.source_package_path}')
        self.target_package_path = os.path.dirname(self.target)
        self.package_exported_symbol_names, self.package_unexported_symbol_names = self.extract_symbols(
            include_package=True)
        self.file_exported_symbol_names, self.file_unexported_symbol_names = self.extract_symbols()

    def extract_symbols(self, include_package=False):
        # 提取所有暴露的 symbol
        os.chdir(self.main_dir)
        current_env = os.environ.copy()
        cmd_list = [self.symbol_bin_path, os.path.join(self.main_dir, self.source)]
        if include_package:
            cmd_list.append('all')
        cmd = " ".join(cmd_list)
        if self.debug:
            print(cmd)
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                cwd=self.main_dir, env=current_env)
        if result.returncode != 0:
            raise Exception(f'extract symbol failed: {result.stderr.decode("utf-8")}')
        doc = result.stdout.decode('utf-8')
        # {"exported":[{"name":"ConfigActionAdd","kind":"const"},{"name":"ConfigActionUpdate","kind":"const"},{"name":"ConfigActionDelete","kind":"const"},{"name":"App","kind":"type"},{"name":"AppstoreConfig","kind":"type"},{"name":"TeamPluginConfig","kind":"type"},{"name":"NewTeamPluginConfig","kind":"func"}],"unexported":[{"name":"newAppstoreConfig","kind":"func"},{"name":"changeAppStoreConfig","kind":"func"},{"name":"addConfig","kind":"func"},{"name":"updateConfig","kind":"func"},{"name":"deleteConfig","kind":"func"}]}
        # 返回是 json
        symbols = []
        if not doc:
            return symbols
        symbols = json.loads(doc)
        return [s['name'] for s in symbols['exported']], [s['name'] for s in symbols['unexported']]

    def search_imported_files(self):
        # 搜索所有文件，找到所有 import 了 package 的文件，可能有别名，设为文件 A
        # grep -r "github\.com/bangwork/bang-api/app/models" --include='*.go' /Users/xhs/go/src/github.com/bangwork/bang-api-gomod | cut -d ':' -f 1 | more
        cmd = f'grep -r "\\"github\.com/bangwork/bang-api/{self.source_package_path}\\"" --include="*.go" {self.main_dir} | cut -d ":" -f 1'
        if self.debug:
            print(cmd)
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(f'grep failed: {result.stderr.decode("utf-8")}')
        self.imported_files = result.stdout.decode('utf-8').split('\n')
        # 去掉空行
        self.imported_files = list(filter(None, self.imported_files))

    def replace(self):
        # 此文件用了包的导出的、未导出的 symbols
        self.source_use_package_symbols()
        # 包的其他文件用了此文件的导出的、未导出的 symbols
        self.source_package_use_file_symbol()

        # 读取文件 A 内容，列出所有 package 的函数，常量
        # self.imported_files = ['/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/app/services/manhour/message.go']
        for file_path in self.imported_files:
            if self.debug:
                print(f'processing {file_path}')
            with open(file_path, 'r+') as f:
                go_code = f.read()
                # 如果 imported_packages 不为空，排序
                imported_packages = get_file_imported_packages(go_code)
                name = search_name(imported_packages, self.source_package_path)
                if not name:
                    raise Exception(f'package {self.source_package_path} not found in {f}')
                # 列出所有 package 的函数，常量
                function_calls, other_symbols = find_package_symbols(go_code, name)
                file_symbols = []
                for s in function_calls + other_symbols:
                    file_symbols.append(s.split('.')[1])
                if len(file_symbols) == 0:
                    raise Exception(f'package {self.source_package_path} not found in {f}')
                # 取 package_symbol_names 和 file_symbols 的交集
                file_symbols = list(set(file_symbols).intersection(set(self.package_exported_symbol_names)))
                if self.debug:
                    print(f'file symbols: {file_symbols}')
                # 判断要替换的函数和常量是否都包含于原始文件里，如果是，替换包名，如果不是，加一个别名，比如 xxx2，插入一行 import
                # 判断 file_symbols 是否都包含于 symbol_names

                # 将文件指针移动回文件开头
                f.seek(0)

                if set(file_symbols).issubset(set(self.file_exported_symbol_names)):
                    # 替换 import 就行
                    go_code = go_code.replace(f'"github.com/bangwork/bang-api/{self.source_package_path}"',
                                              f'"github.com/bangwork/bang-api/{self.target_package_path}"')
                    f.write(go_code)
                else:
                    have_symbol = False
                    for s in self.file_exported_symbol_names:
                        if re.search(r'\b' + re.escape(f'{name}.{s}') + r'\b', go_code):
                            have_symbol = True
                            break
                    if not have_symbol:
                        continue
                    # 加一个别名，比如 xxx2，插入一行 import
                    go_code = add_import(go_code, f'{name}2 "github.com/bangwork/bang-api/{self.target_package_path}"')
                    # 替换
                    for s in self.file_exported_symbol_names:
                        go_code = re.sub(r'\b' + re.escape(f'{name}.{s}') + r'\b', f'{name}2.{s}', go_code)
                    f.write(go_code)
                # 截断文件，删除多余的内容（如果新内容比旧内容短）
                f.truncate()

        # 移动文件
        # 取 target 的父目录，如果不存在，创建
        target_dir = os.path.dirname(self.target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
        mv_cmd = f'mv {self.source} {self.target}'
        if self.debug:
            print(mv_cmd)
        result = subprocess.run(mv_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.main_dir)
        if result.returncode != 0:
            raise Exception(f'mv failed: {result.stderr.decode("utf-8")}')
        # 编译
        self.build_commit(f'move {self.source} to {self.target}')

    def build_commit(self, commit_message):
        # 执行构建命令
        if not os.path.exists(self.go_path):
            raise Exception(f'go_path "{self.go_path}" not exists')
        build_command = f'{self.go_path} build  -o /tmp/'
        build_result = subprocess.run(build_command, shell=True, check=False)

        # 检查构建结果
        if build_result.returncode == 0:
            # 构建成功，自动提交修改
            git_commit_command = f'git add . && git commit -m "{commit_message}"'
            commit_result = subprocess.run(git_commit_command, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
            if commit_result.returncode != 0 and \
                    "nothing to commit, working tree clean" not in commit_result.stdout.decode("utf-8"):
                print(f'Commit failed, Please check the modifications.')
                raise Exception(f'Commit failed: {commit_result.stderr.decode("utf-8")}')
        else:
            raise Exception(f'Build failed, Please check the modifications.')

    def source_package_use_file_exported_symbol(self):
        for root, dirs, files in os.walk(os.path.join(self.main_dir, self.source_package_path)):
            for file in files:
                # 是否是 .go 文件
                if not is_go_file(file):
                    continue
                # 如果是 source，跳过
                if file == os.path.basename(self.source):
                    continue
                file_path = os.path.join(root, file)
                with open(file_path, 'r+') as f:
                    go_code = f.read()
                    # 查找是否含有某个 symbol
                    have_symbol = False
                    for s in self.file_exported_symbol_names:
                        if re.search(r'\b' + re.escape(s) + r'\b', go_code):
                            have_symbol = True
                            break
                    if not have_symbol:
                        continue
                    # 将文件指针移动回文件开头
                    f.seek(0)
                    go_code = add_import(go_code, f'"github.com/bangwork/bang-api/{self.target_package_path}"')
                    # 从 self.target_package_path 提取 package name
                    package_name = self.target_package_path.split('/')[-1]
                    # 替换
                    for s in self.file_exported_symbol_names:
                        go_code = re.sub(r'\b' + re.escape(s) + r'\b', f'{package_name}.{s}', go_code)
                    f.write(go_code)
                    # 截断文件，删除多余的内容（如果新内容比旧内容短）
                    f.truncate()
            break

    def source_use_package_symbols(self):
        with open(os.path.join(self.main_dir, self.source), 'r') as f:
            go_code = f.read()
            # self.package_symbol_names - self.file_symbol_names
            # 求差集
            exported_diff = list(
                set(self.package_exported_symbol_names).difference(set(self.file_exported_symbol_names)))
            unexported_diff = list(
                set(self.package_unexported_symbol_names).difference(set(self.file_unexported_symbol_names)))
            # 查找是否含有某个 symbol
            used_symbols = []
            for s in exported_diff + unexported_diff:
                if include_symbol(s, go_code):
                    used_symbols.append(s)
            if len(used_symbols) > 0:
                used_symbols_str = '\n'.join(used_symbols)
                raise Exception(f'{self.source} use these symbols in package '
                                f'{self.source_package_path}, you must move them to {self.source} first: \n'
                                f'{used_symbols_str}')

    def source_package_use_file_symbol(self):
        for root, dirs, files in os.walk(os.path.join(self.main_dir, self.source_package_path)):
            errors = []
            for file in files:
                # 是否是 .go 文件
                if not is_go_file(file):
                    continue
                # 如果是 source，跳过
                if file == os.path.basename(self.source):
                    continue
                file_path = os.path.join(root, file)
                with open(file_path, 'r+') as f:
                    go_code = f.read()
                    # 查找是否含有某个 symbol
                    symbols = []
                    for s in self.file_unexported_symbol_names + self.file_exported_symbol_names:
                        if include_symbol(s, go_code):
                            symbols.append(s)
                    if len(symbols) == 0:
                        continue
                    symbol_str = '\n'.join(symbols)
                    errors.append(f'{file} use these symbols in {os.path.basename(self.source)}, '
                                  f'you must change it first: \n'
                                  f'{symbol_str}')
            if len(errors) > 0:
                error_str = '\n'.join(errors)
                raise Exception(error_str)
            break
        pass


class MoveGoFiles:
    sources = []
    target = None
    main_dir = None
    go_path = None
    symbol_bin_path = None
    source_package_path = None
    target_package_path = None
    package_exported_symbol_names = []
    package_unexported_symbol_names = []
    file_exported_symbol_names = []
    file_unexported_symbol_names = []
    imported_files = []
    debug = False
    force = False
    have_error = False

    def __init__(self, main_dir, go_path, symbol_bin_path, sources, target, debug=False, force=False):
        self.main_dir = main_dir
        self.go_path = go_path
        self.symbol_bin_path = symbol_bin_path
        self.sources = sources
        self.target = target
        self.debug = debug
        self.force = force

    def extract_go_info(self):
        self.source_package_path = os.path.dirname(self.sources[0])
        print(f'package path: {self.source_package_path}')
        self.target_package_path = self.target
        self.package_exported_symbol_names, self.package_unexported_symbol_names = self.extract_symbols(
            self.sources[0],
            include_package=True)
        for source in self.sources:
            exported, unexported = self.extract_symbols(source)
            # self.file_exported_symbol_names, self.file_unexported_symbol_names
            self.file_exported_symbol_names.extend(exported)
            self.file_unexported_symbol_names.extend(unexported)

    def extract_symbols(self, file_path, include_package=False):
        # 提取所有暴露的 symbol
        os.chdir(self.main_dir)
        current_env = os.environ.copy()
        cmd_list = [self.symbol_bin_path, os.path.join(self.main_dir, file_path)]
        if include_package:
            cmd_list.append('all')
        cmd = " ".join(cmd_list)
        if self.debug:
            print(cmd)
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                cwd=self.main_dir, env=current_env)
        if result.returncode != 0:
            raise Exception(f'extract symbol failed: {result.stderr.decode("utf-8")}')
        doc = result.stdout.decode('utf-8')
        # 返回是 json
        symbols = []
        if not doc:
            return symbols
        symbols = json.loads(doc)
        return [s['name'] for s in symbols['exported']], [s['name'] for s in symbols['unexported']]

    def search_imported_files(self):
        # 搜索所有文件，找到所有 import 了 package 的文件，可能有别名，设为文件 A
        # grep -r "github\.com/bangwork/bang-api/app/models" --include='*.go' /Users/xhs/go/src/github.com/bangwork/bang-api-gomod | cut -d ':' -f 1 | more
        cmd = f'grep -r "\\"github\.com/bangwork/bang-api/{self.source_package_path}\\"" --include="*.go" {self.main_dir} | cut -d ":" -f 1'
        if self.debug:
            print(cmd)
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(f'grep failed: {result.stderr.decode("utf-8")}')
        self.imported_files = result.stdout.decode('utf-8').split('\n')
        # 去掉空行
        self.imported_files = list(filter(None, self.imported_files))

    def replace(self):
        # 此文件用了包的导出的、未导出的 symbols
        self.source_use_package_symbols()
        # 包的其他文件用了此文件的导出的、未导出的 symbols
        self.source_package_use_file_symbol()

        if self.have_error and not self.force:
            return

        # 读取文件 A 内容，列出所有 package 的函数，常量
        # self.imported_files = ['/Users/xhs/go/src/github.com/bangwork/bang-api-gomod/project-api/task/models/workflow/types.go']
        for file_path in self.imported_files:
            if self.debug:
                print(f'processing {file_path}')
            with open(file_path, 'r+') as f:
                go_code = f.read()
                # 如果 imported_packages 不为空，排序
                imported_packages = get_file_imported_packages(go_code)
                if not imported_packages:
                    continue
                name = search_name(imported_packages, self.source_package_path)
                if not name:
                    raise Exception(f'package {self.source_package_path} not found in {f}')
                # 列出所有 package 的函数，常量
                function_calls, other_symbols = find_package_symbols(go_code, name)
                file_symbols = []
                for s in function_calls + other_symbols:
                    file_symbols.append(s.split('.')[1])
                if len(file_symbols) == 0:
                    raise Exception(f'package {self.source_package_path} not found in {f}')
                # 取 package_symbol_names 和 file_symbols 的交集
                file_symbols = list(set(file_symbols).intersection(set(self.package_exported_symbol_names)))
                if self.debug:
                    print(f'file symbols: {file_symbols}')
                # 判断要替换的函数和常量是否都包含于原始文件里，如果是，替换包名，如果不是，加一个别名，比如 xxx2，插入一行 import
                # 判断 file_symbols 是否都包含于 symbol_names

                # 将文件指针移动回文件开头
                f.seek(0)

                if set(file_symbols).issubset(set(self.file_exported_symbol_names)):
                    # 替换 import 就行
                    go_code = go_code.replace(f'"github.com/bangwork/bang-api/{self.source_package_path}"',
                                              f'"github.com/bangwork/bang-api/{self.target_package_path}"')
                    f.write(go_code)
                else:
                    have_symbol = False
                    for s in self.file_exported_symbol_names:
                        if re.search(r'\b' + re.escape(f'{name}.{s}') + r'\b', go_code):
                            have_symbol = True
                            break
                    if not have_symbol:
                        continue
                    # 加一个别名，比如 xxx2，插入一行 import
                    import_alias = f'{name}' + os.path.basename(self.target_package_path)
                    go_code = add_import(go_code,
                                         f'{import_alias} "github.com/bangwork/bang-api/{self.target_package_path}"')
                    # 替换
                    for s in self.file_exported_symbol_names:
                        go_code = re.sub(r'\b' + re.escape(f'{name}.{s}') + r'\b', f'{import_alias}.{s}', go_code)
                    f.write(go_code)
                # 截断文件，删除多余的内容（如果新内容比旧内容短）
                f.truncate()

        # 移动文件
        # 取 target 的父目录，如果不存在，创建
        if not os.path.exists(self.target):
            os.makedirs(self.target, exist_ok=True)
        for source in self.sources:
            source_name = os.path.basename(source)
            mv_cmd = f'mv {source} {os.path.join(self.target, source_name)}'
            if self.debug:
                print(mv_cmd)
            result = subprocess.run(mv_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    cwd=self.main_dir)
            if result.returncode != 0:
                raise Exception(f'mv failed: {result.stderr.decode("utf-8")}')
        # 编译
        source_name_str = ', '.join(self.sources)
        self.build_commit(f'move {source_name_str} to {self.target}')

    def build_commit(self, commit_message):
        # 执行构建命令
        if not os.path.exists(self.go_path):
            raise Exception(f'go_path "{self.go_path}" not exists')
        build_command = f'{self.go_path} build  -o /tmp/'
        build_result = subprocess.run(build_command, shell=True, check=False)

        # 检查构建结果
        if build_result.returncode == 0:
            # 构建成功，自动提交修改
            git_commit_command = f'git add . && git commit -m "{commit_message}"'
            commit_result = subprocess.run(git_commit_command, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
            if commit_result.returncode != 0 and \
                    "nothing to commit, working tree clean" not in commit_result.stdout.decode("utf-8"):
                print(f'Commit failed, Please check the modifications.')
                raise Exception(f'Commit failed: {commit_result.stderr.decode("utf-8")}')
        else:
            raise Exception(f'Build failed, Please check the modifications.')

    def source_package_use_file_exported_symbol(self):
        source_names = [os.path.basename(source) for source in self.sources]
        for root, dirs, files in os.walk(os.path.join(self.main_dir, self.source_package_path)):
            for file in files:
                # 是否是 .go 文件
                if not is_go_file(file):
                    continue
                # 如果是 source，跳过
                if file in source_names:
                    continue
                file_path = os.path.join(root, file)
                with open(file_path, 'r+') as f:
                    go_code = f.read()
                    # 查找是否含有某个 symbol
                    have_symbol = False
            break

    def source_use_package_symbols(self):
        for source in self.sources:
            with open(os.path.join(self.main_dir, source), 'r') as f:
                go_code = f.read()
                # self.package_symbol_names - self.file_symbol_names
                # 求差集
                exported_diff = list(
                    set(self.package_exported_symbol_names).difference(set(self.file_exported_symbol_names)))
                unexported_diff = list(
                    set(self.package_unexported_symbol_names).difference(set(self.file_unexported_symbol_names)))
                # 查找是否含有某个 symbol
                used_symbols = []
                for s in exported_diff + unexported_diff:
                    if include_symbol(s, go_code):
                        used_symbols.append(s)
                if len(used_symbols) > 0:
                    self.have_error = True
                    used_symbols_str = '\n'.join(used_symbols)
                    print(
                        f'{source} use these symbols in package {self.source_package_path}, you must move them to '
                        f'{source} first: \n{used_symbols_str}')

    def source_package_use_file_symbol(self):
        for root, dirs, files in os.walk(os.path.join(self.main_dir, self.source_package_path)):
            errors = []
            source_names = [os.path.basename(source) for source in self.sources]
            for file in files:
                # 是否是 .go 文件
                if not is_go_file(file):
                    continue
                # 如果是 source，跳过
                if file in source_names:
                    continue
                file_path = os.path.join(root, file)
                with open(file_path, 'r+') as f:
                    go_code = f.read()
                    # 查找是否含有某个 symbol
                    symbols = []
                    for s in self.file_unexported_symbol_names + self.file_exported_symbol_names:
                        if include_symbol(s, go_code):
                            symbols.append(s)
                    if len(symbols) == 0:
                        continue
                    symbol_str = '\n'.join(symbols)
                    errors.append(f'{file} use these symbols in {source_names}, '
                                  f'you must change it first: \n'
                                  f'{symbol_str}')
            if len(errors) > 0:
                self.have_error = True
                error_str = '\n'.join(errors)
                print(error_str)
            break
        pass


if __name__ == '__main__':
    args = parse_command_line_args()
    # 判断一些目录是否存在
    if not os.path.exists(args.main_dir):
        print(f'main_dir "{args.main_dir}" not exists')
        sys.exit(1)
    if not os.path.exists(args.go_path):
        print(f'go_path "{args.go_path}" not exists')
        sys.exit(1)
    try:
        # 先判断 source, target 是否是 .go 文件
        if is_go_file(args.source):
            if not os.path.exists(args.symbol_bin_path):
                print(f'symbol_bin_path "{args.symbol_bin_path}" not exists')
                sys.exit(1)
            if is_go_file(args.target):
                print('move go file')
                move_go = MoveGo(args.main_dir, args.go_path, args.symbol_bin_path, args.source, args.target,
                                 args.debug)
                # 第一步：提取原始文件的 package 名称、对外暴露的方法、常量
                move_go.extract_go_info()
                # 第二步：搜索所有文件，找到所有 import 了 package 的文件，可能有别名，设为文件 A
                move_go.search_imported_files()
                move_go.replace()
            else:
                print('move go files')
                # 英文逗号分隔
                sources = args.source.split(',')
                move_go_files = MoveGoFiles(args.main_dir, args.go_path, args.symbol_bin_path, sources, args.target,
                                            args.debug, args.force)
                move_go_files.extract_go_info()
                move_go_files.search_imported_files()
                move_go_files.replace()
        else:
            print('move dir')
            move_dir(args.main_dir, args.go_path, args.source, args.target, args.no_compile)
    except Exception as e:
        print(f"Error:\n{e}")
        sys.exit(1)
