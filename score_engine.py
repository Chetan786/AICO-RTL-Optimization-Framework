def compute_score(
    original_delay,
    new_delay,
    reg_count,
    logic_nodes
):

    delay_gain = original_delay - new_delay

    # Weighted objective
    score = (
        (delay_gain * 10)
        - (reg_count * 2)
        - (logic_nodes * 0.5)
    )

    return score

def count_registers(lines):
    regs = set()

    for line in lines:
        stripped = line.strip()

        # Only count real reg declarations
        if stripped.startswith("reg "):

            # Extract register name
            parts = stripped.replace(";", "").split()

            if len(parts) >= 2:
                reg_name = parts[1]
                regs.add(reg_name)

    return len(regs)

def count_logic_nodes(G):
    return len(G.nodes())

def placement_quality(path, candidate):
    """
    Higher score if candidate is near center of path
    """

    if candidate not in path:
        return 0

    center = len(path) / 2
    idx = path.index(candidate)

    distance = abs(center - idx)

    return max(0, 5 - distance)