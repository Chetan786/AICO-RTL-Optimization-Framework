import tempfile
import os
from score_engine import placement_quality
from parser import parse_verilog, extract_assignments
from delay_analyzer import build_graph, find_critical_path
from sta_engine import compute_arrival_times, compute_slack
from self_heal import run_self_heal
from score_engine import compute_score, count_registers, count_logic_nodes


def evaluate_candidates(
    lines,
    candidates,
    original_delay,
    clock_period=2
):

    results = []

    for candidate in candidates:

        # Apply repair
        modified_lines = run_self_heal(lines, candidate)

        # Write temp RTL
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".v",
            mode="w"
        )

        temp_file.writelines(modified_lines)
        temp_file.close()

        # Parse repaired RTL
        ast = parse_verilog(temp_file.name)
        assigns = extract_assignments(ast)

        G = build_graph(assigns)

        path, new_delay = find_critical_path(G)

        arrival = compute_arrival_times(G)
        slack = compute_slack(arrival, clock_period)

        worst_slack = min(slack.values())

        reg_count = count_registers(modified_lines)
        logic_nodes = count_logic_nodes(G)

        base_score = compute_score(
            original_delay,
            new_delay,
            reg_count,
            logic_nodes
        )

        placement_bonus = placement_quality(path, candidate)

        score = base_score + placement_bonus

        results.append((candidate, score, worst_slack))

        os.unlink(temp_file.name)

    return sorted(results, key=lambda x: x[1], reverse=True)