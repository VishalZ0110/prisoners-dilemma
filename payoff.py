from typing import Tuple


# ─────────────────────────────────────────────────────────────────────────────
#  Payoff matrix  (action_alpha, action_beta) → (reward_alpha, reward_beta)
# ─────────────────────────────────────────────────────────────────────────────

PAYOFF_MATRIX: dict[Tuple[str, str], Tuple[int, int]] = {
    ("COOPERATE", "COOPERATE"): (3, 3),
    ("COOPERATE", "DEFECT"):    (0, 5),
    ("DEFECT",    "COOPERATE"): (5, 0),
    ("DEFECT",    "DEFECT"):    (1, 1),
}


def compute_payoff(action_alpha: str, action_beta: str) -> Tuple[int, int]:
    """
    Return (reward_alpha, reward_beta) for a given pair of actions.

    Both actions must be either "COOPERATE" or "DEFECT".
    """
    key = (action_alpha, action_beta)
    if key not in PAYOFF_MATRIX:
        raise ValueError(
            f"Invalid action pair: {key}. "
            "Each action must be 'COOPERATE' or 'DEFECT'."
        )
    return PAYOFF_MATRIX[key]
