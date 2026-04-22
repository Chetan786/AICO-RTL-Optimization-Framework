import networkx as nx
import matplotlib.pyplot as plt

# Delay model
GATE_DELAY = {
    "&": 1,
    "|": 1,
    "^": 1
}

def extract_dependencies(expr):
    tokens = expr.replace("(", "").replace(")", "").split()
    return tokens


def build_graph(assignments):
    G = nx.DiGraph()

    for left, right, signals in assignments:
        for sig in signals:
            if sig != left:
                G.add_edge(sig, left, weight=1)

    return G


def find_critical_path(G):
    try:
        path = nx.dag_longest_path(G, weight='weight')
        delay = nx.dag_longest_path_length(G, weight='weight')
        return path, delay
    except:
        return [], 0


# 🔥 ADD THIS (don’t replace anything above)
def visualize_graph(G, critical_path):
    pos = nx.spring_layout(G)   # 🔥 FIX: automatic layout

    edge_colors = []

# Build actual path edges
    path_edges = list(zip(critical_path, critical_path[1:]))

    for u, v in G.edges():
        if (u, v) in path_edges:
            edge_colors.append('red')  # true critical edge
        else:
            edge_colors.append('black')

    nx.draw(G, pos,
            with_labels=True,
            edge_color=edge_colors,
            node_color='lightblue',
            node_size=2000,
            font_size=10)

    plt.title("Circuit Graph (Red = Critical Path)")
    plt.show()


def detect_patterns(G):
    patterns = []

    # Detect nodes with high fan-in
    for node in G.nodes():
        in_degree = G.in_degree(node)
        if in_degree > 2:
            patterns.append(f"⚠️ High fan-in detected at '{node}' ({in_degree} inputs)")

    # Detect long chains (depth)
    longest_path = nx.dag_longest_path(G)
    if len(longest_path) > 3:
        patterns.append(f"⚠️ Deep logic chain detected: {' -> '.join(longest_path)}")

    return patterns