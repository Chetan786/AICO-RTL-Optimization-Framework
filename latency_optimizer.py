def choose_pipeline_point(path, G):
    """
    Choose pipeline split point based on balanced delay.
    """

    # Edge delays along path
    delays = []

    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]

        weight = G[u][v].get("weight", 1)
        delays.append(weight)

    total_delay = sum(delays)

    best_split = None
    best_balance = float("inf")

    running_delay = 0

    for i in range(len(delays)):
        running_delay += delays[i]

        stage1 = running_delay
        stage2 = total_delay - running_delay

        balance = abs(stage1 - stage2)

        if balance < best_balance:
            best_balance = balance
            best_split = path[i + 1]

    return best_split