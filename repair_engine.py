from latency_optimizer import choose_pipeline_point

def auto_repair(path, G, slack):
    worst_node = None
    worst_slack = 999

    for node, s in slack.items():
        if s < worst_slack:
            worst_slack = s
            worst_node = node

    if worst_slack < 0:
        pipeline_point = choose_pipeline_point(path, G)
        return pipeline_point

    return None