def calculate_accuracy(predictions: list[str], ground_truth: list[str]) -> float:
    if not ground_truth:
        return 0.0
    correct = sum(1 for p, g in zip(predictions, ground_truth) if p == g)
    return correct / len(ground_truth)


def calculate_abstention_f1(pred_abstains: list[bool], gold_abstains: list[bool]) -> float:
    tp = sum(1 for p, g in zip(pred_abstains, gold_abstains) if p and g)
    fp = sum(1 for p, g in zip(pred_abstains, gold_abstains) if p and not g)
    fn = sum(1 for p, g in zip(pred_abstains, gold_abstains) if not p and g)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    return (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
