def insert_multi_pipeline(verilog_lines, pipeline_signals):
    new_lines = []

    # Create register names
    reg_names = {sig: sig + "_reg" for sig in pipeline_signals}

    # ----------------------------
    # PASS 1: Modify RTL safely
    # ----------------------------
    for line in verilog_lines:

        # Add clk to module only once
        if "module" in line and "clk" not in line:
            line = line.replace("(", "(input clk, ")

        # Modify RHS safely
        if "=" in line:
            lhs, rhs = line.split("=", 1)

            for sig in pipeline_signals:
                reg_name = reg_names[sig]

                # Skip LHS modification
                if sig not in lhs:

                    # Prevent repeated replacement
                    if reg_name not in rhs and sig in rhs:
                        rhs = rhs.replace(sig, reg_name)

            line = lhs + "=" + rhs

        new_lines.append(line)

    # ----------------------------
    # PASS 2: Insert register declarations
    # ----------------------------
    for i, line in enumerate(new_lines):
        if "module" in line:
            idx = i + 1

            for sig in pipeline_signals:
                reg_decl = f"reg {reg_names[sig]};"

                # Avoid duplicate reg insertion
                already_exists = any(reg_decl in l for l in new_lines)

                if not already_exists:
                    new_lines.insert(idx, f"    {reg_decl}\n")
                    idx += 1

            break

    # ----------------------------
    # PASS 3: Insert always blocks
    # ----------------------------
    for i, line in enumerate(new_lines):
        if "endmodule" in line:
            idx = i

            for sig in pipeline_signals:

                reg_name = reg_names[sig]

                # Avoid duplicate always block
                assign_exists = any(
                    f"{reg_name} <=" in l for l in new_lines
                )

                if not assign_exists:
                    new_lines.insert(idx, f"\n    always @(posedge clk) begin\n")
                    new_lines.insert(idx + 1, f"        {reg_name} <= {sig};\n")
                    new_lines.insert(idx + 2, f"    end\n")
                    idx += 3

            break

    return new_lines