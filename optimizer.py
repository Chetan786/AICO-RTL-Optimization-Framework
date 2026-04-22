import networkx as nx

def generate_suggestions(path, delay, threshold=2):
    suggestions = []

    if delay > threshold:
        suggestions.append("⚠️ Critical path is too long")

        # Better pipeline suggestion (earlier split)
        if len(path) > 2:
            pipeline_point = path[len(path)//2 - 1]
        else:
            pipeline_point = path[0]

        suggestions.append(
            f"💡 Insert pipeline register after '{pipeline_point}' to reduce logic depth"
        )

        # More meaningful explanation
        suggestions.append(
            f"📉 This can reduce critical path delay from {delay} to ~{delay//2 + 1}"
        )

        # Parallelization suggestion
        suggestions.append(
            "💡 Consider restructuring logic to enable parallel execution"
        )

    else:
        suggestions.append("✅ Timing is within acceptable range")

    return suggestions

def detect_patterns(G):
    patterns = []

    for node in G.nodes():
        in_degree = G.in_degree(node)
        if in_degree > 2:
            patterns.append(f"⚠️ High fan-in detected at '{node}' ({in_degree} inputs)")

    longest_path = nx.dag_longest_path(G)
    if len(longest_path) > 3:
        patterns.append(f"⚠️ Deep logic chain detected: {' -> '.join(longest_path)}")

    return patterns