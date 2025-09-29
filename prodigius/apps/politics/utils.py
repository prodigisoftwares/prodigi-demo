from typing import Dict, Tuple

Q_AXIS = {
    1: ("x", 1.0),
    2: ("x", 1.0),
    3: ("y", 1.0),
    4: ("x", 1.0),
    5: ("x", 0.8),
    6: ("y", 0.8),
    7: ("x", 0.8),
    8: ("y", 0.8),
}


def score_answer(qnum: int, choice: str) -> float:
    axis, weight = Q_AXIS[qnum]
    if axis == "x":
        if choice == "A":
            return -1.0 * weight
        if choice == "B":
            return 1.0 * weight
        return 0.0
    else:
        if qnum in (3, 6):
            if choice == "A":
                return 1.0 * weight
            if choice == "B":
                return -1.0 * weight
            if choice == "Both":
                return 0.3 * weight
            return 0.0
        if qnum == 8:
            if choice == "A":
                return 0.6 * weight
            if choice == "B":
                return 0.6 * weight
            if choice == "Both":
                return 1.0 * weight
            return 0.0
        if choice == "A":
            return 1.0 * weight
        if choice == "B":
            return -1.0 * weight
        if choice == "Both":
            return 0.3 * weight
        return 0.0


def compute_coords(answers: Dict[str, str]) -> Tuple[float, float]:
    x_total = y_total = 0.0
    x_weight = y_weight = 0.0

    for qnum in range(1, 9):
        choice = answers.get(f"q{qnum}")
        if not choice:
            continue
        axis, weight = Q_AXIS[qnum]
        delta = score_answer(qnum, choice)
        if axis == "x":
            x_total += delta
            x_weight += weight
        else:
            y_total += delta
            y_weight += weight

    x = x_total / x_weight if x_weight else 0.0
    y = y_total / y_weight if y_weight else 0.0
    x = max(-1.0, min(1.0, x))
    y = max(-1.0, min(1.0, y))
    return x, y
