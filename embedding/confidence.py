import numpy as np

def calculate_retrieval_confidence(scores):
    MIN_SCORE = 0.35
    MAX_SCORE = 0.75

    valid_scores = [
        float(score)
        for score in scores[0]
        if score > -1
    ]

    if not valid_scores:
        return 0

    top_scores = valid_scores[:3]
    weights = np.array([0.5, 0.3, 0.2])#Gives most value to highest Score, lower to 2nd Highest and Lowest to 3rd Highest

    retrieval_score = np.sum(
        np.array(top_scores) * weights
    )

    normalized = (retrieval_score - MIN_SCORE) / (MAX_SCORE - MIN_SCORE)
    normalized = max(0, min(1, normalized))

    confidence = normalized * 100
    return confidence