import networkx as nx

def compute_arrival_times(G):
    arrival = {}

    # Topological order
    for node in nx.topological_sort(G):

        preds = list(G.predecessors(node))

        if not preds:
            arrival[node] = 0
        else:
            max_arrival = 0

            for p in preds:
                edge_delay = G[p][node].get("weight", 1)
                candidate = arrival[p] + edge_delay

                if candidate > max_arrival:
                    max_arrival = candidate

            arrival[node] = max_arrival

    return arrival

def compute_slack(arrival, clock_period):
    slack = {}

    for node, arr_time in arrival.items():
        slack[node] = clock_period - arr_time

    return slack

def detect_violations(slack):
    violations = {}

    for node, s in slack.items():
        if s < 0:
            violations[node] = s

    return violations