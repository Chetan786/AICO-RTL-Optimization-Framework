from parser import parse_verilog, extract_assignments
from delay_analyzer import build_graph, find_critical_path
from optimizer import generate_suggestions
from delay_analyzer import visualize_graph
from optimizer import detect_patterns
from rtl_modifier import insert_multi_pipeline
from latency_optimizer import choose_pipeline_point
from sta_engine import compute_arrival_times, compute_slack
from sta_engine import detect_violations
from repair_engine import auto_repair
from self_heal import run_self_heal
from timing_closure import timing_closure_loop
from score_engine import compute_score, count_registers
from score_engine import count_logic_nodes
from candidate_ranker import evaluate_candidates
from memory_engine import update_memory
from memory_engine import predict_best_repair
from confidence_engine import compute_confidence
from explain_engine import generate_explanation
from history_engine import save_history
from dashboard_engine import plot_history
import os

def main():
    file_path = os.path.join(os.getcwd(), "samples", "sample1.v")
    file_path = file_path.replace("\\", "/")

    print("FILE PATH =", file_path)
    ast = parse_verilog(file_path)
    assigns = extract_assignments(ast)

    print("\n=== ASSIGNMENTS DETECTED ===")
    for left, right, _ in assigns:
        print(f"{left} = {right}")

    # 🔥 IMPORTANT: define path and delay FIRST
    G = build_graph(assigns)
    path, delay = find_critical_path(G)

    print("\n=== CRITICAL PATH ===")
    print(" -> ".join(path))
    print(f"Total Delay: {delay}")

    # 🔥 NOW use them
    print("\n=== OPTIMIZATION SUGGESTIONS ===")
    suggestions = generate_suggestions(path, delay)

    for s in suggestions:
        print(s)

    print("\n=== PATTERN ANALYSIS ===")
    patterns = detect_patterns(G)

    for p in patterns:
        print(p)

    print("\n=== GRAPH EDGES ===")
    for u, v in G.edges():
        print(f"{u} -> {v}")

    visualize_graph(G, path)

    print("\n=== MODIFIED RTL ===")

    with open("samples/sample1.v", "r") as f:
        lines = f.readlines()
    
 

# Use your detected pipeline point
    best_point = choose_pipeline_point(path, G)
    pipeline_points = [best_point]


    best_point = choose_pipeline_point(path, G)
    pipeline_points = [best_point]

    modified_lines = insert_multi_pipeline(lines, pipeline_points)

    for line in modified_lines:
        print(line, end="")
    
    print("\n=== LATENCY-AWARE DECISION ===")
    print(f"Best pipeline point: {best_point}")

    print("\n=== ARRIVAL TIMES ===")

    arrival = compute_arrival_times(G)

    for node, t in arrival.items():
        print(f"{node}: {t}")

    print("\n=== SLACK REPORT ===")

    clock_period = 2

    slack = compute_slack(arrival, clock_period)

    for node, s in slack.items():
        print(f"{node}: Slack = {s}")

    print("\n=== TIMING VIOLATIONS ===")

    violations = detect_violations(slack)

    if violations:
        for node, s in violations.items():
            print(f"❌ {node}: Negative Slack = {s}")
    else:
        print("✅ No timing violations detected")

    print("\n=== AUTO REPAIR ENGINE ===")

    repair_point = auto_repair(path, G, slack)

    if repair_point:
        print(f"🔧 Suggested repair: Insert pipeline after {repair_point}")
    else:
        print("✅ No repair needed")

    print("\n=== SELF-HEALING FLOW ===")

    if repair_point:
        with open("samples/sample1.v", "r") as f:
            original_lines = f.readlines()

        healed_lines = run_self_heal(original_lines, repair_point)

        print("✅ Auto-fixed RTL generated:\n")

        for line in healed_lines:
            print(line, end="")

        print("\n=== TIMING CLOSURE LOOP ===")

    with open("samples/sample1.v", "r") as f:
        original_lines = f.readlines()

    closed_lines = timing_closure_loop(
        original_lines,
        clock_period=2
    )

    print("\n=== FINAL TIMING-CLOSED RTL ===\n")

    for line in closed_lines:
        print(line, end="")

    print("\n=== OPTIMIZATION SCORE ===")

    original_delay = 3
    new_delay = 2

    reg_count = count_registers(closed_lines)
    logic_nodes = count_logic_nodes(G)

    score = compute_score(
        original_delay,
        new_delay,
        reg_count,
        logic_nodes
    )

    print(f"Registers Added: {reg_count}")
    print(f"Logic Nodes: {logic_nodes}")
    print(f"Optimization Score: {score}")

    print("\n=== REPAIR CANDIDATE RANKING ===")

    with open("samples/sample1.v", "r") as f:
        original_lines = f.readlines()

    candidates = path[1:-1]

    ranked = evaluate_candidates(
        original_lines,
        candidates,
        original_delay=3,
        clock_period=2
    )

    for candidate, score, slack in ranked:
        print(f"{candidate}: Score = {score}, Worst Slack = {slack}")

    print("\n=== BEST REPAIR DECISION ===")

    best_candidate = ranked[0]

    print(f"Selected Repair: {best_candidate[0]}")
    print(f"Best Score: {best_candidate[1]}")
    print(f"Worst Slack: {best_candidate[2]}")  

    print("\n=== LEARNING MEMORY UPDATE ===")

    pattern_key = "deep_logic_chain"

    update_memory(pattern_key, best_candidate[0])

    print(f"Stored learning: {pattern_key} → {best_candidate[0]}")

    print("\n=== MEMORY GUIDED PREDICTION ===")

    pattern_key = "deep_logic_chain"

    predicted = predict_best_repair(pattern_key)

    if predicted:
        print(f"Memory suggests trying: {predicted}")
    else:
        print("No learned repair yet")

    print("\n=== DECISION CONFIDENCE ===")

    confidence = compute_confidence(ranked)

    print(f"Confidence Level: {confidence}%")

    print("\n=== EXPLAINABLE DECISION ===")

    explanation = generate_explanation(
        best_candidate,
        ranked,
        predicted,
        confidence
    )

    for line in explanation:
        print("•", line)

    print("\n=== HISTORY UPDATE ===")

    save_history(
        best_candidate[0],
        best_candidate[1],
        best_candidate[2],
        confidence
    )

    print("Optimization history stored.")

    print("\n=== VISUAL DASHBOARD ===")

    plot_history()

    os.makedirs("output/reports", exist_ok=True)
    with open("output/reports/latest_report.txt", "w") as f:
        f.write("Optimization Complete\n")
        f.write(f"Best Repair: {best_candidate[0]}\n")
        f.write(f"Confidence: {confidence}%\n")

if __name__ == "__main__":
    main()