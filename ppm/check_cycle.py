import matplotlib.pyplot as plt
import networkx as nx

def find_cycle(graph):
    """
    使用深度优先搜索（DFS）检测有向图中的环并返回环的节点列表。
    """
    visited = set()       # 存储已经访问过的节点
    stack = set()         # 当前路径上的节点（用于检测环）
    parent = {}           # 记录每个节点的父节点，用于回溯找到环

    def dfs(node):
        visited.add(node)
        stack.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:  # 如果邻居未访问，递归进行DFS
                parent[neighbor] = node
                cycle = dfs(neighbor)
                if cycle:
                    return cycle
            elif neighbor in stack:  # 如果邻居在当前路径中，说明发现环
                cycle = []
                current = node
                while current != neighbor:  # 回溯找出环的节点
                    cycle.append(current)
                    current = parent[current]
                cycle.append(neighbor)
                cycle.append(node)  # 环的最后一个节点和起始节点相同
                return cycle

        stack.remove(node)
        return None

    for node in graph:
        if node not in visited:
            cycle = dfs(node)
            if cycle:
                return cycle
    return None

def draw_graph_with_cycle(graph, cycle=None, file_name="graph.png"):
    """
    绘制有向图，并将环的部分标红。图像将保存为文件。
    """
    pos = nx.spring_layout(graph)  # 布局

    # 绘制节点和非环的边
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='black',
            node_size=2000, font_size=16, font_color='black')

    if cycle:
        # 标记环的边为红色
        red_edges = [(cycle[i], cycle[i+1]) for i in range(len(cycle)-1)]
        nx.draw_networkx_edges(graph, pos, edgelist=red_edges, edge_color='red', width=2)

    # 保存图像到文件
    plt.savefig(file_name)
    print(f"Graph image saved as {file_name}")

if __name__ == "__main__":
    # 创建有向图
    G = nx.DiGraph()

    # 添加节点和边
    edges = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'B'),  # 环: B -> C -> D -> B
        ('C', 'E'), ('E', 'F')
    ]
    G.add_edges_from(edges)

    # 查找图中的环
    cycle = find_cycle(G)

    if cycle:
        print(f"Graph has a cycle: {cycle}")
    else:
        print("Graph has no cycle.")

    # 绘制图并将环部分标红，保存为文件
    draw_graph_with_cycle(G, cycle, file_name="graph_with_cycle.png")
