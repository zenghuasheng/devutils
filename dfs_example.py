class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []


def has_cycle(graph):
    def dfs(node):
        if status[node] == 1:  # 如果当前节点正在被访问，说明存在环
            return True
        if status[node] == 2:  # 如果当前节点已经访问过，跳过
            return False

        # 标记当前节点正在访问中
        status[node] = 1
        for neighbor in graph[node].neighbors:
            if dfs(neighbor.name):
                return True

        # 标记当前节点已经访问完毕
        status[node] = 2
        return False

    # 初始化所有节点状态为 0：未访问
    status = {node: 0 for node in graph}

    # 对每个节点进行 DFS，如果检测到环，返回 True
    for node in graph:
        if status[node] == 0:  # 只对未访问的节点进行 DFS
            if dfs(node):
                return True

    return False


if __name__ == "__main__":
    # 创建节点
    node_a = Node('A')
    node_b = Node('B')
    node_c = Node('C')
    node_d = Node('D')
    node_e = Node('E')

    # 构建邻接关系
    node_a.neighbors = [node_b, node_d]
    node_b.neighbors = [node_c, node_d]
    node_d.neighbors = [node_e]
    node_e.neighbors = [node_b]

    # 构建图的字典表示
    graph = {
        'A': node_a,
        'B': node_b,
        'C': node_c,
        'D': node_d,
        'E': node_e
    }

    result = has_cycle(graph)
    print(result)