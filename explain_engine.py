def generate_explanation(
    best_candidate,
    ranked,
    predicted,
    confidence
):

    explanation = []

    explanation.append(
        f"Selected '{best_candidate[0]}' because it achieved the highest score ({best_candidate[1]})."
    )

    explanation.append(
        f"Worst slack after repair = {best_candidate[2]}."
    )

    if predicted == best_candidate[0]:
        explanation.append(
            "Memory prediction matched final decision."
        )

    explanation.append(
        f"Decision confidence = {confidence}%."
    )

    return explanation