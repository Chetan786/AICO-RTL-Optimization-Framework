import tempfile
import os

from parser import parse_verilog, extract_assignments
from delay_analyzer import build_graph, find_critical_path
from sta_engine import compute_arrival_times, compute_slack
from repair_engine import auto_repair
from self_heal import run_self_heal


def timing_closure_loop(lines, clock_period=2, max_iterations=5):

    current_lines = lines

    for iteration in range(max_iterations):

        # ----------------------------
        # Write temporary RTL file
        # ----------------------------
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".v",
            mode="w"
        )

        temp_file.writelines(current_lines)
        temp_file.close()

        # ----------------------------
        # Parse repaired RTL
        # ----------------------------
        ast = parse_verilog(temp_file.name)
        assigns = extract_assignments(ast)

        G = build_graph(assigns)

        path, delay = find_critical_path(G)

        arrival = compute_arrival_times(G)
        slack = compute_slack(arrival, clock_period)

        worst_slack = min(slack.values())

        print(f"\nIteration {iteration+1}")
        print(f"Worst Slack = {worst_slack}")

        # ----------------------------
        # Stop if timing closed
        # ----------------------------
        if worst_slack >= 0:
            print("✅ Timing closure achieved")
            os.unlink(temp_file.name)
            return current_lines

        # ----------------------------
        # Repair again
        # ----------------------------
        repair_point = auto_repair(path, G, slack)

        print(f"🔧 Repairing at {repair_point}")

        current_lines = run_self_heal(current_lines, repair_point)

        os.unlink(temp_file.name)

    return current_lines