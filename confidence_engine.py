def compute_confidence(ranked_candidates):

    if len(ranked_candidates) < 2:
        return 100

    best_score = ranked_candidates[0][1]
    second_score = ranked_candidates[1][1]

    gap = best_score - second_score

    confidence = min(100, max(0, gap * 20))

    return round(confidence, 2)