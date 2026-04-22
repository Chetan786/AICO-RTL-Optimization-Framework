from rtl_modifier import insert_multi_pipeline

def run_self_heal(lines, repair_point):
    pipeline_points = [repair_point]

    modified_lines = insert_multi_pipeline(lines, pipeline_points)

    return modified_lines