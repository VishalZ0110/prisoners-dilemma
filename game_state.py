from dataclasses import dataclass, field
from typing import List


@dataclass
class TurnRecord:
    """Stores what happened in a single turn, including each agent's reasoning."""
    turn_number:      int
    action_alpha:     str
    action_beta:      str
    reward_alpha:     int
    reward_beta:      int
    reasoning_alpha:  str = ""
    reasoning_beta:   str = ""


@dataclass
class GameState:
    """
    Central state object shared by the controller and both agents.

    Tracks cumulative scores and the full turn-by-turn history.
    Each agent receives history formatted from its own perspective
    (its own moves labelled "You:", the opponent labelled by name).
    """

    total_turns: int
    agent_names: List[str]       # [alpha_name, beta_name]
    score_alpha: int = 0
    score_beta:  int = 0
    history:     List[TurnRecord] = field(default_factory=list)

    # ── Convenience properties ────────────────────────────────────────

    @property
    def current_turn(self) -> int:
        return len(self.history) + 1

    @property
    def alpha_name(self) -> str:
        return self.agent_names[0]

    @property
    def beta_name(self) -> str:
        return self.agent_names[1]

    # ── Mutation ──────────────────────────────────────────────────────

    def record_turn(
        self,
        action_alpha:    str,
        action_beta:     str,
        reward_alpha:    int,
        reward_beta:     int,
        reasoning_alpha: str = "",
        reasoning_beta:  str = "",
    ) -> None:
        """Append a completed turn and update cumulative scores."""
        record = TurnRecord(
            turn_number     = self.current_turn,
            action_alpha    = action_alpha,
            action_beta     = action_beta,
            reward_alpha    = reward_alpha,
            reward_beta     = reward_beta,
            reasoning_alpha = reasoning_alpha,
            reasoning_beta  = reasoning_beta,
        )
        self.history.append(record)
        self.score_alpha += reward_alpha
        self.score_beta  += reward_beta

    # ── History formatters ────────────────────────────────────────────

    def history_for_alpha(self) -> str:
        """Return history text from Agent Alpha's perspective."""
        if not self.history:
            return "No previous turns."
        lines = []
        for record in self.history:
            lines += [
                f"Turn {record.turn_number}",
                f"You: {record.action_alpha}",
                f"{self.beta_name}: {record.action_beta}",
                "",
            ]
        return "\n".join(lines).strip()

    def history_for_beta(self) -> str:
        """Return history text from Agent Beta's perspective."""
        if not self.history:
            return "No previous turns."
        lines = []
        for record in self.history:
            lines += [
                f"Turn {record.turn_number}",
                f"You: {record.action_beta}",
                f"{self.alpha_name}: {record.action_alpha}",
                "",
            ]
        return "\n".join(lines).strip()
