from collections import defaultdict


# 示例数据代替数据库读取
def fetch_dependencies():
    # 返回示例数据，格式为 [(task_id, dependent_task_id), ...]
    return [
        ('A', 'B'),
        ('B', 'C'),
        ('C', 'A'),  # 形成 A -> B -> C -> A 的环
        ('D', 'E'),  # D -> E 不存在环
        ('E', 'D'),  # D -> E 不存在环
    ]


# 使用 DFS 构建子图
def build_graph(dependencies):
    graph = defaultdict(list)
    for task_id, dependent_task_id in dependencies:
        graph[task_id].append(dependent_task_id)
    return graph


# 查找所有连通子图
def find_connected_components(graph):
    visited = set()
    components = []

    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)

    for node in list(graph.keys()):
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)

    return components


# 检查是否存在环，并找出成环的节点及其方向
def find_cycles_in_component(graph, component):
    visited = set()
    rec_stack = []
    cycle_paths = []

    def dfs(node):
        if node in rec_stack:
            # 找到环，构建环路径
            cycle_start_index = rec_stack.index(node)
            cycle = rec_stack[cycle_start_index:]  # 环的节点序列
            cycle_edges = [(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)]  # 环的边
            cycle_edges.append((cycle[-1], cycle[0]))  # 补上最后一条边形成环
            cycle_paths.append(cycle_edges)
            return True
        if node in visited:
            return False

        visited.add(node)
        rec_stack.append(node)

        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True

        rec_stack.pop()
        return False

    for node in component:
        if node not in visited:
            if dfs(node):
                break  # 只要找到一个环就可以停止

    return cycle_paths


# 主逻辑
dependencies = fetch_dependencies()
graph = build_graph(dependencies)
components = find_connected_components(graph)

all_cycles = []

for component in components:
    cycle_paths = find_cycles_in_component(graph, component)
    if cycle_paths:
        all_cycles.extend(cycle_paths)

if all_cycles:
    print("存在环")
    for cycle in all_cycles:
        print("环路径：")
        for edge in cycle:
            print(f"{edge[0]} -> {edge[1]}")
else:
    print("无环")
